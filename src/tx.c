// src/tx.c
//
// 役割
//   - UDP送信プログラム（tx）のエントリポイント
//   - CLI引数の解析（dst-ip / dst-port / rate-hz / duration-sec / log-path / sndbuf）
//   - CLOCK_MONOTONIC ベースの固定レート送信ループ
//   - Frame v1 を手動 serialize して UDP送信
//   - ログ出力（start / summary / end）
//
// このファイルが担当すること
//   - UDPソケット生成 / 宛先アドレス構築 / sendto
//   - 実行時間管理（duration_sec）
//   - rate_hz に基づく送信周期の計算と送信ループ
//   - 最小統計の集計と summary ログ出力
//
// このファイルが担当しないこと（別段階/別責務）
//   - 再送制御 / ACK 処理
//   - 輻輳制御 / レート適応
//   - 高度な送信統計 / 可視化
//
// 計測の前提と限界（重要）
//   - tx_ts は CLOCK_MONOTONIC の送信時刻
//   - avg_rate_hz は elapsed_ns に対する実測平均
//   - sendto の成功は受信側への到達保証を意味しない
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
#include <stdint.h>
#include <stddef.h>
#include <inttypes.h>

#include "frame_v1_wire.h"
#include "feedback_v1_wire.h"
#include "fec_v1_wire.h"

// 1 UDP datagram に連結して送信する frame 数
#define TX_FRAMES_PER_DATAGRAM 3
#define TX_MAX_DATA_DATAGRAM_BYTES (TX_FRAMES_PER_DATAGRAM * FRAME_V1_MAX_WIRE_BYTES)
#define TX_MAX_FEC_DATAGRAM_BYTES (FEC_V1_HEADER_LEN + TX_MAX_DATA_DATAGRAM_BYTES)

// 故障注入の対象フィールド
typedef enum {
    FAULT_NONE        = 0,
    FAULT_PREAMBLE    = 1,  // preamble (bytes 0-3) の任意 1bit を反転 → PREAMBLE_MISS
    FAULT_PAYLOAD_LEN = 2,  // payload_len を上限超えの値に書き換え → LEN_INVALID
    FAULT_CRC         = 3,  // crc32 フィールド (bytes 21-24) の任意 1bit を反転 → CRC_FAIL
    FAULT_PAYLOAD     = 4,  // payload の任意 1bit を反転 → CRC_FAIL
    FAULT_HEADER      = 5,  // version または header_len を不正値に書き換え → HEADER_INVALID
} FaultTarget;

typedef struct {
    const char *dst_ip;         // 送信先IP（例: "127.0.0.1"）
    int dst_port;               // 送信先ポート
    int rate_hz;                // 送信レート（Hz）
    int duration_sec;           // 実行時間
    const char *log_path;       // ログファイルパス
    int sndbuf;                 // SO_SNDBUF に設定する送信バッファサイズ（byte）
    int sndbuf_set;             // --sndbuf が明示指定されたか
    int payload_len;            // 送信する payload 長（byte）
    int version;                // プロトコルバージョン（現状は v1 固定）
    int crc32_test_mode;        // ハードコードした v1 フレームで CRC32 を確認する
    FaultTarget fault_target;   // 故障注入の対象フィールド（FAULT_NONE = 無効）
    float fault_rate;           // 故障注入確率（0.0〜1.0）
    int outage_at_sec;          // 単発瞬断の開始時刻（tx 開始からの相対秒）
    int outage_duration_ms;     // 単発瞬断の継続時間（ms）
    int outage_at_sec_set;
    int outage_duration_ms_set;
    int outage_enabled;
    const char *feedback_bind_ip;
    int feedback_bind_port;
    int feedback_enabled;
    const char *adaptive_log_path;
    int adaptive_enabled;
    int adaptive_min_rate_hz;
    int adaptive_max_rate_hz;
    int adaptive_debug_set_rate_hz;
    double adaptive_high_latency_ms;
    int retransmit_enabled;
    int retransmit_buffer_datagrams;
    int retransmit_max_datagrams_per_feedback;
    int fec_enabled;
    int fec_k;
    int fec_r;
    int drop_datagram_every;
} TxConfig;

typedef struct {
    FILE *log_fp;
    FILE *adaptive_log_fp;
} TxFiles;

typedef struct {
    uint32_t seq;
    uint32_t sent;
    uint64_t retransmit_requested_frames;
    uint64_t retransmit_sent_datagrams;
    uint64_t retransmit_sent_frames;
    uint64_t retransmit_buffer_miss_count;
    uint64_t fec_data_datagrams;
    uint64_t fec_parity_datagrams;
    uint64_t dropped_datagrams;
} TxTotals;

typedef struct {
    uint32_t start_seq;
    uint32_t frame_count;
    size_t len;
    int valid;
    uint8_t bytes[TX_MAX_DATA_DATAGRAM_BYTES];
} TxStoredDatagram;

typedef struct {
    TxStoredDatagram *items;
    size_t cap;
    size_t next;
} TxRetransmitBuffer;

typedef struct {
    struct timespec next_send;  // 次回送信予定時刻（絶対時刻, CLOCK_MONOTONIC）
    uint64_t period_ns;         // 基本送信周期 = 1_000_000_000 / rate_hz（端数切り捨て）
                                // ループ内では remainder 補正後の this_period を使う
    uint64_t t_start_ns;
    uint64_t now_ns;
    uint64_t tx_ts_ns;
    uint64_t next_stats_ns;
    uint64_t last_stats_wall_ns;
    uint64_t last_process_cpu_ns;
    uint32_t last_sent_datagrams;
    uint32_t last_sent_frames;
} TxTimingState;

typedef struct {
    int current_rate_hz;
    int min_rate_hz;
    int max_rate_hz;
    uint64_t period_ns;
    uint64_t period_remainder;
    uint64_t remainder_acc;
    int stable_windows;
} TxRateState;

typedef struct {
    uint64_t start_ns_from_t0;
    uint64_t end_ns_from_t0;
    uint64_t duration_ns;
    int active;
    int logged_start;
    int logged_end;
} TxOutageState;

static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s --dst-ip <ip> --dst-port <port> --rate-hz <hz> --duration-sec <sec>"
            " --log-path <path> [--sndbuf <bytes>] [--payload-len <n>] [--version <n>] [--crc32-test]"
            " [--fault-target preamble|payload_len|crc|payload|header] [--fault-rate 0.0-1.0]"
            " [--outage-at-sec <sec> --outage-duration-ms <ms>]"
            " [--feedback-bind-ip <ip> --feedback-bind-port <port> --adaptive-log-path <path>]"
            " [--adaptive-mode off|on] [--adaptive-min-rate-hz <hz>] [--adaptive-max-rate-hz <hz>]"
            " [--adaptive-high-latency-ms <ms>] [--adaptive-debug-set-rate-hz <hz>]"
            " [--retransmit-mode off|on] [--retransmit-buffer-datagrams <n>] [--retransmit-max-datagrams-per-feedback <n>]"
            " [--fec-mode off|xor] [--fec-k 4] [--fec-r 1] [--drop-datagram-every <n>]\n",
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

static int parse_float(const char *s, float *out) {
    char *end = NULL;
    errno = 0;
    double v = strtod(s, &end);
    if (errno != 0 || end == s || *end != '\0') return -1;
    if (v < 0.0 || v > 1.0) return -1;
    *out = (float)v;
    return 0;
}

static int parse_nonnegative_double(const char *s, double *out) {
    char *end = NULL;
    errno = 0;
    double v = strtod(s, &end);
    if (errno != 0 || end == s || *end != '\0') return -1;
    if (v < 0.0) return -1;
    *out = v;
    return 0;
}

static int parse_args(int argc, char **argv, TxConfig *cfg) {
    int opt;
    int option_index = 0;

    cfg->version = (int)kFrameV1Version;
    cfg->payload_len = FRAME_V0_PAYLOAD_BYTES;
    cfg->adaptive_min_rate_hz = 1;
    cfg->adaptive_max_rate_hz = 1000000;
    cfg->adaptive_high_latency_ms = 0.0;
    cfg->retransmit_buffer_datagrams = 4096;
    cfg->retransmit_max_datagrams_per_feedback = 256;
    cfg->fec_k = FEC_V1_K_FIXED;
    cfg->fec_r = FEC_V1_R_FIXED;

    static struct option long_opts[] = {
        {"dst-ip", required_argument, 0, 1},
        {"dst-port", required_argument, 0, 2},
        {"rate-hz", required_argument, 0, 3},
        {"duration-sec", required_argument, 0, 4},
        {"log-path", required_argument, 0, 5},
        {"version", required_argument, 0, 6},
        {"crc32-test",    no_argument,       0, 7},
        {"payload-len",   required_argument, 0, 8},
        {"fault-target",  required_argument, 0, 9},
        {"fault-rate",    required_argument, 0, 10},
        {"outage-at-sec", required_argument, 0, 11},
        {"outage-duration-ms", required_argument, 0, 12},
        {"sndbuf",        required_argument, 0, 13},
        {"feedback-bind-ip", required_argument, 0, 14},
        {"feedback-bind-port", required_argument, 0, 15},
        {"adaptive-log-path", required_argument, 0, 16},
        {"adaptive-mode", required_argument, 0, 17},
        {"adaptive-min-rate-hz", required_argument, 0, 18},
        {"adaptive-max-rate-hz", required_argument, 0, 19},
        {"adaptive-debug-set-rate-hz", required_argument, 0, 20},
        {"adaptive-high-latency-ms", required_argument, 0, 21},
        {"retransmit-mode", required_argument, 0, 22},
        {"retransmit-buffer-datagrams", required_argument, 0, 23},
        {"retransmit-max-datagrams-per-feedback", required_argument, 0, 24},
        {"fec-mode", required_argument, 0, 25},
        {"fec-k", required_argument, 0, 26},
        {"fec-r", required_argument, 0, 27},
        {"drop-datagram-every", required_argument, 0, 28},
        {0, 0, 0, 0}
    };

    while ((opt = getopt_long(argc, argv, "", long_opts, &option_index)) != -1) {
        switch (opt) {
            case 1:
                cfg->dst_ip = optarg;
                break;

            case 2:
                if (parse_int(optarg, &cfg->dst_port) != 0) {
                    fprintf(stderr, "Invalid --dst-port: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;

            case 3:
                if (parse_int(optarg, &cfg->rate_hz) != 0) {
                    fprintf(stderr, "Invalid --rate-hz: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;

            case 4:
                if (parse_int(optarg, &cfg->duration_sec) != 0) {
                    fprintf(stderr, "Invalid --duration-sec: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;

            case 5:
                cfg->log_path = optarg;
                break;
            case 6:
                if (parse_int(optarg, &cfg->version) != 0) {
                    fprintf(stderr, "Invalid --version: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 7:
                cfg->crc32_test_mode = 1;
                break;
            case 8:
                if (parse_int(optarg, &cfg->payload_len) != 0) {
                    fprintf(stderr, "Invalid --payload-len: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 9:
                if (strcmp(optarg, "preamble") == 0) {
                    cfg->fault_target = FAULT_PREAMBLE;
                } else if (strcmp(optarg, "payload_len") == 0) {
                    cfg->fault_target = FAULT_PAYLOAD_LEN;
                } else if (strcmp(optarg, "crc") == 0) {
                    cfg->fault_target = FAULT_CRC;
                } else if (strcmp(optarg, "payload") == 0) {
                    cfg->fault_target = FAULT_PAYLOAD;
                } else if (strcmp(optarg, "header") == 0) {
                    cfg->fault_target = FAULT_HEADER;
                } else {
                    fprintf(stderr, "Invalid --fault-target: %s (expected preamble|payload_len|crc|payload|header)\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 10:
                if (parse_float(optarg, &cfg->fault_rate) != 0) {
                    fprintf(stderr, "Invalid --fault-rate: %s (expected 0.0-1.0)\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 11:
                if (parse_int(optarg, &cfg->outage_at_sec) != 0) {
                    fprintf(stderr, "Invalid --outage-at-sec: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                cfg->outage_at_sec_set = 1;
                break;
            case 12:
                if (parse_int(optarg, &cfg->outage_duration_ms) != 0) {
                    fprintf(stderr, "Invalid --outage-duration-ms: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                cfg->outage_duration_ms_set = 1;
                break;
            case 13:
                if (parse_int(optarg, &cfg->sndbuf) != 0) {
                    fprintf(stderr, "Invalid --sndbuf: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                cfg->sndbuf_set = 1;
                break;
            case 14:
                cfg->feedback_bind_ip = optarg;
                break;
            case 15:
                if (parse_int(optarg, &cfg->feedback_bind_port) != 0) {
                    fprintf(stderr, "Invalid --feedback-bind-port: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 16:
                cfg->adaptive_log_path = optarg;
                break;
            case 17:
                if (strcmp(optarg, "off") == 0) {
                    cfg->adaptive_enabled = 0;
                } else if (strcmp(optarg, "on") == 0) {
                    cfg->adaptive_enabled = 1;
                } else {
                    fprintf(stderr, "Invalid --adaptive-mode: %s (expected off|on)\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 18:
                if (parse_int(optarg, &cfg->adaptive_min_rate_hz) != 0) {
                    fprintf(stderr, "Invalid --adaptive-min-rate-hz: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 19:
                if (parse_int(optarg, &cfg->adaptive_max_rate_hz) != 0) {
                    fprintf(stderr, "Invalid --adaptive-max-rate-hz: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 20:
                if (parse_int(optarg, &cfg->adaptive_debug_set_rate_hz) != 0) {
                    fprintf(stderr, "Invalid --adaptive-debug-set-rate-hz: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 21:
                if (parse_nonnegative_double(optarg, &cfg->adaptive_high_latency_ms) != 0) {
                    fprintf(stderr, "Invalid --adaptive-high-latency-ms: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 22:
                if (strcmp(optarg, "on") == 0) {
                    cfg->retransmit_enabled = 1;
                } else if (strcmp(optarg, "off") == 0) {
                    cfg->retransmit_enabled = 0;
                } else {
                    fprintf(stderr, "Invalid --retransmit-mode: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 23:
                if (parse_int(optarg, &cfg->retransmit_buffer_datagrams) != 0) {
                    fprintf(stderr, "Invalid --retransmit-buffer-datagrams: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 24:
                if (parse_int(optarg, &cfg->retransmit_max_datagrams_per_feedback) != 0) {
                    fprintf(stderr, "Invalid --retransmit-max-datagrams-per-feedback: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 25:
                if (strcmp(optarg, "xor") == 0) {
                    cfg->fec_enabled = 1;
                } else if (strcmp(optarg, "off") == 0) {
                    cfg->fec_enabled = 0;
                } else {
                    fprintf(stderr, "Invalid --fec-mode: %s (expected off|xor)\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 26:
                if (parse_int(optarg, &cfg->fec_k) != 0) {
                    fprintf(stderr, "Invalid --fec-k: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 27:
                if (parse_int(optarg, &cfg->fec_r) != 0) {
                    fprintf(stderr, "Invalid --fec-r: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            case 28:
                if (parse_int(optarg, &cfg->drop_datagram_every) != 0) {
                    fprintf(stderr, "Invalid --drop-datagram-every: %s\n", optarg);
                    print_usage(argv[0]);
                    return -1;
                }
                break;
            default:
                print_usage(argv[0]);
                return -1;
        }
    }

    if (cfg->crc32_test_mode) {
        return 0;
    }

    if (!cfg->dst_ip || !cfg->log_path || cfg->dst_port <= 0 || cfg->dst_port > 65535 ||
        cfg->rate_hz <= 0 || cfg->duration_sec <= 0) {
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->payload_len < 0 || cfg->payload_len > FRAME_V1_PAYLOAD_MAX_BYTES) {
        fprintf(stderr, "Invalid --payload-len: %d (expected 0..%d)\n", cfg->payload_len, FRAME_V1_PAYLOAD_MAX_BYTES );
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->sndbuf_set && cfg->sndbuf <= 0) {
        fprintf(stderr, "Invalid --sndbuf: %d (expected > 0)\n", cfg->sndbuf);
        print_usage(argv[0]);
        return -1;
    }

    if (cfg->version != (int)kFrameV1Version) {
        fprintf(stderr, "Unsupported --version: %d (expected %u)\n", cfg->version, kFrameV1Version);
        print_usage(argv[0]);
        return -1;
    }

    if (cfg->outage_at_sec_set != cfg->outage_duration_ms_set) {
        fprintf(stderr, "--outage-at-sec and --outage-duration-ms must be specified together\n");
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->outage_at_sec_set) {
        if (cfg->outage_at_sec < 0) {
            fprintf(stderr, "Invalid --outage-at-sec: %d (expected >= 0)\n", cfg->outage_at_sec);
            print_usage(argv[0]);
            return -1;
        }
        if (cfg->outage_duration_ms <= 0) {
            fprintf(stderr, "Invalid --outage-duration-ms: %d (expected > 0)\n", cfg->outage_duration_ms);
            print_usage(argv[0]);
            return -1;
        }
        cfg->outage_enabled = 1;
    }

    if ((cfg->feedback_bind_ip || cfg->feedback_bind_port > 0 || cfg->adaptive_log_path) &&
        (!cfg->feedback_bind_ip || cfg->feedback_bind_port <= 0 || !cfg->adaptive_log_path)) {
        fprintf(stderr, "--feedback-bind-ip, --feedback-bind-port and --adaptive-log-path must be specified together\n");
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->feedback_bind_port < 0 || cfg->feedback_bind_port > 65535) {
        fprintf(stderr, "Invalid --feedback-bind-port: %d\n", cfg->feedback_bind_port);
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->retransmit_buffer_datagrams <= 0) {
        fprintf(stderr, "Invalid --retransmit-buffer-datagrams: %d\n", cfg->retransmit_buffer_datagrams);
        return -1;
    }
    if (cfg->retransmit_max_datagrams_per_feedback <= 0) {
        fprintf(stderr, "Invalid --retransmit-max-datagrams-per-feedback: %d\n", cfg->retransmit_max_datagrams_per_feedback);
        return -1;
    }

    if (cfg->fec_enabled && (cfg->fec_k != FEC_V1_K_FIXED || cfg->fec_r != FEC_V1_R_FIXED)) {
        fprintf(stderr, "Invalid FEC parameters: this milestone supports --fec-k 4 --fec-r 1 only\n");
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->drop_datagram_every < 0) {
        fprintf(stderr, "Invalid --drop-datagram-every: %d (expected >= 0)\n", cfg->drop_datagram_every);
        return -1;
    }
    if (cfg->fec_enabled && cfg->retransmit_enabled) {
        fprintf(stderr, "--fec-mode xor and --retransmit-mode on are not supported together in this milestone\n");
        return -1;
    }

    cfg->feedback_enabled = cfg->feedback_bind_ip && cfg->feedback_bind_port > 0 && cfg->adaptive_log_path;

    if (cfg->adaptive_min_rate_hz <= 0 || cfg->adaptive_max_rate_hz <= 0 ||
        cfg->adaptive_min_rate_hz > cfg->adaptive_max_rate_hz) {
        fprintf(stderr, "Invalid adaptive rate range: min=%d max=%d\n", cfg->adaptive_min_rate_hz, cfg->adaptive_max_rate_hz);
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->rate_hz < cfg->adaptive_min_rate_hz || cfg->rate_hz > cfg->adaptive_max_rate_hz) {
        fprintf(stderr, "Initial --rate-hz must be within adaptive range: rate=%d min=%d max=%d\n",
                cfg->rate_hz, cfg->adaptive_min_rate_hz, cfg->adaptive_max_rate_hz);
        print_usage(argv[0]);
        return -1;
    }
    if (cfg->adaptive_debug_set_rate_hz != 0 &&
        (cfg->adaptive_debug_set_rate_hz < cfg->adaptive_min_rate_hz ||
         cfg->adaptive_debug_set_rate_hz > cfg->adaptive_max_rate_hz)) {
        fprintf(stderr, "Invalid --adaptive-debug-set-rate-hz: %d outside min/max\n", cfg->adaptive_debug_set_rate_hz);
        print_usage(argv[0]);
        return -1;
    }

    return 0;
}

static void close_output_files(TxFiles *files) {
    if (files->log_fp) {
        fclose(files->log_fp);
        files->log_fp = NULL;
    }
    if (files->adaptive_log_fp) {
        fclose(files->adaptive_log_fp);
        files->adaptive_log_fp = NULL;
    }
}

static int open_output_files(const TxConfig *config, TxFiles *files) {
    files->log_fp = fopen(config->log_path, "a");
    if (!files->log_fp) {
        perror("fopen(log_path)");
        return -1;
    }
    if (config->adaptive_log_path) {
        files->adaptive_log_fp = fopen(config->adaptive_log_path, "w");
        if (!files->adaptive_log_fp) {
            perror("fopen(adaptive_log_path)");
            close_output_files(files);
            return -1;
        }
        fprintf(files->adaptive_log_fp,
                "elapsed_sec,feedback_seq,missing_delta,missing_rate,p99_latency_ms,old_rate_hz,new_rate_hz,action,reason,stable_windows,retransmit_start_seq,retransmit_count,retransmit_sent_datagrams,retransmit_buffer_miss\n");
        fflush(files->adaptive_log_fp);
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

static const char *fault_target_name(FaultTarget t) {
    switch (t) {
        case FAULT_PREAMBLE:    return "preamble";
        case FAULT_PAYLOAD_LEN: return "payload_len";
        case FAULT_CRC:         return "crc";
        case FAULT_PAYLOAD:     return "payload";
        case FAULT_HEADER:      return "header";
        default:             return "none";
    }
}

// 故障注入: frame_v1_build() 後の wire バイト列に対して�arget フィールドを破壊する。
// 確率 rate で注入し、実施した場合はログに記録する。
static void apply_fault_injection(
    FaultTarget target,
    float rate,
    uint8_t *frame_buf,
    size_t frame_len,
    size_t payload_len,
    uint32_t seq,
    FILE *log_fp
) {
    // 確率判定
    float r = (float)rand() / ((float)RAND_MAX + 1.0f);
    if (r >= rate) {
        return;
    }

    char msg[128];

    switch (target) {
        case FAULT_PREAMBLE: {
            // preamble (bytes 0-3) の任意 1bit を反転
            int byte_off = rand() % 4;
            int bit_off  = rand() % 8;
            frame_buf[byte_off] ^= (uint8_t)(1U << bit_off);
            snprintf(msg, sizeof(msg),
                     "seq=%lu: fault injected to preamble (byte=%d bit=%d)",
                     (unsigned long)seq, byte_off, bit_off);
            break;
        }
        case FAULT_PAYLOAD_LEN: {
            // payload_len を上限超えの値に書き換え
            uint16_t bad_len = (uint16_t)(FRAME_V1_PAYLOAD_MAX_BYTES + 1);
            frame_buf[FRAME_V1_PAYLOAD_LEN_OFFSET]     = (uint8_t)(bad_len >> 8);
            frame_buf[FRAME_V1_PAYLOAD_LEN_OFFSET + 1] = (uint8_t)bad_len;
            snprintf(msg, sizeof(msg),
                     "seq=%lu: fault injected to payload_len (bad_len=%u)",
                     (unsigned long)seq, (unsigned int)bad_len);
            break;
        }
        case FAULT_CRC: {
            // crc32 フィールド (bytes 21-24) の任意 1bit を反転
            int byte_off = FRAME_V1_CRC32_OFFSET + rand() % 4;
            int bit_off  = rand() % 8;
            frame_buf[byte_off] ^= (uint8_t)(1U << bit_off);
            snprintf(msg, sizeof(msg),
                     "seq=%lu: fault injected to crc (byte=%d bit=%d)",
                     (unsigned long)seq, byte_off, bit_off);
            break;
        }
        case FAULT_PAYLOAD: {
            // payload_len=0 のときは注入不可
            if (payload_len == 0) {
                snprintf(msg, sizeof(msg),
                         "seq=%lu: fault skip payload (payload_len=0)", (unsigned long)seq);
                write_log_line(log_fp, "WARN", msg);
                return;
            }
            int byte_off = (int)(rand() % payload_len);
            int bit_off  = rand() % 8;
            frame_buf[FRAME_V1_WIRE_HEADER_LEN + (size_t)byte_off] ^= (uint8_t)(1U << bit_off);
            snprintf(msg, sizeof(msg),
                     "seq=%lu: fault injected to payload (byte=%d bit=%d)",
                     (unsigned long)seq, byte_off, bit_off);
            break;
        }
        case FAULT_HEADER: {
            // version または header_len をランダムに不正値に書き換え
            if (rand() % 2 == 0) {
                frame_buf[FRAME_V1_VERSION_OFFSET] = kFrameV1Version + 1U;
                snprintf(msg, sizeof(msg),
                         "seq=%lu: fault injected to header (version=%u)",
                         (unsigned long)seq, (unsigned int)(kFrameV1Version + 1U));
            } else {
                frame_buf[FRAME_V1_HEADER_LEN_OFFSET] = (uint8_t)(FRAME_V1_WIRE_HEADER_LEN + 1);
                snprintf(msg, sizeof(msg),
                         "seq=%lu: fault injected to header (header_len=%d)",
                         (unsigned long)seq, FRAME_V1_WIRE_HEADER_LEN + 1);
            }
            break;
        }
        default:
            return;
    }

    write_log_line(log_fp, "INFO", msg);
    (void)frame_len;  // 将来の範囲チェック拡張用
}

static void write_summary(const TxFiles *files, const TxTotals *totals, uint64_t elapsed_ns) {
    char msg[1024];
    double avg_rate = 0.0;

    if (!files || !files->log_fp || !totals) {
        return;
    }

    if (elapsed_ns > 0) {
        // avg_rate_hz はフレームレート（frame/s）。totals->seq がフレーム総数。
        avg_rate = (double)totals->seq / ((double)elapsed_ns / 1e9);
    }

    snprintf(
        msg,
        sizeof(msg),
        "tx summary sent=%lu last_seq=%lu elapsed_sec=%.3f avg_rate_hz=%.2f"
        " retransmit_requested_frames=%llu retransmit_sent_datagrams=%llu retransmit_sent_frames=%llu retransmit_buffer_miss_count=%llu"
        " fec_mode=%s fec_k=%d fec_r=%d fec_data_datagrams=%llu fec_parity_datagrams=%llu dropped_datagrams=%llu",
        (unsigned long)totals->sent,
        (unsigned long)((totals->seq == 0) ? 0 : (totals->seq - 1)),
        (double)elapsed_ns / 1e9,
        avg_rate,
        (unsigned long long)totals->retransmit_requested_frames,
        (unsigned long long)totals->retransmit_sent_datagrams,
        (unsigned long long)totals->retransmit_sent_frames,
        (unsigned long long)totals->retransmit_buffer_miss_count,
        (totals->fec_data_datagrams > 0 || totals->fec_parity_datagrams > 0) ? "xor" : "off",
        FEC_V1_K_FIXED,
        FEC_V1_R_FIXED,
        (unsigned long long)totals->fec_data_datagrams,
        (unsigned long long)totals->fec_parity_datagrams,
        (unsigned long long)totals->dropped_datagrams
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

static int now_process_cpu_ns(uint64_t *out_ns) {
    struct timespec ts;
    if (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts) != 0) {
        return -1;
    }
    *out_ns = (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
    return 0;
}

static int build_dst_addr(const char *ip, int port, struct sockaddr_in *out) {
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



static void tx_rate_recompute_period(TxRateState *rate) {
    rate->period_ns = (1000000000ULL * (uint64_t)TX_FRAMES_PER_DATAGRAM) / (uint64_t)rate->current_rate_hz;
    rate->period_remainder = (1000000000ULL * (uint64_t)TX_FRAMES_PER_DATAGRAM) % (uint64_t)rate->current_rate_hz;
    rate->remainder_acc = 0;
}

static int tx_rate_clamp(const TxRateState *rate, int requested_rate_hz) {
    if (requested_rate_hz < rate->min_rate_hz) {
        return rate->min_rate_hz;
    }
    if (requested_rate_hz > rate->max_rate_hz) {
        return rate->max_rate_hz;
    }
    return requested_rate_hz;
}

static int tx_rate_set(TxRateState *rate, int requested_rate_hz) {
    int next_rate_hz = tx_rate_clamp(rate, requested_rate_hz);
    if (next_rate_hz == rate->current_rate_hz) {
        return rate->current_rate_hz;
    }
    rate->current_rate_hz = next_rate_hz;
    tx_rate_recompute_period(rate);
    return rate->current_rate_hz;
}

static void tx_rate_init(TxRateState *rate, const TxConfig *cfg) {
    rate->current_rate_hz = cfg->rate_hz;
    rate->min_rate_hz = cfg->adaptive_min_rate_hz;
    rate->max_rate_hz = cfg->adaptive_max_rate_hz;
    tx_rate_recompute_period(rate);
}


static int tx_rate_multiply(TxRateState *rate, double factor) {
    double raw = (double)rate->current_rate_hz * factor;
    int requested = (factor >= 1.0) ? (int)(raw + 0.999999) : (int)raw;
    if (requested < 1) {
        requested = 1;
    }
    return tx_rate_set(rate, requested);
}

static void decide_adaptive_rate(
    const TxConfig *cfg,
    TxRateState *rate,
    const FeedbackV1Packet *packet,
    double missing_rate,
    double p99_latency_ms,
    int *old_rate_hz,
    int *new_rate_hz,
    const char **action,
    const char **reason
) {
    *old_rate_hz = rate->current_rate_hz;
    *new_rate_hz = *old_rate_hz;
    *action = "hold";
    *reason = "feedback_logged";

    if (!cfg->adaptive_enabled) {
        *reason = "adaptive_off";
        return;
    }

    if (cfg->adaptive_debug_set_rate_hz > 0) {
        *new_rate_hz = tx_rate_set(rate, cfg->adaptive_debug_set_rate_hz);
        if (*new_rate_hz != *old_rate_hz) {
            *action = "set_rate";
            *reason = "debug_set_rate";
        }
        return;
    }

    if (packet->missing_delta >= 3 || missing_rate > 0.001) {
        rate->stable_windows = 0;
        *new_rate_hz = tx_rate_multiply(rate, 0.80);
        *action = (*new_rate_hz < *old_rate_hz) ? "decrease" : "hold";
        *reason = "missing_detected";
        return;
    }

    if (packet->missing_delta == 0) {
        rate->stable_windows++;
        if (rate->stable_windows >= 3 && p99_latency_ms > cfg->adaptive_high_latency_ms) {
            *new_rate_hz = tx_rate_multiply(rate, 1.05);
            *action = (*new_rate_hz > *old_rate_hz) ? "increase" : "hold";
            *reason = "stable_latency_threshold";
            return;
        }
        *reason = "stable_wait";
        return;
    }

    rate->stable_windows = 0;
}

static int open_feedback_socket(const TxConfig *cfg, const TxFiles *files) {
    struct sockaddr_in bind_addr = {0};
    int sock = -1;
    char msg[256];

    if (!cfg || !cfg->feedback_enabled) {
        return -1;
    }

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("feedback socket");
        return -1;
    }

    if (build_dst_addr(cfg->feedback_bind_ip, cfg->feedback_bind_port, &bind_addr) != 0) {
        close(sock);
        return -1;
    }

    if (bind(sock, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) != 0) {
        perror("feedback bind");
        close(sock);
        return -1;
    }

    snprintf(msg, sizeof(msg),
             "feedback receiver enabled bind=%s:%d adaptive_log=%s",
             cfg->feedback_bind_ip,
             cfg->feedback_bind_port,
             cfg->adaptive_log_path);
    write_log_line(files ? files->log_fp : NULL, "INFO", msg);
    return sock;
}

static int tx_retransmit_buffer_init(TxRetransmitBuffer *buf, size_t cap) {
    if (!buf || cap == 0) {
        return -1;
    }
    buf->items = calloc(cap, sizeof(buf->items[0]));
    if (!buf->items) {
        return -1;
    }
    buf->cap = cap;
    buf->next = 0;
    return 0;
}

static void tx_retransmit_buffer_free(TxRetransmitBuffer *buf) {
    if (!buf) {
        return;
    }
    free(buf->items);
    *buf = (TxRetransmitBuffer){0};
}

static void tx_retransmit_buffer_store(TxRetransmitBuffer *buf, uint32_t start_seq, const uint8_t *bytes, size_t len) {
    TxStoredDatagram *slot = NULL;
    if (!buf || !buf->items || buf->cap == 0 || !bytes || len > sizeof(slot->bytes)) {
        return;
    }
    slot = &buf->items[buf->next];
    memset(slot, 0, sizeof(*slot));
    slot->start_seq = start_seq;
    slot->frame_count = TX_FRAMES_PER_DATAGRAM;
    slot->len = len;
    slot->valid = 1;
    memcpy(slot->bytes, bytes, len);
    buf->next = (buf->next + 1u) % buf->cap;
}

static int ranges_overlap(uint32_t a_start, uint32_t a_count, uint32_t b_start, uint32_t b_count) {
    uint64_t a_end = (uint64_t)a_start + (uint64_t)a_count;
    uint64_t b_end = (uint64_t)b_start + (uint64_t)b_count;
    return (uint64_t)a_start < b_end && (uint64_t)b_start < a_end;
}

static uint32_t tx_retransmit_range(
    int sock,
    const struct sockaddr_in *dest,
    const TxConfig *cfg,
    TxFiles *files,
    TxRetransmitBuffer *buf,
    TxTotals *totals,
    uint32_t start_seq,
    uint32_t count,
    uint32_t *out_buffer_miss
) {
    uint32_t sent_datagrams = 0;
    uint32_t buffer_miss = 0;
    char msg[256];

    if (out_buffer_miss) {
        *out_buffer_miss = 0;
    }
    if (!cfg || !cfg->retransmit_enabled || sock < 0 || !dest || !buf || !buf->items || count == 0) {
        return 0;
    }

    for (size_t i = 0; i < buf->cap; i++) {
        TxStoredDatagram *slot = &buf->items[i];
        if (!slot->valid) {
            continue;
        }
        if (!ranges_overlap(slot->start_seq, slot->frame_count, start_seq, count)) {
            continue;
        }
        if (sent_datagrams >= (uint32_t)cfg->retransmit_max_datagrams_per_feedback) {
            break;
        }
        ssize_t n = sendto(sock, slot->bytes, slot->len, 0, (const struct sockaddr *)dest, sizeof(*dest));
        if (n < 0 || (size_t)n != slot->len) {
            buffer_miss++;
            continue;
        }
        sent_datagrams++;
        if (totals) {
            totals->retransmit_sent_datagrams++;
            totals->retransmit_sent_frames += slot->frame_count;
        }
    }
    if (sent_datagrams == 0) {
        buffer_miss++;
    }
    if (totals) {
        totals->retransmit_requested_frames += count;
        totals->retransmit_buffer_miss_count += buffer_miss;
    }
    if (out_buffer_miss) {
        *out_buffer_miss = buffer_miss;
    }
    snprintf(msg, sizeof(msg),
             "retransmit request start_seq=%lu count=%lu sent_datagrams=%lu buffer_miss=%lu",
             (unsigned long)start_seq,
             (unsigned long)count,
             (unsigned long)sent_datagrams,
             (unsigned long)buffer_miss);
    write_log_line(files ? files->log_fp : NULL, "INFO", msg);
    return sent_datagrams;
}

static void process_feedback_packets(int feedback_sock, int data_sock, const struct sockaddr_in *dest, const TxConfig *cfg, TxFiles *files, TxRateState *rate, TxRetransmitBuffer *rtx_buf, TxTotals *totals, uint64_t now_ns, uint64_t t_start_ns) {
    uint8_t buf[FEEDBACK_V1_WIRE_LEN];
    char msg[256];

    if (feedback_sock < 0 || !cfg || !files || !files->adaptive_log_fp) {
        return;
    }

    for (;;) {
        FeedbackV1Packet packet = {0};
        ssize_t n = recvfrom(feedback_sock, buf, sizeof(buf), MSG_DONTWAIT, NULL, NULL);
        double elapsed_sec = 0.0;
        double missing_rate = 0.0;
        double p99_latency_ms = 0.0;
        int old_rate_hz = rate ? rate->current_rate_hz : cfg->rate_hz;
        int new_rate_hz = old_rate_hz;
        const char *action = "hold";
        const char *reason = "feedback_logged";
        uint32_t retransmit_sent_datagrams = 0;
        uint32_t retransmit_buffer_miss = 0;

        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                return;
            }
            snprintf(msg, sizeof(msg), "feedback recv failed errno=%d", errno);
            write_log_line(files->log_fp, "WARN", msg);
            return;
        }

        if ((size_t)n != FEEDBACK_V1_WIRE_LEN || feedback_v1_parse(buf, (size_t)n, &packet) != 0) {
            snprintf(msg, sizeof(msg), "feedback invalid len=%zd", n);
            write_log_line(files->log_fp, "WARN", msg);
            continue;
        }

        if (now_ns >= t_start_ns) {
            elapsed_sec = (double)(now_ns - t_start_ns) / 1e9;
        }
        missing_rate = (double)packet.missing_rate_ppm / 1000000.0;
        p99_latency_ms = (double)packet.p99_latency_us / 1000.0;
        if (rate) {
            decide_adaptive_rate(cfg, rate, &packet, missing_rate, p99_latency_ms,
                                 &old_rate_hz, &new_rate_hz, &action, &reason);
        }
        if (cfg->retransmit_enabled && (packet.flags & FEEDBACK_V1_FLAG_RETRANSMIT_REQUEST) && packet.retransmit_count > 0) {
            retransmit_sent_datagrams = tx_retransmit_range(
                data_sock, dest, cfg, files, rtx_buf, totals,
                packet.retransmit_start_seq, packet.retransmit_count, &retransmit_buffer_miss);
        }

        fprintf(files->adaptive_log_fp,
                "%.3f,%lu,%lu,%.6f,%.3f,%d,%d,%s,%s,%d,%lu,%lu,%lu,%lu\n",
                elapsed_sec,
                (unsigned long)packet.feedback_seq,
                (unsigned long)packet.missing_delta,
                missing_rate,
                p99_latency_ms,
                old_rate_hz,
                new_rate_hz,
                action,
                reason,
                rate ? rate->stable_windows : 0,
                (unsigned long)packet.retransmit_start_seq,
                (unsigned long)packet.retransmit_count,
                (unsigned long)retransmit_sent_datagrams,
                (unsigned long)retransmit_buffer_miss);
        fflush(files->adaptive_log_fp);

        snprintf(msg, sizeof(msg),
                 "feedback received seq=%lu missing_delta=%lu missing_rate_ppm=%lu p99_latency_us=%lu action=%s old_rate_hz=%d new_rate_hz=%d",
                 (unsigned long)packet.feedback_seq,
                 (unsigned long)packet.missing_delta,
                 (unsigned long)packet.missing_rate_ppm,
                 (unsigned long)packet.p99_latency_us,
                 action,
                 old_rate_hz,
                 new_rate_hz);
        write_log_line(files->log_fp, "INFO", msg);
    }
}

static void timespec_add_ns(struct timespec *t, uint64_t ns) {
    t->tv_sec += ns / 1000000000ULL;
    t->tv_nsec += (long)(ns % 1000000000ULL);
    if (t->tv_nsec >= 1000000000L) {
        t->tv_sec += 1;
        t->tv_nsec -= 1000000000L;
    } else if (t->tv_nsec < 0) {
        t->tv_sec -= 1;
        t->tv_nsec += 1000000000L;
    }
}

static void write_stats_per_1sec(const TxFiles *files, TxTimingState *ts, const TxTotals *totals) {
    char msg[256];
    uint64_t process_cpu_now_ns = 0;
    uint64_t cpu_delta_ns = 0;
    uint64_t window_elapsed_ns = ts->next_stats_ns - ts->last_stats_wall_ns;
    uint32_t datagrams_delta = totals->sent - ts->last_sent_datagrams;
    uint32_t frames_delta = totals->seq - ts->last_sent_frames;
    double pps = (window_elapsed_ns > 0)
        ? ((double)datagrams_delta * 1000000000.0 / (double)window_elapsed_ns)
        : 0.0;
    double cpu_pct = 0.0;
    uint64_t elapsed_sec = (ts->next_stats_ns - ts->t_start_ns) / UINT64_C(1000000000);

    if (!files || !files->log_fp || !ts || !totals) {
        return;
    }

    if (now_process_cpu_ns(&process_cpu_now_ns) == 0) {
        if (process_cpu_now_ns >= ts->last_process_cpu_ns && window_elapsed_ns > 0) {
            cpu_delta_ns = process_cpu_now_ns - ts->last_process_cpu_ns;
            cpu_pct = (double)cpu_delta_ns * 100.0 / (double)window_elapsed_ns;
        }
        ts->last_process_cpu_ns = process_cpu_now_ns;
    }

    snprintf(
        msg,
        sizeof(msg),
        "tx_stats elapsed_sec=%llu sent_datagrams=%lu"
        " sent_frames=%lu pps=%.2f cpu_pct=%.2f",
        (unsigned long long)elapsed_sec,
        (unsigned long)datagrams_delta,
        (unsigned long)frames_delta,
        pps,
        cpu_pct
    );
    write_log_line(files->log_fp, "INFO", msg);

    ts->last_stats_wall_ns = ts->next_stats_ns;
    ts->last_sent_datagrams = totals->sent;
    ts->last_sent_frames = totals->seq;
}

static void fill_payload_pattern(uint8_t *payload, size_t payload_len) {
    for (size_t i = 0; i < payload_len; i++) {
        payload[i] = (uint8_t)(i & 0xFFU);
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
    printf("payload_len=%zu seq=0x%08lX tx_ts=0x%016llX\n",
           (size_t)frame.payload_len, (unsigned long)frame.seq, (unsigned long long)frame.tx_ts);
    printf("crc32=0x%08lX frame_len=%zu\n", (unsigned long)frame.crc32, frame_len);
    return 0;
}

int main(int argc, char **argv) {
    TxConfig cfg = {0};
    TxFiles files = {0};
    TxTotals totals = {0};
    TxTimingState ts = {0};
    TxOutageState outage = {0};
    TxRateState rate = {0};
    FrameV1Header frame = {0};
    uint8_t payload[FRAME_V1_PAYLOAD_MAX_BYTES] = {0};
    uint8_t datagram_buf[TX_MAX_DATA_DATAGRAM_BYTES];
    uint8_t send_buf[TX_MAX_FEC_DATAGRAM_BYTES];
    uint8_t parity_payload[TX_MAX_DATA_DATAGRAM_BYTES] = {0};
    size_t fec_payload_len = 0;
    int fec_block_count = 0;
    uint32_t fec_block_id = 0;
    uint32_t fec_block_first_seq = 0;
    int logged_first_frame = 0;
    int pending_first_frame_log = 0;
    char first_frame_log_msg[256] = {0};
    int feedback_sock = -1;
    TxRetransmitBuffer rtx_buf = {0};

    if (parse_args(argc, argv, &cfg) != 0) {
        return 1;
    }

    if (cfg.crc32_test_mode) {
        return run_crc32_test_mode();
    }

    // 故障注入の乱数シードを初期化
    srand((unsigned int)time(NULL));

    if (open_output_files(&cfg, &files) != 0) {
        return 1;
    }

    char buf[256];
    fill_payload_pattern(payload, (size_t)cfg.payload_len);
    tx_rate_init(&rate, &cfg);

    if (files.log_fp) {
        snprintf(buf, sizeof(buf),
                 "frame_v1 config version=%u header_len=%u payload_len=%d payload_max=%d",
                 kFrameV1Version,
                 (unsigned)FRAME_V1_WIRE_HEADER_LEN,
                 cfg.payload_len,
                 FRAME_V1_PAYLOAD_MAX_BYTES);
        write_log_line(files.log_fp, "INFO", buf);

        snprintf(buf, sizeof(buf),
                 "tx start dst=%s:%d rate_hz=%d duration_sec=%d payload_len=%d",
                 cfg.dst_ip, cfg.dst_port, cfg.rate_hz, cfg.duration_sec, cfg.payload_len);
        write_log_line(files.log_fp, "INFO", buf);

        if (cfg.fault_target != FAULT_NONE) {
            snprintf(buf, sizeof(buf),
                     "fault injection enabled target=%s rate=%.2f",
                     fault_target_name(cfg.fault_target), (double)cfg.fault_rate);
            write_log_line(files.log_fp, "INFO", buf);
        }
        if (cfg.retransmit_enabled) {
            snprintf(buf, sizeof(buf),
                     "retransmit enabled buffer_datagrams=%d max_datagrams_per_feedback=%d",
                     cfg.retransmit_buffer_datagrams,
                     cfg.retransmit_max_datagrams_per_feedback);
            write_log_line(files.log_fp, "INFO", buf);
        }
        if (cfg.fec_enabled) {
            snprintf(buf, sizeof(buf),
                     "fec enabled mode=xor k=%d r=%d header_len=%d drop_datagram_every=%d",
                     cfg.fec_k, cfg.fec_r, FEC_V1_HEADER_LEN, cfg.drop_datagram_every);
            write_log_line(files.log_fp, "INFO", buf);
        }
        if (cfg.outage_enabled) {
            snprintf(buf, sizeof(buf),
                     "outage configured at_sec=%d duration_ms=%d",
                     cfg.outage_at_sec, cfg.outage_duration_ms);
            write_log_line(files.log_fp, "INFO", buf);
        }
    }

    printf("tx started: dst=%s:%d rate_hz=%d duration=%d log=%s\n",
           cfg.dst_ip, cfg.dst_port, cfg.rate_hz, cfg.duration_sec, cfg.log_path);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        close_output_files(&files);
        return 1;
    }

    if (cfg.sndbuf_set) {
        if (apply_socket_buffer_setting(files.log_fp, sock, SO_SNDBUF, "SO_SNDBUF", cfg.sndbuf) != 0) {
            close(sock);
            close_output_files(&files);
            return 1;
        }
    }

    struct sockaddr_in dest = {0};
    if (build_dst_addr(cfg.dst_ip, cfg.dst_port, &dest) != 0) {
        close(sock);
        close_output_files(&files);
        return 1;
    }

    if (cfg.retransmit_enabled) {
        if (tx_retransmit_buffer_init(&rtx_buf, (size_t)cfg.retransmit_buffer_datagrams) != 0) {
            write_log_line(files.log_fp, "ERROR", "retransmit buffer allocation failed");
            close(sock);
            close_output_files(&files);
            return 1;
        }
    }

    if (cfg.feedback_enabled) {
        feedback_sock = open_feedback_socket(&cfg, &files);
        if (feedback_sock < 0) {
            close(sock);
            close_output_files(&files);
            return 1;
        }
    }

    if (clock_gettime(CLOCK_MONOTONIC, &ts.next_send) != 0) {
        perror("clock_gettime");
        close(sock);
        close_output_files(&files);
        return 1;
    }

    // --rate-hz はフレームレート（frame/s）として扱う。
    // 1 datagram に TX_FRAMES_PER_DATAGRAM フレームを含むため、
    // datagram 送信周期 = (1s * TX_FRAMES_PER_DATAGRAM) / rate_hz となる。
    // 例) rate_hz=100, TX_FRAMES_PER_DATAGRAM=3:
    //   period_ns = 3000000000/100 = 30000000 ns (30 ms)
    //   → 33.3 datagram/s × 3 frame = 100 frame/s ✓
    ts.period_ns = rate.period_ns;

    if (now_monotonic_ns(&ts.t_start_ns) != 0) {
        perror("clock_gettime");
        close(sock);
        close_output_files(&files);
        return 1;
    }

    if (ts.t_start_ns == 0) {
        close(sock);
        close_output_files(&files);
        return 1;
    }
    ts.next_stats_ns = ts.t_start_ns + 1000000000ULL;
    ts.last_stats_wall_ns = ts.t_start_ns;
    if (cfg.outage_enabled) {
        outage.start_ns_from_t0 = (uint64_t)cfg.outage_at_sec * 1000000000ULL;
        outage.duration_ns = (uint64_t)cfg.outage_duration_ms * 1000000ULL;
        outage.end_ns_from_t0 = outage.start_ns_from_t0 + outage.duration_ns;
    }
    if (now_process_cpu_ns(&ts.last_process_cpu_ns) != 0) {
        ts.last_process_cpu_ns = 0;
    }

    if (now_monotonic_ns(&ts.now_ns) != 0) {
        perror("clock_gettime");
        close(sock);
        close_output_files(&files);
        return 1;
    }

    // 初回送信即時化:
    //   next_send を 1 周期分だけ過去に設定しておく。
    //   ループ先頭の timespec_add_ns で next_send += period となり、
    //   clock_nanosleep は過去時刻 (≈ t_start) を目標とするため即時返る。
    ts.next_send.tv_nsec -= (long)(ts.period_ns % 1000000000ULL);
    ts.next_send.tv_sec  -= (long)(ts.period_ns / 1000000000ULL);
    if (ts.next_send.tv_nsec < 0) {
        ts.next_send.tv_nsec += 1000000000L;
        ts.next_send.tv_sec--;
    }

    while (ts.now_ns - ts.t_start_ns < (uint64_t)cfg.duration_sec * 1000000000ULL) {
        // remainder 補正: 端数を蓄積し rate_hz 回で +1ns して長期平均を合わせる
        uint64_t this_period = rate.period_ns;
        rate.remainder_acc += rate.period_remainder;
        if (rate.remainder_acc >= (uint64_t)rate.current_rate_hz) {
            this_period++;
            rate.remainder_acc -= (uint64_t)rate.current_rate_hz;
        }
        timespec_add_ns(&ts.next_send, this_period);
        int sleep_err = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &ts.next_send, NULL);
        if (sleep_err != 0 && sleep_err != EINTR) {
            errno = sleep_err;
            perror("clock_nanosleep");
            write_log_line(files.log_fp, "ERROR", "clock_nanosleep failed");
            break;
        }

        if (now_monotonic_ns(&ts.now_ns) != 0) {
            write_log_line(files.log_fp, "ERROR", "clock_gettime failed");
            break;
        }

        if (now_monotonic_ns(&ts.tx_ts_ns) != 0) {
            write_log_line(files.log_fp, "ERROR", "clock_gettime failed before send");
            break;
        }

        uint64_t elapsed_tx_ns = (ts.tx_ts_ns > ts.t_start_ns) ? (ts.tx_ts_ns - ts.t_start_ns) : 0;
        if (cfg.outage_enabled) {
            if (!outage.logged_start && elapsed_tx_ns >= outage.start_ns_from_t0) {
                snprintf(buf, sizeof(buf),
                         "outage start elapsed_sec=%.3f duration_ms=%d",
                         (double)elapsed_tx_ns / 1e9,
                         cfg.outage_duration_ms);
                write_log_line(files.log_fp, "INFO", buf);
                outage.logged_start = 1;
                outage.active = 1;
            }

            if (outage.active && elapsed_tx_ns < outage.end_ns_from_t0) {
                continue;
            }

            if (outage.active && !outage.logged_end && elapsed_tx_ns >= outage.end_ns_from_t0) {
                snprintf(buf, sizeof(buf),
                         "outage end elapsed_sec=%.3f duration_ms=%d",
                         (double)elapsed_tx_ns / 1e9,
                         cfg.outage_duration_ms);
                write_log_line(files.log_fp, "INFO", buf);
                outage.logged_end = 1;
                outage.active = 0;
            }
        }

        // TX_FRAMES_PER_DATAGRAM 個のフレームを datagram_buf に連結してから 1 回の sendto で送る
        uint32_t datagram_start_seq = totals.seq;
        size_t datagram_len = 0;
        int build_ok = 1;
        for (int fi = 0; fi < TX_FRAMES_PER_DATAGRAM && build_ok; fi++) {
            size_t one_frame_len = 0;
            memset(&frame, 0, sizeof(frame));
            frame.seq   = totals.seq + (uint32_t)fi;
            frame.tx_ts = ts.tx_ts_ns;
            frame.flags = kFrameV1FlagsNone;
            uint8_t *dst = datagram_buf + datagram_len;
            size_t   cap = sizeof(datagram_buf) - datagram_len;
            if (frame_v1_build(&frame, payload, (size_t)cfg.payload_len, dst, cap, &one_frame_len) != 0) {
                write_log_line(files.log_fp, "ERROR", "frame_v1_build failed");
                build_ok = 0;
                break;
            }
            if (!logged_first_frame && files.log_fp) {
                snprintf(first_frame_log_msg, sizeof(first_frame_log_msg),
                         "frame_v1 first_frame version=%u payload_len=%u seq=%lu crc32=0x%08lX frame_len=%zu",
                         (unsigned int)frame.version,
                         (unsigned int)frame.payload_len,
                         (unsigned long)frame.seq,
                         (unsigned long)frame.crc32,
                         one_frame_len);
                pending_first_frame_log = 1;
                logged_first_frame = 1;
            }
            // 故障注入（frame_v1_build 後の wire バイト列を直接書き換える）
            if (cfg.fault_target != FAULT_NONE) {
                apply_fault_injection(
                    cfg.fault_target,
                    cfg.fault_rate,
                    dst,
                    one_frame_len,
                    (size_t)cfg.payload_len,
                    totals.seq + (uint32_t)fi,
                    files.log_fp
                );
            }
            datagram_len += one_frame_len;
        }
        if (!build_ok) break;

        const uint8_t *wire_to_send = datagram_buf;
        size_t wire_len = datagram_len;
        int drop_this_datagram = 0;
        uint64_t data_attempt_index = (uint64_t)(datagram_start_seq / TX_FRAMES_PER_DATAGRAM) + 1u;

        if (cfg.drop_datagram_every > 0 && (data_attempt_index % (uint64_t)cfg.drop_datagram_every) == 0) {
            drop_this_datagram = 1;
        }

        if (cfg.fec_enabled) {
            FecV1Header fec_header = {0};
            if (fec_block_count == 0) {
                memset(parity_payload, 0, sizeof(parity_payload));
                fec_payload_len = datagram_len;
                fec_block_first_seq = datagram_start_seq;
            }
            if (datagram_len != fec_payload_len) {
                write_log_line(files.log_fp, "ERROR", "FEC datagram length changed within block");
                break;
            }
            for (size_t i = 0; i < datagram_len; i++) {
                parity_payload[i] ^= datagram_buf[i];
            }

            fec_header.version = FEC_V1_VERSION;
            fec_header.header_len = FEC_V1_HEADER_LEN;
            fec_header.packet_type = FEC_V1_TYPE_DATA;
            fec_header.k = FEC_V1_K_FIXED;
            fec_header.r = FEC_V1_R_FIXED;
            fec_header.index_in_block = (uint8_t)fec_block_count;
            fec_header.payload_len = (uint16_t)datagram_len;
            fec_header.block_id = fec_block_id;
            fec_header.first_seq = fec_block_first_seq;
            if (fec_v1_build_header(&fec_header, send_buf, sizeof(send_buf)) != 0) {
                write_log_line(files.log_fp, "ERROR", "fec_v1_build_header data failed");
                break;
            }
            memcpy(send_buf + FEC_V1_HEADER_LEN, datagram_buf, datagram_len);
            wire_to_send = send_buf;
            wire_len = FEC_V1_HEADER_LEN + datagram_len;
            totals.fec_data_datagrams++;
        }

        if (drop_this_datagram) {
            totals.dropped_datagrams++;
        } else {
            ssize_t sent = sendto(sock, wire_to_send, wire_len, 0, (struct sockaddr *)&dest, sizeof(dest));
            if (sent < 0) {
                perror("sendto");
                write_log_line(files.log_fp, "ERROR", "sendto failed");
                break;
            }

            if ((size_t)sent != wire_len) {
                write_log_line(files.log_fp, "ERROR", "sendto returned unexpected size");
                break;
            }

            if (cfg.retransmit_enabled) {
                tx_retransmit_buffer_store(&rtx_buf, datagram_start_seq, datagram_buf, datagram_len);
            }
            totals.sent++;
        }

        totals.seq += TX_FRAMES_PER_DATAGRAM;

        if (cfg.fec_enabled) {
            fec_block_count++;
            if (fec_block_count == FEC_V1_K_FIXED) {
                FecV1Header parity_header = {0};
                parity_header.version = FEC_V1_VERSION;
                parity_header.header_len = FEC_V1_HEADER_LEN;
                parity_header.packet_type = FEC_V1_TYPE_PARITY;
                parity_header.k = FEC_V1_K_FIXED;
                parity_header.r = FEC_V1_R_FIXED;
                parity_header.index_in_block = FEC_V1_K_FIXED;
                parity_header.payload_len = (uint16_t)fec_payload_len;
                parity_header.block_id = fec_block_id;
                parity_header.first_seq = fec_block_first_seq;
                if (fec_v1_build_header(&parity_header, send_buf, sizeof(send_buf)) != 0) {
                    write_log_line(files.log_fp, "ERROR", "fec_v1_build_header parity failed");
                    break;
                }
                memcpy(send_buf + FEC_V1_HEADER_LEN, parity_payload, fec_payload_len);
                ssize_t sent = sendto(sock, send_buf, FEC_V1_HEADER_LEN + fec_payload_len, 0, (struct sockaddr *)&dest, sizeof(dest));
                if (sent < 0) {
                    perror("sendto");
                    write_log_line(files.log_fp, "ERROR", "sendto parity failed");
                    break;
                }
                if ((size_t)sent != FEC_V1_HEADER_LEN + fec_payload_len) {
                    write_log_line(files.log_fp, "ERROR", "sendto parity returned unexpected size");
                    break;
                }
                totals.fec_parity_datagrams++;
                fec_block_id++;
                fec_block_count = 0;
                fec_payload_len = 0;
            }
        }

        if (pending_first_frame_log) {
            write_log_line(files.log_fp, "INFO", first_frame_log_msg);
            pending_first_frame_log = 0;
        }

        process_feedback_packets(feedback_sock, sock, &dest, &cfg, &files, &rate, &rtx_buf, &totals, ts.tx_ts_ns, ts.t_start_ns);

        while (ts.tx_ts_ns >= ts.next_stats_ns) {
            write_stats_per_1sec(&files, &ts, &totals);
            ts.next_stats_ns += 1000000000ULL;
        }
    }

    process_feedback_packets(feedback_sock, sock, &dest, &cfg, &files, &rate, &rtx_buf, &totals, ts.now_ns, ts.t_start_ns);

    if (feedback_sock >= 0) {
        close(feedback_sock);
    }
    close(sock);

    uint64_t t_end_ns = 0;
    if (now_monotonic_ns(&t_end_ns) != 0) {
        perror("clock_gettime");
        close_output_files(&files);
        return 1;
    }

    uint64_t elapsed_ns = (t_end_ns > ts.t_start_ns) ? (t_end_ns - ts.t_start_ns) : 0;

    if (cfg.outage_enabled && outage.logged_start && !outage.logged_end && files.log_fp) {
        snprintf(buf, sizeof(buf),
                 "outage end elapsed_sec=%.3f duration_ms=%d reason=tx_end",
                 (double)elapsed_ns / 1e9,
                 cfg.outage_duration_ms);
        write_log_line(files.log_fp, "INFO", buf);
    }

    while (t_end_ns >= ts.next_stats_ns) {
        write_stats_per_1sec(&files, &ts, &totals);
        ts.next_stats_ns += 1000000000ULL;
    }

    if (files.log_fp) {
        write_summary(&files, &totals, elapsed_ns);
        write_log_line(files.log_fp, "INFO", "tx end");
    }
    tx_retransmit_buffer_free(&rtx_buf);
    close_output_files(&files);

    printf("tx finished\n");
    return 0;
}

