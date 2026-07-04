#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <poll.h>
#include <stdint.h>
#include <stddef.h>
#include <signal.h>
#include <stdbool.h>

#include "frame.h"
#include "frame_v1_wire.h"

static int now_process_cpu_ns(uint64_t *out_ns);
static void normalize_trial_summary_link_name(const char *link_name, char *out, size_t out_size);

static volatile sig_atomic_t g_stop_requested = 0;

static void on_stop_signal(int signo) {
    (void)signo;
    g_stop_requested = 1;
}

static int install_signal_handlers(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_handler = on_stop_signal;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;  // SA_RESTARTなし（pollをEINTRで返しやすくする）

    if (sigaction(SIGINT, &sa, NULL) != 0) {
        return -1;
    }
    if (sigaction(SIGTERM, &sa, NULL) != 0) {
        return -1;
    }
    return 0;
}

typedef struct {
    const char *bind_ip;   // bind先IP（例: "127.0.0.1" / "0.0.0.0"）
    int port;              // bindポート
    int duration_sec;       // 実行時間（受信ループの終了条件）
    const char *log_path;  // ログファイルパス
    int rcvbuf;            // SO_RCVBUF に設定する受信バッファサイズ（byte）
    int rcvbuf_set;        // --rcvbuf が明示指定されたか
    const char *link_name;  // trial_summary の link 識別子（Host loopback / 実リンク名など）
    bool has_link_name;    // --link-name が明示指定されたか
    int trial;             // trial_summary の試行番号（1始まりを想定）
    bool has_trial;        // --trial が明示指定されたか
    const char *csv_in_1sec_log_path;  // １秒ごとの統計ログ（rx_stats）をCSV形式で出力する場合のファイルパス（オプション、未指定ならCSV出力しない）
    const char *csv_by_1recv_log_path;  // 受信ごとの統計ログ（rx_stats）をCSV形式で出力する場合のファイルパス（オプション、未指定ならCSV出力しない）
    const char *state_log_path;  // FSM 状態遷移をCSV形式で出力する場合のファイルパス（オプション、未指定ならCSV出力しない）
    int recovery_mode;  // W05 の復旧モード（0=fsm, 1=timeout-only）
    int crc32_test_mode;  // ハードコードした v1 フレームで CRC32 を確認する
} RxConfig;

typedef struct {
    FILE *log_fp;
    FILE *csv_in_1sec_fp;
    FILE *csv_by_1recv_fp;
    FILE *state_fp;
} RxFiles;

typedef struct {
    uint64_t recv_any;
    uint64_t recv_ok;
    uint64_t bad_size;
    uint64_t bad_header;
    uint64_t bad_crc;
    uint64_t resync_count;   // PREAMBLE_MISS / LEN_INVALID / CRC_FAIL で再探索した回数
    uint64_t preamble_miss;  // preamble が先頭にないと判定された回数（FRAMER_RESYNCED のみ）
    uint64_t len_invalid;    // payload_len が上限超えのフレーム数（LEN_INVALID）
    uint64_t poll_timeout;
    uint64_t gap_cnt;
    uint64_t dup_cnt;
    uint64_t reord_cnt;
    uint64_t latency_sum_ns;
    uint64_t latency_sample_cnt;
    uint64_t future_ts_cnt;
    uint64_t future_ts_detected;
    uint64_t min_latency_ns;
    uint64_t max_latency_ns;
    uint64_t *latency_samples_ns;
    size_t latency_samples_len;
    size_t latency_samples_cap;
    bool latency_samples_oom;
    bool collect_latency_samples;
} RxTotals;

typedef struct {
    uint32_t prev_seq;
    bool has_prev_seq;
} SeqState;

typedef struct {
    uint64_t recv_any;
    uint64_t recv_ok;
    uint64_t gap_cnt;
    uint64_t dup_cnt;
    uint64_t reord_cnt;
    uint64_t latency_sum_ns;
    uint64_t latency_sample_cnt;
    uint64_t max_latency_ns;
    uint64_t min_latency_ns;
} WindowStats;

typedef struct {
    uint64_t t_start_ns;
    uint64_t next_stats_ns;
    uint64_t now_ns;
    uint64_t recv_now_ns;
    uint64_t now_for_stats_ns;
    uint64_t elapsed_sec;
    uint64_t avg_latency_ns_in_1sec;
    uint64_t last_stats_wall_ns;
    uint64_t last_process_cpu_ns;
    uint64_t gap;
    uint64_t latency;
    int wait_ms;
    int win_idx;
    int target_idx;
    int cur_idx;
    double pps_in_1sec;
    double cpu_pct_in_1sec;
    WindowStats win_stats[2];
} RxTimingState;

typedef enum {
    RX_LINK_STATE_NORMAL = 0,
    RX_LINK_STATE_DEGRADED = 1,
    RX_LINK_STATE_RECOVER = 2,
} RxLinkState;

typedef struct {
    RxLinkState state;
    uint64_t consecutive_empty_windows;
    uint64_t consecutive_good_windows;
} RxLinkFsm;

typedef enum {
    RX_RECOVERY_MODE_FSM = 0,
    RX_RECOVERY_MODE_TIMEOUT_ONLY = 1,
} RxRecoveryMode;

#define RX_FSM_DEGRADED_EMPTY_WINDOWS UINT64_C(2)
#define RX_FSM_RECOVER_GOOD_WINDOWS UINT64_C(2)

#define RX_STREAM_BUF_CAP (FRAME_V1_MAX_WIRE_BYTES * 4)

typedef struct {
    uint8_t data[RX_STREAM_BUF_CAP];
    size_t  len;   // バッファに溜まっているバイト数
} RxStreamBuf;

typedef enum {
    FRAMER_OK        = 0,  // フレーム抽出成功。out に格納済み・バッファ消費済み
    FRAMER_NEED_MORE = 1,  // バイト不足。次の recvfrom を待つ
    FRAMER_RESYNCED  = 2,  // 不正データを読み飛ばした。同バッファで再試行せよ
} FramerResult;

static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s --bind-ip <ip> --port <port> --duration-sec <sec> --log-path <path> [--rcvbuf <bytes>] [--link-name <name>] [--trial <n>] [--csv-in-1sec-log-path <path>] [--csv-by-1recv-log-path <path>] [--state-log-path <path>] [--recovery-mode fsm|timeout-only] [--crc32-test]\n",
            prog);
}

static int parse_int(const char *s, int *out) {
    char *end = NULL;
    errno = 0;
    long v = strtol(s, &end, 10);
    if (errno != 0 || end == s || *end != '\0') return -1;
    if (v < -2147483648L || v > 2147483647L) return -1;
    *out = (int)v;
    return 0;
}

static int parse_recovery_mode(const char *s, int *out) {
    if (!s || !out) {
        return -1;
    }
    if (strcmp(s, "fsm") == 0) {
        *out = RX_RECOVERY_MODE_FSM;
        return 0;
    }
    if (strcmp(s, "timeout-only") == 0) {
        *out = RX_RECOVERY_MODE_TIMEOUT_ONLY;
        return 0;
    }
    return -1;
}

static int parse_args(int argc, char **argv, RxConfig *cfg) {
    int opt;
    int option_index = 0;

    static struct option long_opts[] = {
        {"bind-ip", required_argument, 0, 1},
        {"port", required_argument, 0, 2},
        {"duration-sec", required_argument, 0, 3},
        {"log-path", required_argument, 0, 4},
        {"link-name", required_argument, 0, 5},
        {"trial", required_argument, 0, 6},
        {"csv-in-1sec-log-path", required_argument, 0, 7},
        {"csv-by-1recv-log-path", required_argument, 0, 8},
        {"state-log-path", required_argument, 0, 9},
        {"recovery-mode", required_argument, 0, 10},
        {"crc32-test", no_argument, 0, 11},
        {"rcvbuf", required_argument, 0, 12},
        {0, 0, 0, 0}
    };

    while ((opt = getopt_long(argc, argv, "", long_opts, &option_index)) != -1) {
        switch (opt) {
            case 1:
                cfg->bind_ip = optarg;
                break;

            case 2:
                if (parse_int(optarg, &cfg->port) != 0) {
                    fprintf(stderr, "Invalid --port: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;

            case 3:
                if (parse_int(optarg, &cfg->duration_sec) != 0) {
                    fprintf(stderr, "Invalid --duration-sec: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;

            case 4:
                cfg->log_path = optarg;
                break;

            case 5:
                cfg->link_name = optarg;
                cfg->has_link_name = true;
                break;

            case 6:
                if (parse_int(optarg, &cfg->trial) != 0 || cfg->trial <= 0) {
                    fprintf(stderr, "Invalid --trial: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                cfg->has_trial = true;
                break;

            case 7:
                cfg->csv_in_1sec_log_path = optarg;
                break;

            case 8:
                cfg->csv_by_1recv_log_path = optarg;
                break;
            case 9:
                cfg->state_log_path = optarg;
                break;
            case 10:
                if (parse_recovery_mode(optarg, &cfg->recovery_mode) != 0) {
                    fprintf(stderr, "Invalid --recovery-mode: %s (expected fsm|timeout-only)\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 11:
                cfg->crc32_test_mode = 1;
                break;
            case 12:
                if (parse_int(optarg, &cfg->rcvbuf) != 0) {
                    fprintf(stderr, "Invalid --rcvbuf: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                cfg->rcvbuf_set = 1;
                break;

            default:
                print_usage(argv[0]);
                return -1;
        }
    }

    if (cfg->crc32_test_mode) {
        return 0;
    }

    if (!cfg->log_path || cfg->port <= 0 || cfg->port > 65535 || cfg->duration_sec <= 0) {
        print_usage(argv[0]);
        return -1;
    }

    if (cfg->recovery_mode != RX_RECOVERY_MODE_FSM &&
        cfg->recovery_mode != RX_RECOVERY_MODE_TIMEOUT_ONLY) {
        cfg->recovery_mode = RX_RECOVERY_MODE_FSM;
    }

    if (cfg->rcvbuf_set && cfg->rcvbuf <= 0) {
        fprintf(stderr, "Invalid --rcvbuf: %d (expected > 0)\n", cfg->rcvbuf);
        print_usage(argv[0]);
        return -1;
    }

    return 0;
}

static void close_output_files(RxFiles *files) {
    if (files->log_fp) {
        fclose(files->log_fp);
        files->log_fp = NULL;
    }
    if (files->csv_in_1sec_fp) {
        fclose(files->csv_in_1sec_fp);
        files->csv_in_1sec_fp = NULL;
    }
    if (files->csv_by_1recv_fp) {
        fclose(files->csv_by_1recv_fp);
        files->csv_by_1recv_fp = NULL;
    }
    if (files->state_fp) {
        fclose(files->state_fp);
        files->state_fp = NULL;
    }
}

static int open_output_files(const RxConfig *config, RxFiles *files) {
    files->log_fp = fopen(config->log_path, "a");
    if (!files->log_fp) {
        perror("fopen(log_path)");
        return -1;
    }

    if (config->csv_in_1sec_log_path) {
        files->csv_in_1sec_fp = fopen(config->csv_in_1sec_log_path, "w");
        if (!files->csv_in_1sec_fp) {
            perror("fopen(csv_in_1sec_log_path)");
            close_output_files(files);
            return -1;
        }
        fprintf(files->csv_in_1sec_fp, "elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt,pps,cpu_pct\n");
        fflush(files->csv_in_1sec_fp);
    }

    if (config->csv_by_1recv_log_path) {
        files->csv_by_1recv_fp = fopen(config->csv_by_1recv_log_path, "w");
        if (!files->csv_by_1recv_fp) {
            perror("fopen(csv_by_1recv_log_path)");
            close_output_files(files);
            return -1;
        }
        fprintf(files->csv_by_1recv_fp, "rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status\n");
        fflush(files->csv_by_1recv_fp);
    }

    if (config->state_log_path) {
        files->state_fp = fopen(config->state_log_path, "w");
        if (!files->state_fp) {
            perror("fopen(state_log_path)");
            close_output_files(files);
            return -1;
        }
        fprintf(files->state_fp, "link_name,trial,mono_ns,elapsed_ms,from_state,to_state,reason\n");
        fflush(files->state_fp);
    }

    return 0;
}

static void write_log_line(FILE *fp, const char *level, const char *msg);

static int apply_socket_buffer_setting(FILE *log_fp, int sock, int optname, const char *opt_label, int requested) {
    int value = requested;
    socklen_t actual_len = sizeof(value);

    if (setsockopt(sock, SOL_SOCKET, optname, &value, sizeof(value)) != 0) {
        char msg[256];
        snprintf(msg, sizeof(msg), "setsockopt failed option=%s requested=%d", opt_label, requested);
        write_log_line(log_fp, "ERROR", msg);
        perror(opt_label);
        return -1;
    }

    if (getsockopt(sock, SOL_SOCKET, optname, &value, &actual_len) != 0) {
        char msg[256];
        snprintf(msg, sizeof(msg), "getsockopt failed option=%s requested=%d", opt_label, requested);
        write_log_line(log_fp, "ERROR", msg);
        perror(opt_label);
        return -1;
    }

    char msg[256];
    snprintf(msg, sizeof(msg), "socket buffer option=%s requested=%d actual=%d", opt_label, requested, value);
    write_log_line(log_fp, "INFO", msg);
    return 0;
}

static void write_log_line(FILE *fp, const char *level, const char *msg) {
    if (!fp || !level || !msg) {
        return;
    }
    time_t now = time(NULL);
    struct tm tmv;
    localtime_r(&now, &tmv);

    char ts[64];
    strftime(ts, sizeof(ts), "%Y-%m-%d %H:%M:%S", &tmv);
    fprintf(fp, "%s [%s] %s\n", ts, level, msg);
    fflush(fp);
}

static const char *rx_link_state_name(RxLinkState state) {
    switch (state) {
        case RX_LINK_STATE_NORMAL:
            return "Normal";
        case RX_LINK_STATE_DEGRADED:
            return "Degraded";
        case RX_LINK_STATE_RECOVER:
            return "Recover";
        default:
            return "Unknown";
    }
}

static const char *rx_recovery_mode_name(RxRecoveryMode mode) {
    switch (mode) {
        case RX_RECOVERY_MODE_TIMEOUT_ONLY:
            return "timeout-only";
        case RX_RECOVERY_MODE_FSM:
        default:
            return "fsm";
    }
}

static void write_fsm_threshold_log(const RxFiles *files, RxRecoveryMode mode, RxLinkState initial_state) {
    char msg[256];

    if (!files || !files->log_fp) {
        return;
    }

    snprintf(
        msg,
        sizeof(msg),
        "link_fsm mode=%s initial=%s degraded_detect=recv_ok_zero_for_%llu"
        "_windows recover_complete=recv_ok_positive_for_%llu_windows",
        rx_recovery_mode_name(mode),
        rx_link_state_name(initial_state),
        (unsigned long long)RX_FSM_DEGRADED_EMPTY_WINDOWS,
        (unsigned long long)RX_FSM_RECOVER_GOOD_WINDOWS
    );
    write_log_line(files->log_fp, "INFO", msg);
}

static void write_fsm_transition_log(
    const RxFiles *files,
    RxLinkState from_state,
    RxLinkState to_state,
    uint64_t t_start_ns,
    uint64_t event_ns,
    uint64_t empty_windows,
    uint64_t good_windows,
    uint64_t recv_ok_in_window,
    const char *reason
) {
    char msg[256];
    uint64_t since_start_ms = 0;

    if (!files || !files->log_fp || !reason) {
        return;
    }
    if (event_ns >= t_start_ns) {
        since_start_ms = (event_ns - t_start_ns) / UINT64_C(1000000);
    }

    snprintf(
        msg,
        sizeof(msg),
        "link_state %s -> %s since_start_ms=%llu"
        " reason=%s empty_windows=%llu"
        " good_windows=%llu recv_ok_in_window=%llu",
        rx_link_state_name(from_state),
        rx_link_state_name(to_state),
        (unsigned long long)since_start_ms,
        reason,
        (unsigned long long)empty_windows,
        (unsigned long long)good_windows,
        (unsigned long long)recv_ok_in_window
    );
    write_log_line(files->log_fp, "INFO", msg);
}

static void write_fsm_transition_csv(
    const RxFiles *files,
    const RxConfig *config,
    RxLinkState from_state,
    RxLinkState to_state,
    uint64_t t_start_ns,
    uint64_t event_ns,
    const char *reason
) {
    char link_name_token[128];
    uint64_t elapsed_ms = 0;

    if (!files || !files->state_fp || !config || !reason) {
        return;
    }
    if (!config->has_link_name || !config->has_trial) {
        return;
    }

    normalize_trial_summary_link_name(config->link_name, link_name_token, sizeof(link_name_token));
    if (event_ns >= t_start_ns) {
        elapsed_ms = (event_ns - t_start_ns) / UINT64_C(1000000);
    }

    fprintf(
        files->state_fp,
        "%s,%d,%llu,%llu,%s,%s,%s\n",
        link_name_token,
        config->trial,
        (unsigned long long)event_ns,
        (unsigned long long)elapsed_ms,
        rx_link_state_name(from_state),
        rx_link_state_name(to_state),
        reason
    );
    fflush(files->state_fp);
}

static void transition_link_state(
    const RxFiles *files,
    const RxConfig *config,
    RxLinkFsm *fsm,
    RxLinkState next_state,
    uint64_t t_start_ns,
    uint64_t event_ns,
    uint64_t recv_ok_in_window,
    const char *reason
) {
    RxLinkState prev_state;

    if (!fsm || fsm->state == next_state) {
        return;
    }

    prev_state = fsm->state;
    write_fsm_transition_log(
        files,
        prev_state,
        next_state,
        t_start_ns,
        event_ns,
        fsm->consecutive_empty_windows,
        fsm->consecutive_good_windows,
        recv_ok_in_window,
        reason
    );
    write_fsm_transition_csv(
        files,
        config,
        prev_state,
        next_state,
        t_start_ns,
        event_ns,
        reason
    );

    fsm->state = next_state;
    switch (next_state) {
        case RX_LINK_STATE_NORMAL:
            fsm->consecutive_empty_windows = 0;
            fsm->consecutive_good_windows = 0;
            break;
        case RX_LINK_STATE_DEGRADED:
            fsm->consecutive_good_windows = 0;
            break;
        case RX_LINK_STATE_RECOVER:
            fsm->consecutive_empty_windows = 0;
            fsm->consecutive_good_windows = 0;
            break;
        default:
            break;
    }
}

static void write_summary(const RxFiles *files, const RxTotals *totals, uint64_t elapsed_ns) {
    char msg[512];

    if (!files || !files->log_fp || !totals) {
        return;
    }

    snprintf(
        msg,
        sizeof(msg),
        "rx summary recv_any=%llu recv_ok=%llu"
        " bad_size=%llu bad_header=%llu bad_crc=%llu"
        " resync_count=%llu preamble_miss=%llu"
        " crc_fail=%llu len_invalid=%llu"
        " poll_timeout=%llu"
        " elapsed_ms=%llu avg_latency_ms=%.3f"
        " max_latency_ms=%llu min_latency_ms=%llu"
        " gap_cnt=%llu dup_cnt=%llu reord_cnt=%llu"
        " future_ts_cnt=%llu future_ts_detected=%llu",
        (unsigned long long)totals->recv_any,
        (unsigned long long)totals->recv_ok,
        (unsigned long long)totals->bad_size,
        (unsigned long long)totals->bad_header,
        (unsigned long long)totals->bad_crc,
        (unsigned long long)totals->resync_count,
        (unsigned long long)totals->preamble_miss,
        (unsigned long long)totals->bad_crc,      // crc_fail = bad_crc の別名
        (unsigned long long)totals->len_invalid,
        (unsigned long long)totals->poll_timeout,
        (unsigned long long)(elapsed_ns / UINT64_C(1000000)),
        (totals->latency_sample_cnt > 0)
            ? (double)totals->latency_sum_ns / (double)totals->latency_sample_cnt / 1000000.0
            : 0.0,
        (unsigned long long)(totals->max_latency_ns / UINT64_C(1000000)),
        (unsigned long long)(totals->min_latency_ns / UINT64_C(1000000)),
        (unsigned long long)totals->gap_cnt,
        (unsigned long long)totals->dup_cnt,
        (unsigned long long)totals->reord_cnt,
        (unsigned long long)totals->future_ts_cnt,
        (unsigned long long)totals->future_ts_detected
    );

    write_log_line(files->log_fp, "INFO", msg);
}

static bool is_trial_summary_token_char(char ch) {
    return
        (ch >= '0' && ch <= '9') ||
        (ch >= 'A' && ch <= 'Z') ||
        (ch >= 'a' && ch <= 'z') ||
        ch == '_' || ch == '-' || ch == '.' || ch == ':';
}

static void normalize_trial_summary_link_name(const char *link_name, char *out, size_t out_size) {
    size_t i = 0;

    if (!out || out_size == 0) {
        return;
    }

    if (!link_name || link_name[0] == '\0') {
        snprintf(out, out_size, "unknown");
        return;
    }

    for (; link_name[i] != '\0' && i + 1 < out_size; i++) {
        out[i] = is_trial_summary_token_char(link_name[i]) ? link_name[i] : '_';
    }
    out[i] = '\0';

    if (i == 0) {
        snprintf(out, out_size, "unknown");
    }
}

static int compare_u64_asc(const void *a, const void *b) {
    uint64_t va = *(const uint64_t *)a;
    uint64_t vb = *(const uint64_t *)b;

    if (va < vb) {
        return -1;
    }
    if (va > vb) {
        return 1;
    }
    return 0;
}

static size_t latency_percentile_index(size_t sample_count, size_t percentile) {
    size_t rank = (sample_count * percentile + 99) / 100;
    if (rank == 0) {
        rank = 1;
    }
    return rank - 1;
}

static void format_latency_ms(char *out, size_t out_size, uint64_t latency_ns) {
    if (!out || out_size == 0) {
        return;
    }
    snprintf(out, out_size, "%.3f", (double)latency_ns / 1000000.0);
}

static void build_trial_summary_latency_fields(
    RxTotals *totals,
    char *p50_ms,
    size_t p50_ms_size,
    char *p95_ms,
    size_t p95_ms_size,
    char *p99_ms,
    size_t p99_ms_size,
    char *max_ms,
    size_t max_ms_size
) {
    if (!totals || !p50_ms || !p95_ms || !p99_ms || !max_ms) {
        return;
    }

    snprintf(p50_ms, p50_ms_size, "na");
    snprintf(p95_ms, p95_ms_size, "na");
    snprintf(p99_ms, p99_ms_size, "na");
    snprintf(max_ms, max_ms_size, "na");

    if (totals->latency_sample_cnt == 0) {
        return;
    }
    if (totals->recv_ok != totals->latency_sample_cnt) {
        return;
    }
    if (totals->latency_samples_oom || totals->latency_samples_len != totals->latency_sample_cnt) {
        return;
    }

    qsort(
        totals->latency_samples_ns,
        totals->latency_samples_len,
        sizeof(totals->latency_samples_ns[0]),
        compare_u64_asc
    );

    format_latency_ms(
        p50_ms,
        p50_ms_size,
        totals->latency_samples_ns[latency_percentile_index(totals->latency_samples_len, 50)]
    );
    format_latency_ms(
        p95_ms,
        p95_ms_size,
        totals->latency_samples_ns[latency_percentile_index(totals->latency_samples_len, 95)]
    );
    format_latency_ms(
        p99_ms,
        p99_ms_size,
        totals->latency_samples_ns[latency_percentile_index(totals->latency_samples_len, 99)]
    );
    format_latency_ms(max_ms, max_ms_size, totals->max_latency_ns);
}

static void write_trial_summary(const RxFiles *files, const RxConfig *config, RxTotals *totals) {
    char msg[768];
    char link_name_token[128];
    char latency_p50_ms[32];
    char latency_p95_ms[32];
    char latency_p99_ms[32];
    char latency_max_ms[32];

    if (!files || !files->log_fp || !config || !totals) {
        return;
    }
    if (!config->has_link_name || !config->has_trial) {
        return;
    }

    normalize_trial_summary_link_name(config->link_name, link_name_token, sizeof(link_name_token));
    build_trial_summary_latency_fields(
        totals,
        latency_p50_ms,
        sizeof(latency_p50_ms),
        latency_p95_ms,
        sizeof(latency_p95_ms),
        latency_p99_ms,
        sizeof(latency_p99_ms),
        latency_max_ms,
        sizeof(latency_max_ms)
    );

    snprintf(
        msg,
        sizeof(msg),
        "trial_summary link_name=%s trial=%d duration_sec=%d sent=na"
        " recv_ok=%llu gap_est=%llu crc_fail=%llu"
        " len_invalid=%llu preamble_miss=%llu"
        " resync_count=%llu"
        " latency_p50_ms=%s latency_p95_ms=%s latency_p99_ms=%s latency_max_ms=%s",
        link_name_token,
        config->trial,
        config->duration_sec,
        (unsigned long long)totals->recv_ok,
        (unsigned long long)totals->gap_cnt,
        (unsigned long long)totals->bad_crc,
        (unsigned long long)totals->len_invalid,
        (unsigned long long)totals->preamble_miss,
        (unsigned long long)totals->resync_count,
        latency_p50_ms,
        latency_p95_ms,
        latency_p99_ms,
        latency_max_ms
    );

    write_log_line(files->log_fp, "INFO", msg);
}

static void append_latency_sample(RxTotals *totals, uint64_t latency_ns) {
    size_t new_cap = 0;
    uint64_t *new_buf = NULL;

    if (!totals || !totals->collect_latency_samples || totals->latency_samples_oom) {
        return;
    }
    if (totals->latency_samples_len == totals->latency_samples_cap) {
        new_cap = (totals->latency_samples_cap == 0) ? 256 : totals->latency_samples_cap * 2;
        new_buf = realloc(totals->latency_samples_ns, new_cap * sizeof(new_buf[0]));
        if (!new_buf) {
            totals->latency_samples_oom = true;
            return;
        }
        totals->latency_samples_ns = new_buf;
        totals->latency_samples_cap = new_cap;
    }

    totals->latency_samples_ns[totals->latency_samples_len++] = latency_ns;
}

static int now_monotonic_ns(uint64_t *out_ns) {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) {
        return -1;
    }
    *out_ns = (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
    return 0;
}

static int build_bind_addr(const char *ip, int port, struct sockaddr_in *out) {
    memset(out, 0, sizeof(*out));
    out->sin_family = AF_INET;
    out->sin_port = htons((uint16_t)port);

    int rc = inet_pton(AF_INET, ip, &out->sin_addr);
    if (rc != 1) {
        if (rc == 0) {
            fprintf(stderr, "Invalid IPv4 address: %s\n", ip);
        } else {
            perror("inet_pton");
        }
        return -1;
    }
    return 0;
}

static WindowStats *select_window_stats(RxTimingState *ts) {
    if (ts->recv_now_ns >= ts->next_stats_ns) {
        ts->target_idx = (ts->win_idx + 1) % 2;
    } else {
        ts->target_idx = ts->win_idx % 2;
    }

    return &ts->win_stats[ts->target_idx];
}

static void update_seq_stats(
    uint32_t seq_value,
    SeqState *seq,
    RxTotals *totals,
    RxTimingState *ts,
    WindowStats *win
) {
    ts->gap = 0;

    if (seq->has_prev_seq) {
        if (seq->prev_seq == seq_value) {
            totals->dup_cnt++;
            win->dup_cnt++;
        } else if (seq->prev_seq < seq_value) {
            ts->gap = seq_value - seq->prev_seq - 1;
            totals->gap_cnt += ts->gap;
            win->gap_cnt += ts->gap;
            seq->prev_seq = seq_value;
        } else if (seq_value < seq->prev_seq) {
            totals->reord_cnt++;
            win->reord_cnt++;
        }
    } else {
        seq->has_prev_seq = true;
        seq->prev_seq = seq_value;
    }
}

static void update_latency_stats(
    uint64_t tx_ts_ns,
    RxTotals *totals,
    RxTimingState *ts,
    WindowStats *win
) {
    ts->latency = 0;
    if (ts->recv_now_ns >= tx_ts_ns) {
        ts->latency = ts->recv_now_ns - tx_ts_ns;
        totals->latency_sum_ns += ts->latency;

        totals->latency_sample_cnt++;
        win->latency_sample_cnt++;
        win->latency_sum_ns += ts->latency;
        if (ts->latency > totals->max_latency_ns) {
            totals->max_latency_ns = ts->latency;
        }
        if (totals->min_latency_ns == 0 || ts->latency < totals->min_latency_ns) {
            totals->min_latency_ns = ts->latency;
        }
        append_latency_sample(totals, ts->latency);
        if (ts->latency > win->max_latency_ns) {
            win->max_latency_ns = ts->latency;
        }
        if (ts->latency < win->min_latency_ns || win->min_latency_ns == 0) {
            win->min_latency_ns = ts->latency;
        }
    } else {
        totals->future_ts_cnt++;
    }
    if (ts->recv_now_ns < tx_ts_ns) {
        totals->future_ts_detected = 1;
    }
}

static void write_per_recv_csv(const RxFiles *files, const RxTimingState *ts, uint32_t seq_value, uint64_t tx_ts_ns) {
    char msg_csv_by_1recv[256];
    if (files->csv_by_1recv_fp) {
        snprintf(msg_csv_by_1recv, sizeof(msg_csv_by_1recv),
            "%llu,%lu,%llu,%llu,%llu,OK\n",
            (unsigned long long)ts->recv_now_ns, (unsigned long)seq_value, (unsigned long long)tx_ts_ns,
            (unsigned long long)ts->latency, (unsigned long long)ts->gap
            );
        fprintf(files->csv_by_1recv_fp, "%s", msg_csv_by_1recv);
        fflush(files->csv_by_1recv_fp);
    }
}

static void write_fault_csv(const RxFiles *files, uint64_t recv_now_ns, const char *parse_status) {
    if (files->csv_by_1recv_fp) {
        fprintf(files->csv_by_1recv_fp,
                "%llu,0,0,0,0,%s\n",
                (unsigned long long)recv_now_ns, parse_status);
        fflush(files->csv_by_1recv_fp);
    }
}

static int rx_buf_append(RxStreamBuf *buf, const uint8_t *data, size_t len) {
    if (buf->len + len > RX_STREAM_BUF_CAP) {
        return -1;
    }
    memcpy(&buf->data[buf->len], data, len);
    buf->len += len;
    return 0;
}

static void rx_buf_consume(RxStreamBuf *buf, size_t n) {
    if (n >= buf->len) {
        buf->len = 0;
        return;
    }
    memmove(buf->data, &buf->data[n], buf->len - n);
    buf->len -= n;
}

static size_t rx_buf_find_preamble(const RxStreamBuf *buf) {
    const uint8_t p0 = (uint8_t)(kFrameV1Preamble >> 24);
    const uint8_t p1 = (uint8_t)(kFrameV1Preamble >> 16);
    const uint8_t p2 = (uint8_t)(kFrameV1Preamble >> 8);
    const uint8_t p3 = (uint8_t)(kFrameV1Preamble);

    if (buf->len < 4) {
        return buf->len;
    }

    for (size_t i = 0; i <= buf->len - 4; i++) {
        if (buf->data[i]     == p0 &&
            buf->data[i + 1] == p1 &&
            buf->data[i + 2] == p2 &&
            buf->data[i + 3] == p3) {
            return i;
        }
    }

    return buf->len;
}

static FramerResult rx_framer_step(
    RxStreamBuf *buf,
    FrameV1Parsed *out,
    RxTotals *totals,
    FILE *log_fp,
    char *msg,
    size_t msg_size,
    const char **out_event_type  // "OK" / "CRC_FAIL" / "LEN_INVALID" / "HEADER_INVALID" / "PREAMBLE_MISS"
) {
    size_t preamble_off = rx_buf_find_preamble(buf);

    if (preamble_off == buf->len) {
        if (buf->len > 3) {
            size_t drop = buf->len - 3;
            totals->resync_count++;
            totals->bad_size += drop;
            rx_buf_consume(buf, drop);
        }
        return FRAMER_NEED_MORE;
    }

    if (preamble_off > 0) {
        totals->resync_count++;
        totals->preamble_miss++;
        totals->bad_size += preamble_off;
        rx_buf_consume(buf, preamble_off);
        *out_event_type = "PREAMBLE_MISS";
        return FRAMER_RESYNCED;
    }

    if (buf->len < FRAME_V1_WIRE_HEADER_LEN) {
        return FRAMER_NEED_MORE;
    }

    uint16_t payload_len_peek =
        ((uint16_t)buf->data[FRAME_V1_PAYLOAD_LEN_OFFSET] << 8) |
        (uint16_t)buf->data[FRAME_V1_PAYLOAD_LEN_OFFSET + 1];

    if ((size_t)payload_len_peek > FRAME_V1_PAYLOAD_MAX_BYTES) {
        snprintf(msg, msg_size, "framer: payload_len=%u exceeds max=%d, resyncing",
                 payload_len_peek, FRAME_V1_PAYLOAD_MAX_BYTES);
        write_log_line(log_fp, "WARN", msg);
        totals->resync_count++;
        totals->bad_size++;
        totals->len_invalid++;
        rx_buf_consume(buf, 1);
        *out_event_type = "LEN_INVALID";
        return FRAMER_RESYNCED;
    }

    size_t frame_len = FRAME_V1_WIRE_HEADER_LEN + (size_t)payload_len_peek;

    if (buf->len < frame_len) {
        return FRAMER_NEED_MORE;
    }

    if (frame_v1_parse(buf->data, frame_len, out) != 0) {
        snprintf(msg, msg_size, "framer: frame_v1_parse failed, frame_len=%zu", frame_len);
        write_log_line(log_fp, "WARN", msg);
        totals->resync_count++;
        totals->bad_size++;
        rx_buf_consume(buf, 1);
        *out_event_type = "HEADER_INVALID";
        return FRAMER_RESYNCED;
    }

    if (frame_v1_validate_header(out) != 0) {
        snprintf(msg, msg_size,
                 "framer: invalid header preamble=0x%08lX version=%u header_len=%u"
                 " payload_len=%zu frame_len=%zu",
                 (unsigned long)out->header.preamble,
                 (unsigned int)out->header.version,
                 (unsigned int)out->header.header_len,
                 out->payload_len,
                 out->frame_len);
        write_log_line(log_fp, "WARN", msg);
        totals->resync_count++;
        totals->bad_header++;
        rx_buf_consume(buf, 1);
        *out_event_type = "HEADER_INVALID";
        return FRAMER_RESYNCED;
    }

    if (frame_v1_validate_crc(&out->header, out->payload, out->payload_len) != 1) {
        snprintf(msg, msg_size,
                 "framer: crc mismatch seq=%lu payload_len=%zu crc32=0x%08lX",
                 (unsigned long)out->header.seq,
                 out->payload_len,
                 (unsigned long)out->header.crc32);
        write_log_line(log_fp, "WARN", msg);
        totals->resync_count++;
        totals->bad_crc++;
        rx_buf_consume(buf, frame_len);
        *out_event_type = "CRC_FAIL";
        return FRAMER_RESYNCED;
    }

    rx_buf_consume(buf, frame_len);
    *out_event_type = "OK";
    return FRAMER_OK;
}

static void write_log_per_1sec(const RxFiles *files, RxTimingState *ts, WindowStats *win) {
    char msg[256];
    uint64_t process_cpu_now_ns = 0;
    uint64_t cpu_delta_ns = 0;
    uint64_t window_elapsed_ns = 0;

    ts->avg_latency_ns_in_1sec = win->latency_sample_cnt > 0 ? win->latency_sum_ns / win->latency_sample_cnt : 0;
    ts->elapsed_sec = (ts->next_stats_ns - ts->t_start_ns) / UINT64_C(1000000000);
    window_elapsed_ns = ts->next_stats_ns - ts->last_stats_wall_ns;
    ts->pps_in_1sec = (window_elapsed_ns > 0)
        ? ((double)win->recv_any * 1000000000.0 / (double)window_elapsed_ns)
        : 0.0;
    ts->cpu_pct_in_1sec = 0.0;
    if (now_process_cpu_ns(&process_cpu_now_ns) == 0) {
        if (process_cpu_now_ns >= ts->last_process_cpu_ns && window_elapsed_ns > 0) {
            cpu_delta_ns = process_cpu_now_ns - ts->last_process_cpu_ns;
            ts->cpu_pct_in_1sec = (double)cpu_delta_ns * 100.0 / (double)window_elapsed_ns;
        }
        ts->last_process_cpu_ns = process_cpu_now_ns;
    }
    ts->last_stats_wall_ns = ts->next_stats_ns;

    if (files->csv_in_1sec_fp) {
        snprintf(msg, sizeof(msg),
            "%llu,%.3f,%.3f,%.3f,%llu,%llu,%llu,%llu,%llu,%.2f,%.2f\n",
            (unsigned long long)ts->elapsed_sec, (double)ts->avg_latency_ns_in_1sec/1000000.0, (double)win->max_latency_ns/1000000.0,
            (double)win->min_latency_ns/1000000.0, (unsigned long long)win->recv_any, (unsigned long long)win->recv_ok,
            (unsigned long long)win->gap_cnt, (unsigned long long)win->dup_cnt, (unsigned long long)win->reord_cnt,
            ts->pps_in_1sec, ts->cpu_pct_in_1sec);
        fprintf(files->csv_in_1sec_fp, "%s", msg);
        fflush(files->csv_in_1sec_fp);
    } else {
        snprintf(msg, sizeof(msg),
            "rx_stats elapsed_sec=%llu"
            " avg_latency=%.3f"
            " max_latency=%.3f"
            " min_latency=%.3f"
            " recv_cnt=%llu ok_recv_cnt=%llu gap_cnt=%llu dup_cnt=%llu reord_cnt=%llu"
            " pps=%.2f cpu_pct=%.2f",
            (unsigned long long)ts->elapsed_sec, (double)ts->avg_latency_ns_in_1sec/1000000.0, (double)win->max_latency_ns/1000000.0,
            (double)win->min_latency_ns/1000000.0, (unsigned long long)win->recv_any, (unsigned long long)win->recv_ok,
            (unsigned long long)win->gap_cnt, (unsigned long long)win->dup_cnt, (unsigned long long)win->reord_cnt,
            ts->pps_in_1sec, ts->cpu_pct_in_1sec);
        write_log_line(files->log_fp, "INFO", msg);
    }
}

static void on_recv_ok_for_fsm(const RxFiles *files, const RxConfig *config, RxTimingState *ts, RxLinkFsm *fsm, uint64_t recv_ok_in_window) {
    if (!files || !config || !ts || !fsm) {
        return;
    }
    if (fsm->state == RX_LINK_STATE_DEGRADED) {
        if (config->recovery_mode == RX_RECOVERY_MODE_FSM) {
            transition_link_state(
                files,
                config,
                fsm,
                RX_LINK_STATE_RECOVER,
                ts->t_start_ns,
                ts->recv_now_ns,
                recv_ok_in_window,
                "recv_ok_resumed"
            );
        }
    }
}

static void evaluate_fsm_window(
    const RxFiles *files,
    const RxConfig *config,
    const RxTimingState *ts,
    const WindowStats *win,
    RxLinkFsm *fsm,
    uint64_t window_end_ns
) {
    uint64_t run_end_ns = 0;
    bool allow_degraded_transition = false;

    if (!files || !config || !ts || !win || !fsm) {
        return;
    }

    run_end_ns = ts->t_start_ns + (uint64_t)config->duration_sec * UINT64_C(1000000000);
    allow_degraded_transition = window_end_ns < run_end_ns;

    if (win->recv_ok == 0) {
        fsm->consecutive_empty_windows++;
        fsm->consecutive_good_windows = 0;

        if (fsm->state == RX_LINK_STATE_RECOVER && allow_degraded_transition) {
            transition_link_state(
                files,
                config,
                fsm,
                RX_LINK_STATE_DEGRADED,
                ts->t_start_ns,
                window_end_ns,
                win->recv_ok,
                "recovery_interrupted_by_empty_window"
            );
            return;
        }
        if (fsm->state == RX_LINK_STATE_NORMAL &&
            fsm->consecutive_empty_windows >= RX_FSM_DEGRADED_EMPTY_WINDOWS &&
            allow_degraded_transition) {
            transition_link_state(
                files,
                config,
                fsm,
                RX_LINK_STATE_DEGRADED,
                ts->t_start_ns,
                window_end_ns,
                win->recv_ok,
                "no_recv_ok_for_threshold_windows"
            );
        }
        return;
    }

    fsm->consecutive_empty_windows = 0;
    if (fsm->state == RX_LINK_STATE_RECOVER) {
        fsm->consecutive_good_windows++;
        if (fsm->consecutive_good_windows >= RX_FSM_RECOVER_GOOD_WINDOWS) {
            transition_link_state(
                files,
                config,
                fsm,
                RX_LINK_STATE_NORMAL,
                ts->t_start_ns,
                window_end_ns,
                win->recv_ok,
                "recover_completed_by_healthy_windows"
            );
        }
        return;
    }

    if (fsm->state == RX_LINK_STATE_DEGRADED &&
        config->recovery_mode == RX_RECOVERY_MODE_TIMEOUT_ONLY) {
        fsm->consecutive_good_windows++;
        if (fsm->consecutive_good_windows >= RX_FSM_RECOVER_GOOD_WINDOWS) {
            transition_link_state(
                files,
                config,
                fsm,
                RX_LINK_STATE_NORMAL,
                ts->t_start_ns,
                window_end_ns,
                win->recv_ok,
                "timeout_only_recovered_by_healthy_windows"
            );
        }
        return;
    }

    fsm->consecutive_good_windows = 0;
}

static int run_crc32_test_mode(void) {
    FrameV1Header frame = {0};
    uint8_t frame_bytes[FRAME_V1_MAX_WIRE_BYTES] = {0};
    size_t frame_len = 0;

    if (frame_v1_build_crc32_test_frame(&frame, frame_bytes, sizeof(frame_bytes), &frame_len) != 0) {
        fprintf(stderr, "frame_v1_build_crc32_test_frame failed\n");
        return 1;
    }

    printf("crc32 test mode\n");
    printf("payload_len=%zu seq=0x%08lX tx_ts=0x%016llX\n",
           (size_t)frame.payload_len, (unsigned long)frame.seq, (unsigned long long)frame.tx_ts);
    printf("crc32=0x%08lX frame_len=%zu\n", (unsigned long)frame.crc32, frame_len);
    return 0;
}

int main(int argc, char **argv) {

    RxConfig cfg = {0};
    RxFiles files = {0};
    RxTotals totals = {0};
    RxTimingState ts = {0};
    SeqState seq_state = {0};
    RxLinkFsm link_fsm = {
        .state = RX_LINK_STATE_NORMAL,
    };
    WindowStats *win = NULL;

    cfg.bind_ip = "0.0.0.0";
    cfg.link_name = "unknown";
    cfg.trial = 0;

    if (parse_args(argc, argv, &cfg) != 0) {
        return 1;
    }

    if (cfg.crc32_test_mode) {
        return run_crc32_test_mode();
    }

    totals.collect_latency_samples = cfg.has_link_name && cfg.has_trial;

    if (open_output_files(&cfg, &files) != 0) {
        return 1;
    }

    if (install_signal_handlers() != 0) {
        perror("sigaction");
        close_output_files(&files);
        return 1;
    }

    char buf[256];

    if (files.log_fp) {
        snprintf(buf, sizeof(buf),
                 "frame_v1 config version=%u header_len=%u payload_max=%d frame_max=%d"
                 " stream_buf_cap=%d",
                 kFrameV1Version,
                 (unsigned)FRAME_V1_WIRE_HEADER_LEN,
                 FRAME_V1_PAYLOAD_MAX_BYTES,
                 FRAME_V1_MAX_WIRE_BYTES,
                 RX_STREAM_BUF_CAP);
        write_log_line(files.log_fp, "INFO", buf);
        snprintf(buf, sizeof(buf),
                "rx start bind=%s:%d duration_sec=%d",
                cfg.bind_ip, cfg.port, cfg.duration_sec);
        write_log_line(files.log_fp, "INFO", buf);
        snprintf(buf, sizeof(buf),
                 "rx recovery_mode=%s",
                 (cfg.recovery_mode == RX_RECOVERY_MODE_TIMEOUT_ONLY) ? "timeout-only" : "fsm");
        write_log_line(files.log_fp, "INFO", buf);
        write_fsm_threshold_log(&files, cfg.recovery_mode, link_fsm.state);
    }

    printf("rx started: bind=%s:%d duration=%d log=%s\n", cfg.bind_ip, cfg.port, cfg.duration_sec, cfg.log_path);
    if (files.csv_in_1sec_fp) printf("csv_in_1sec_log_path=%s\n", cfg.csv_in_1sec_log_path);
    if (files.csv_by_1recv_fp) printf("csv_by_1recv_log_path=%s\n", cfg.csv_by_1recv_log_path);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        close_output_files(&files);
        return 1;
    }

    if (cfg.rcvbuf_set) {
        if (apply_socket_buffer_setting(files.log_fp, sock, SO_RCVBUF, "SO_RCVBUF", cfg.rcvbuf) != 0) {
            close(sock);
            close_output_files(&files);
            return 1;
        }
    }

    struct pollfd pfd;
    pfd.fd = sock;
    pfd.events = POLLIN;  // 読み取り可能イベントを待つ
    pfd.revents = 0;

    struct sockaddr_in bind_addr = {0};
    if (build_bind_addr(cfg.bind_ip, cfg.port, &bind_addr) != 0) {
        close(sock);
        close_output_files(&files);
        return 1;
    }

    if (bind(sock, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) != 0) {
        perror("bind");
        close(sock);
        close_output_files(&files);
        return 1;
    }

    FrameV1Parsed parsed = {0};
    RxStreamBuf stream_buf = {0};
    uint8_t buf_udp[RX_STREAM_BUF_CAP];

    char msg[256];
    ssize_t n = 0;
    struct sockaddr_in src_addr;

    if (now_monotonic_ns(&ts.t_start_ns) != 0) {
        write_log_line(files.log_fp, "ERROR", "clock_gettime failed");
        close(sock);
        close_output_files(&files);
        return 1;
    }

    ts.next_stats_ns = ts.t_start_ns + 1000000000ULL;
    ts.last_stats_wall_ns = ts.t_start_ns;
    if (now_process_cpu_ns(&ts.last_process_cpu_ns) != 0) {
        ts.last_process_cpu_ns = 0;
    }

    while (1) {
        if (g_stop_requested) {
            write_log_line(files.log_fp, "INFO", "stop requested by signal");
            break;
        }

        if (now_monotonic_ns(&ts.now_ns) != 0) {
            write_log_line(files.log_fp, "ERROR", "clock_gettime failed");
            break;
        }
        if (ts.now_ns - ts.t_start_ns >= (uint64_t)cfg.duration_sec * 1000000000ULL) {
            write_log_line(files.log_fp, "INFO", "duration elapsed, exiting");
            break;
        }

        if (ts.next_stats_ns > ts.now_ns) {
            ts.wait_ms = (int)((ts.next_stats_ns - ts.now_ns + 999999ULL) / 1000000ULL);
        } else {
            ts.wait_ms = 0;
        }
        int ret = poll(&pfd, 1, ts.wait_ms);

        if (ret < 0) {
            if (errno == EINTR) {
                if (g_stop_requested) {
                    write_log_line(files.log_fp, "INFO", "poll interrupted by signal");
                    break;
                }
                continue;
            }
            perror("poll");
            break;
        } else if (ret == 0) {
            totals.poll_timeout++;
        } else if (pfd.revents & (POLLERR | POLLNVAL)) {
            fprintf(stderr, "poll error revents=0x%x\n", pfd.revents);
            break;
        } else if (pfd.revents & POLLIN) {
            socklen_t src_len = sizeof(src_addr);
            n = recvfrom(sock, buf_udp, sizeof(buf_udp), 0, (struct sockaddr *)&src_addr, &src_len);

            if (n < 0) {
                if (errno == EINTR) {
                    if (g_stop_requested) {
                        write_log_line(files.log_fp, "INFO", "recvfrom interrupted by signal");
                        break;
                    }
                    continue;
                }
                perror("recvfrom");
                break;
            }

            if (now_monotonic_ns(&ts.recv_now_ns) != 0) {
                write_log_line(files.log_fp, "ERROR", "clock_gettime failed");
                break;
            }
            totals.recv_any++;

            win = select_window_stats(&ts);
            win->recv_any++;

            if (rx_buf_append(&stream_buf, buf_udp, (size_t)n) != 0) {
                snprintf(msg, sizeof(msg),
                         "stream_buf overflow: recv_len=%zd buf_len=%zu cap=%d, clearing",
                         n, stream_buf.len, RX_STREAM_BUF_CAP);
                write_log_line(files.log_fp, "WARN", msg);
                stream_buf.len = 0;
                totals.resync_count++;
                totals.bad_size++;
            }

            const char *event_type = NULL;
            for (;;) {
                FramerResult fr = rx_framer_step(
                    &stream_buf,
                    &parsed,
                    &totals,
                    files.log_fp,
                    msg,
                    sizeof(msg),
                    &event_type
                );

                if (fr == FRAMER_NEED_MORE) {
                    break;
                }
                if (fr == FRAMER_RESYNCED) {
                    write_fault_csv(&files, ts.recv_now_ns, event_type);
                    continue;
                }

                update_seq_stats(parsed.header.seq, &seq_state, &totals, &ts, win);
                update_latency_stats(parsed.header.tx_ts, &totals, &ts, win);
                write_per_recv_csv(&files, &ts, parsed.header.seq, parsed.header.tx_ts);

                totals.recv_ok++;
                win->recv_ok++;
                on_recv_ok_for_fsm(&files, &cfg, &ts, &link_fsm, win->recv_ok);
            }
        }

        if (now_monotonic_ns(&ts.now_for_stats_ns) != 0) {
            write_log_line(files.log_fp, "ERROR", "clock_gettime failed");
            break;
        }
        while (ts.now_for_stats_ns >= ts.next_stats_ns) {
            ts.cur_idx = ts.win_idx % 2;
            evaluate_fsm_window(&files, &cfg, &ts, &ts.win_stats[ts.cur_idx], &link_fsm, ts.next_stats_ns);
            write_log_per_1sec(&files, &ts, &ts.win_stats[ts.cur_idx]);

            ts.next_stats_ns += 1000000000ULL;
            ts.win_stats[ts.cur_idx] = (WindowStats){0};
            ts.win_idx++;
        }
    }

    uint64_t elapsed_ns = 0;
    if (now_monotonic_ns(&elapsed_ns) == 0 && elapsed_ns >= ts.t_start_ns) {
        elapsed_ns -= ts.t_start_ns;
    } else {
        elapsed_ns = 0;
    }

    if (files.log_fp) {
        write_summary(&files, &totals, elapsed_ns);
        write_trial_summary(&files, &cfg, &totals);
        write_log_line(files.log_fp, "INFO", "rx end");
    }

    close_output_files(&files);
    close(sock);
    free(totals.latency_samples_ns);

    printf("rx finished\n");
    return 0;
}

static int now_process_cpu_ns(uint64_t *out_ns) {
    struct timespec ts;
    if (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts) != 0) {
        return -1;
    }
    *out_ns = (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
    return 0;
}
