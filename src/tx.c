// src/tx.c
//
// 役割
//   - UDP送信プログラム（tx）のエントリポイント
//   - CLI引数の解析（dst-ip / dst-port / rate-hz / duration-sec / log-path）
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

typedef struct {
    const char *dst_ip;    // 送信先IP（例: "127.0.0.1"）
    int dst_port;          // 送信先ポート
    int rate_hz;           // 送信レート（Hz）
    int duration_sec;      // 実行時間
    const char *log_path;  // ログファイルパス
    int payload_len;       // 送信する payload 長（byte）
    int version;           // プロトコルバージョン（現状は v1 固定）
    int crc32_test_mode;   // ハードコードした v1 フレームで CRC32 を確認する
} TxConfig;

typedef struct {
    FILE *log_fp;
} TxFiles;

typedef struct {
    uint32_t seq;
    uint32_t sent;
} TxTotals;

typedef struct {
    struct timespec next_send;  // 次回送信予定時刻（絶対時刻, CLOCK_MONOTONIC）
    uint64_t period_ns;         // 基本送信周期 = 1_000_000_000 / rate_hz（端数切り捨て）
                                // ループ内では remainder 補正後の this_period を使う
    uint64_t t_start_ns;
    uint64_t now_ns;
    uint64_t tx_ts_ns;
} TxTimingState;

static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s --dst-ip <ip> --dst-port <port> --rate-hz <hz> --duration-sec <sec> --log-path <path> [--payload-len <n>] [--version <n>] [--crc32-test]\n",
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

static int parse_args(int argc, char **argv, TxConfig *cfg) {
    int opt;
    int option_index = 0;

    cfg->version = (int)kFrameV1Version;
    cfg->payload_len = FRAME_V0_PAYLOAD_BYTES;

    static struct option long_opts[] = {
        {"dst-ip", required_argument, 0, 1},
        {"dst-port", required_argument, 0, 2},
        {"rate-hz", required_argument, 0, 3},
        {"duration-sec", required_argument, 0, 4},
        {"log-path", required_argument, 0, 5},
        {"version", required_argument, 0, 6},
        {"crc32-test", no_argument, 0, 7},
        {"payload-len", required_argument, 0, 8},
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
        fprintf(stderr, "Invalid --payload-len: %d (expected 0..%d)\n", cfg->payload_len, FRAME_V1_PAYLOAD_MAX_BYTES);
        print_usage(argv[0]);
        return -1;
    }

    if (cfg->version != (int)kFrameV1Version) {
        fprintf(stderr, "Unsupported --version: %d (expected %u)\n", cfg->version, kFrameV1Version);
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
}

static int open_output_files(const TxConfig *config, TxFiles *files) {
    files->log_fp = fopen(config->log_path, "a");
    if (!files->log_fp) {
        perror("fopen(log_path)");
        return -1;
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

static void write_summary(const TxFiles *files, const TxTotals *totals, uint64_t elapsed_ns) {
    char msg[256];
    double avg_rate = 0.0;

    if (!files || !files->log_fp || !totals) {
        return;
    }

    if (elapsed_ns > 0) {
        avg_rate = (double)totals->sent / ((double)elapsed_ns / 1e9);
    }

    snprintf(
        msg,
        sizeof(msg),
        "tx summary sent=%" PRIu32 " last_seq=%" PRIu32 " elapsed_sec=%.3f avg_rate_hz=%.2f",
        totals->sent,
        (totals->seq == 0) ? 0 : (totals->seq - 1),
        (double)elapsed_ns / 1e9,
        avg_rate
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
    printf("payload_len=%zu seq=0x%08" PRIX32 " tx_ts=0x%016" PRIX64 "\n",
           (size_t)frame.payload_len, frame.seq, frame.tx_ts);
    printf("crc32=0x%08" PRIX32 " frame_len=%zu\n", frame.crc32, frame_len);
    return 0;
}

int main(int argc, char **argv) {
    TxConfig cfg = {0};
    TxFiles files = {0};
    TxTotals totals = {0};
    TxTimingState ts = {0};
    FrameV1Header frame = {0};
    uint8_t payload[FRAME_V1_PAYLOAD_MAX_BYTES] = {0};
    uint8_t frame_bytes[FRAME_V1_MAX_WIRE_BYTES] = {0};
    int logged_first_frame = 0;

    if (parse_args(argc, argv, &cfg) != 0) {
        return 1;
    }

    if (cfg.crc32_test_mode) {
        return run_crc32_test_mode();
    }

    if (open_output_files(&cfg, &files) != 0) {
        return 1;
    }

    char buf[256];
    fill_payload_pattern(payload, (size_t)cfg.payload_len);

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
    }

    printf("tx started: dst=%s:%d rate_hz=%d duration=%d log=%s\n",
           cfg.dst_ip, cfg.dst_port, cfg.rate_hz, cfg.duration_sec, cfg.log_path);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        close_output_files(&files);
        return 1;
    }

    struct sockaddr_in dest = {0};
    if (build_dst_addr(cfg.dst_ip, cfg.dst_port, &dest) != 0) {
        close(sock);
        close_output_files(&files);
        return 1;
    }

    if (clock_gettime(CLOCK_MONOTONIC, &ts.next_send) != 0) {
        perror("clock_gettime");
        close(sock);
        close_output_files(&files);
        return 1;
    }

    // period_ns: 基本周期（端数切り捨て）
    // period_remainder: 切り捨て分。rate_hz 回ぶん蓄積すると 1ns 余る。
    // 例) rate_hz=7: period_ns=142857142, remainder=6
    //   → 7 周期合計 = 142857142*1 + 142857143*6 = 999999999+1 = 1000000000 ✓
    ts.period_ns = 1000000000ULL / (uint64_t)cfg.rate_hz;
    uint64_t period_remainder = 1000000000ULL % (uint64_t)cfg.rate_hz;
    uint64_t remainder_acc = 0;

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
        size_t frame_len = 0;

        // remainder 補正: 端数を蓄積し rate_hz 回で +1ns して長期平均を合わせる
        uint64_t this_period = ts.period_ns;
        remainder_acc += period_remainder;
        if (remainder_acc >= (uint64_t)cfg.rate_hz) {
            this_period++;
            remainder_acc -= (uint64_t)cfg.rate_hz;
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

        memset(&frame, 0, sizeof(frame));
        memset(frame_bytes, 0, sizeof(frame_bytes));
        if (now_monotonic_ns(&ts.tx_ts_ns) != 0) {
            write_log_line(files.log_fp, "ERROR", "clock_gettime failed before send");
            break;
        }

        frame.seq = totals.seq;
        frame.tx_ts = ts.tx_ts_ns;
        frame.flags = kFrameV1FlagsNone;
        if (frame_v1_build(&frame, payload, (size_t)cfg.payload_len, frame_bytes, sizeof(frame_bytes), &frame_len) != 0) {
            write_log_line(files.log_fp, "ERROR", "frame_v1_build failed");
            break;
        }
        if (!logged_first_frame && files.log_fp) {
            snprintf(buf, sizeof(buf),
                     "frame_v1 first_frame version=%u payload_len=%u seq=%" PRIu32 " crc32=0x%08" PRIX32 " frame_len=%zu",
                     frame.version,
                     frame.payload_len,
                     frame.seq,
                     frame.crc32,
                     frame_len);
            write_log_line(files.log_fp, "INFO", buf);
            logged_first_frame = 1;
        }

        ssize_t sent = sendto(sock, frame_bytes, frame_len, 0, (struct sockaddr *)&dest, sizeof(dest));
        if (sent < 0) {
            perror("sendto");
            write_log_line(files.log_fp, "ERROR", "sendto failed");
            break;
        }

        if ((size_t)sent != frame_len) {
            write_log_line(files.log_fp, "ERROR", "sendto returned unexpected size");
            break;
        }

        totals.seq++;
        totals.sent++;
    }

    close(sock);

    uint64_t t_end_ns = 0;
    if (now_monotonic_ns(&t_end_ns) != 0) {
        perror("clock_gettime");
        close_output_files(&files);
        return 1;
    }

    uint64_t elapsed_ns = (t_end_ns > ts.t_start_ns) ? (t_end_ns - ts.t_start_ns) : 0;

    if (files.log_fp) {
        write_summary(&files, &totals, elapsed_ns);
        write_log_line(files.log_fp, "INFO", "tx end");
    }

    close_output_files(&files);

    printf("tx finished\n");
    return 0;
}
