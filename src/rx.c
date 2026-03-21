// src/rx.c
//
// 役割
//   - UDP受信プログラム（rx）のエントリポイント
//   - CLI引数の解析（bind-ip / port / duration-sec / log-path）
//   - poll ベースの受信ループ
//   - FrameV0 サイズ確認と最小統計の算出（latency平均 / seq差分ベース欠損推定 / 重複 / 逆順）
//   - ログ出力（start / summary / end）
//
// このファイルが担当すること
//   - UDPソケット生成 / bind / 受信待機 / recvfrom
//   - 実行時間管理（duration_sec）
//   - 受信イベント / タイムアウト / シグナル割込みの処理
//   - FrameV0 を前提にした最小統計の集計と summary ログ出力
//
// このファイルが担当しないこと（別段階/別責務）
//   - Frame内容の高度な検証（magic/version/checksum 等）
//   - 高度な統計（P95/P99, ヒストグラム, ジッタ詳細）
//   - 可視化 / オフライン集計
//
// 計測の前提と限界（重要）
//   - latency = recv_now(CLOCK_MONOTONIC) - frame.timestamp_ns
//   - このlatencyは同一マシン/同一クロック系である前提で意味を持つ
//   - UDPは順序保証がないため、seq差分ベースの欠損は「推定値」
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
#include <inttypes.h>
#include <signal.h>
#include <stdbool.h>

#include "frame.h"
#include "frame_v1_wire.h"

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
// 受信側の設定をまとめる構造体
//
// bind_ip をポインタにしている理由は tx.c と同じ。
// CLI引数文字列（argv内）を読み取り専用で参照するだけなのでコピー不要。
typedef struct {
    const char *bind_ip;   // bind先IP（例: "127.0.0.1" / "0.0.0.0"）
    int port;              // bindポート
    int duration_sec;       // 実行時間（受信ループの終了条件）
    const char *log_path;  // ログファイルパス
    const char *csv_in_1sec_log_path;  // １秒ごとの統計ログ（rx_stats）をCSV形式で出力する場合のファイルパス（オプション、未指定ならCSV出力しない）
    const char *csv_by_1recv_log_path;  // 受信ごとの統計ログ（rx_stats）をCSV形式で出力する場合のファイルパス（オプション、未指定ならCSV出力しない）
    int crc32_test_mode;  // ハードコードした v1 フレームで CRC32 を確認する
} RxConfig;

typedef struct {
    FILE *log_fp;
    FILE *csv_in_1sec_fp;
    FILE *csv_by_1recv_fp;
} RxFiles;

typedef struct {
    uint64_t recv_any;
    uint64_t recv_ok;
    uint64_t bad_size;
    uint64_t bad_header;
    uint64_t bad_crc;
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
    uint64_t gap;
    uint64_t latency;
    int wait_ms;
    int win_idx;
    int target_idx;
    int cur_idx;
    WindowStats win_stats[2];
} RxTimingState;

typedef enum {
    RX_FRAME_OK = 0,
    RX_FRAME_BAD_SIZE = 1,
    RX_FRAME_BAD_HEADER = 2,
    RX_FRAME_BAD_CRC = 3
} RxFrameStatus;




static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s --bind-ip <ip> --port <port> --duration-sec <sec> --log-path <path> [--csv-in-1sec-log-path <path>] [--csv-by-1recv-log-path <path>] [--crc32-test]\n",
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

static int parse_args(int argc, char **argv, RxConfig *cfg) {
    int opt;
    int option_index = 0;

    static struct option long_opts[] = {
        {"bind-ip", required_argument, 0, 1},
        {"port", required_argument, 0, 2},
        {"duration-sec", required_argument, 0, 3},
        {"log-path", required_argument, 0, 4},
        {"csv-in-1sec-log-path", required_argument, 0, 5},
        {"csv-by-1recv-log-path", required_argument, 0, 6},
        {"crc32-test", no_argument, 0, 7},
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
                cfg->csv_in_1sec_log_path = optarg;
                break;

            case 6:
                cfg->csv_by_1recv_log_path = optarg;
                break;
            case 7:
                cfg->crc32_test_mode = 1;
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
        fprintf(files->csv_in_1sec_fp, "elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt\n");
        fflush(files->csv_in_1sec_fp);
    }

    if (config->csv_by_1recv_log_path) {
        files->csv_by_1recv_fp = fopen(config->csv_by_1recv_log_path, "w");
        if (!files->csv_by_1recv_fp) {
            perror("fopen(csv_by_1recv_log_path)");
            close_output_files(files);
            return -1;
        }
        fprintf(files->csv_by_1recv_fp, "rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta\n");
        fflush(files->csv_by_1recv_fp);
    }

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

static void write_summary(const RxFiles *files, const RxTotals *totals, uint64_t elapsed_ns) {
    char msg[512];

    if (!files || !files->log_fp || !totals) {
        return;
    }

    snprintf(
        msg,
        sizeof(msg),
        "rx summary recv_any=%" PRIu64 " recv_ok=%" PRIu64
        " bad_size=%" PRIu64 " bad_header=%" PRIu64 " bad_crc=%" PRIu64 " poll_timeout=%" PRIu64
        " elapsed_ms=%" PRIu64 " avg_latency_ms=%.3f"
        " max_latency_ms=%" PRIu64 " min_latency_ms=%" PRIu64
        " gap_cnt=%" PRIu64 " dup_cnt=%" PRIu64 " reord_cnt=%" PRIu64
        " future_ts_cnt=%" PRIu64 " future_ts_detected=%" PRIu64,
        totals->recv_any,
        totals->recv_ok,
        totals->bad_size,
        totals->bad_header,
        totals->bad_crc,
        totals->poll_timeout,
        elapsed_ns / UINT64_C(1000000),
        (totals->latency_sample_cnt > 0)
            ? (double)totals->latency_sum_ns / (double)totals->latency_sample_cnt / 1000000.0
            : 0.0,
        totals->max_latency_ns / UINT64_C(1000000),
        totals->min_latency_ns / UINT64_C(1000000),
        totals->gap_cnt,
        totals->dup_cnt,
        totals->reord_cnt,
        totals->future_ts_cnt,
        totals->future_ts_detected
    );

    write_log_line(files->log_fp, "INFO", msg);
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
            "%" PRIu64 ",%" PRIu32 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 "\n",
            ts->recv_now_ns, seq_value, tx_ts_ns, ts->latency, ts->gap
            );
        fprintf(files->csv_by_1recv_fp, "%s", msg_csv_by_1recv);
    }
}

static void log_bad_frame_size(FILE *log_fp, char *msg, size_t msg_size, ssize_t recv_len) {
    snprintf(msg, msg_size, "invalid frame size: %zd", recv_len);
    write_log_line(log_fp, "WARN", msg);
}

static void log_bad_frame_header(FILE *log_fp, char *msg, size_t msg_size, const FrameV1Parsed *parsed) {
    snprintf(msg, msg_size,
             "invalid frame header: preamble=0x%08" PRIX32 " version=%u header_len=%u payload_len=%zu frame_len=%zu",
             parsed->header.preamble,
             parsed->header.version,
             parsed->header.header_len,
             parsed->payload_len,
             parsed->frame_len);
    write_log_line(log_fp, "WARN", msg);
}

static void log_bad_frame_crc(FILE *log_fp, char *msg, size_t msg_size, const FrameV1Parsed *parsed) {
    snprintf(msg, msg_size,
             "crc mismatch: seq=%" PRIu32 " payload_len=%zu crc32=0x%08" PRIX32,
             parsed->header.seq,
             parsed->payload_len,
             parsed->header.crc32);
    write_log_line(log_fp, "WARN", msg);
}

static RxFrameStatus validate_received_frame(const uint8_t *buf_udp, size_t recv_len, FrameV1Parsed *parsed) {
    if (frame_v1_parse(buf_udp, recv_len, parsed) != 0) {
        return RX_FRAME_BAD_SIZE;
    }
    if (frame_v1_validate_header(parsed) != 0) {
        return RX_FRAME_BAD_HEADER;
    }
    if (frame_v1_validate_crc(&parsed->header, parsed->payload, parsed->payload_len) != 1) {
        return RX_FRAME_BAD_CRC;
    }

    return RX_FRAME_OK;
}

static int handle_received_frame(
    const uint8_t *buf_udp,
    size_t recv_len,
    FrameV1Parsed *parsed,
    RxTotals *totals,
    char *msg,
    size_t msg_size,
    FILE *log_fp
) {
    RxFrameStatus status = validate_received_frame(buf_udp, recv_len, parsed);

    switch (status) {
        case RX_FRAME_OK:
            return 0;
        case RX_FRAME_BAD_SIZE:
            totals->bad_size++;
            log_bad_frame_size(log_fp, msg, msg_size, (ssize_t)recv_len);
            return -1;
        case RX_FRAME_BAD_HEADER:
            totals->bad_header++;
            log_bad_frame_header(log_fp, msg, msg_size, parsed);
            return -1;
        case RX_FRAME_BAD_CRC:
            totals->bad_crc++;
            log_bad_frame_crc(log_fp, msg, msg_size, parsed);
            return -1;
    }

    return -1;
}

static void write_log_per_1sec(const RxFiles *files, RxTimingState *ts, WindowStats *win) {
    char msg[256];

    ts->avg_latency_ns_in_1sec = win->latency_sample_cnt > 0 ? win->latency_sum_ns / win->latency_sample_cnt : 0;
    ts->elapsed_sec = (ts->next_stats_ns - ts->t_start_ns) / UINT64_C(1000000000);
    if (files->csv_in_1sec_fp) {
        snprintf(msg, sizeof(msg),
            "%" PRIu64 ",%.3f,%.3f,%.3f,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 "\n",
            ts->elapsed_sec, (double)ts->avg_latency_ns_in_1sec/1000000.0, (double)win->max_latency_ns/1000000.0, 
            (double)win->min_latency_ns/1000000.0, win->recv_any, win->recv_ok, win->gap_cnt, win->dup_cnt, win->reord_cnt);
        fprintf(files->csv_in_1sec_fp, "%s", msg);
    } else {
        snprintf(msg, sizeof(msg),
            "rx_stats elapsed_sec=%" PRIu64 
            " avg_latency=%.3f"  
            " max_latency=%.3f" 
            " min_latency=%.3f" 
            " recv_cnt=%" PRIu64 " ok_recv_cnt=%" PRIu64 " gap_cnt=%" PRIu64 " dup_cnt=%" PRIu64 " reord_cnt=%" PRIu64,
            ts->elapsed_sec, (double)ts->avg_latency_ns_in_1sec/1000000.0, (double)win->max_latency_ns/1000000.0, 
            (double)win->min_latency_ns/1000000.0, win->recv_any, win->recv_ok, win->gap_cnt, win->dup_cnt, win->reord_cnt);
        write_log_line(files->log_fp, "INFO", msg);
    }

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
    printf("payload_len=%zu seq=0x%08" PRIX32 " tx_ts=0x%016" PRIX64 "\n",
           (size_t)frame.payload_len, frame.seq, frame.tx_ts);
    printf("crc32=0x%08" PRIX32 " frame_len=%zu\n", frame.crc32, frame_len);
    return 0;
}

int main(int argc, char **argv) {

    RxConfig cfg = {0};
    RxFiles files = {0};
    RxTotals totals = {0};
    RxTimingState ts = {0};
    SeqState seq_state = {0};
    WindowStats *win = NULL;

    // rx は bind-ip を省略可能にしておく（利便性のため）
    // 将来、ローカル検証時は 127.0.0.1、複数NIC環境では 0.0.0.0 と使い分けられる
    cfg.bind_ip = "0.0.0.0";

    if (parse_args(argc, argv, &cfg) != 0) {
        return 1;
    }

    if (cfg.crc32_test_mode) {
        return run_crc32_test_mode();
    }

    if (open_output_files(&cfg, &files) != 0) {
        return 1;
    }

    if (install_signal_handlers() != 0) {
        perror("sigaction");
        close_output_files(&files);
        return 1;
    }

    char buf[256];

    // v1 wire 設定が見えていることを、起動時ログで確認できるようにする
    if (files.log_fp) {
        snprintf(buf, sizeof(buf),
                 "frame_v1 config version=%u header_len=%u payload_max=%d frame_max=%d",
                 kFrameV1Version,
                 (unsigned)FRAME_V1_WIRE_HEADER_LEN,
                 FRAME_V1_PAYLOAD_MAX_BYTES,
                 FRAME_V1_MAX_WIRE_BYTES);
        write_log_line(files.log_fp, "INFO", buf);
        snprintf(buf, sizeof(buf),
                "rx start bind=%s:%d duration_sec=%d",
                cfg.bind_ip, cfg.port, cfg.duration_sec);
        write_log_line(files.log_fp, "INFO", buf);
    }

    printf("rx started: bind=%s:%d duration=%d log=%s\n", cfg.bind_ip, cfg.port, cfg.duration_sec, cfg.log_path);
    if (files.csv_in_1sec_fp) printf("csv_in_1sec_log_path=%s\n", cfg.csv_in_1sec_log_path);
    if (files.csv_by_1recv_fp) printf("csv_by_1recv_log_path=%s\n", cfg.csv_by_1recv_log_path);
    
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        close_output_files(&files);
        return 1;  // または exit(EXIT_FAILURE);
    }

    struct pollfd pfd;
    pfd.fd = sock;
    pfd.events = POLLIN;  // 読み取り可能イベントを待つ
    pfd.revents = 0; // 見やすさのため初期化（必須ではない）

    struct sockaddr_in bind_addr={0};
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


    // 起動ログを書き込む
    FrameV1Parsed parsed = {0};
    uint8_t buf_udp[FRAME_V1_MAX_WIRE_BYTES];

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
        }else if (ret == 0) {
            totals.poll_timeout++;
        } 
        else if (pfd.revents & (POLLERR | POLLNVAL)) {
            fprintf(stderr, "poll error revents=0x%x\n", pfd.revents);
            break;
        }
        else if ( pfd.revents & POLLIN) {
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
            if (handle_received_frame(
                buf_udp,
                (size_t)n,
                &parsed,
                &totals,
                msg,
                sizeof(msg),
                files.log_fp
            ) != 0) {
                continue;
            }

            update_seq_stats(parsed.header.seq, &seq_state, &totals, &ts, win);
            update_latency_stats(parsed.header.tx_ts, &totals, &ts, win);
            write_per_recv_csv(&files, &ts, parsed.header.seq, parsed.header.tx_ts);

            totals.recv_ok++;
            win->recv_ok++;

        }
        if (now_monotonic_ns(&ts.now_for_stats_ns) != 0) {
            write_log_line(files.log_fp, "ERROR", "clock_gettime failed");
            break;
        }
        while (ts.now_for_stats_ns >= ts.next_stats_ns ) {
            ts.cur_idx = ts.win_idx % 2;
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
        write_log_line(files.log_fp, "INFO", "rx end");
    }
    
    close_output_files(&files);
    close(sock);

    printf("rx finished\n");
    return 0;
}
