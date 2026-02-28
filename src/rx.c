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
//   - CSV出力 / 可視化 / オフライン集計
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
} RxConfig;

static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s --bind-ip <ip> --port <port> --duration-sec <sec> --log-path <path>\n",
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

static void write_log_line(FILE *fp, const char *level, const char *msg) {
    time_t now = time(NULL);
    struct tm tmv;
    localtime_r(&now, &tmv);

    char ts[64];
    strftime(ts, sizeof(ts), "%Y-%m-%d %H:%M:%S", &tmv);
    fprintf(fp, "%s [%s] %s\n", ts, level, msg);
    fflush(fp);
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



int main(int argc, char **argv) {

    RxConfig cfg = {0};

    // rx は bind-ip を省略可能にしておく（利便性のため）
    // 将来、ローカル検証時は 127.0.0.1、複数NIC環境では 0.0.0.0 と使い分けられる
    cfg.bind_ip = "0.0.0.0";

    int opt;
    int option_index = 0;

    static struct option long_opts[] = {
        {"bind-ip", required_argument, 0, 1},
        {"port", required_argument, 0, 2},
        {"duration-sec", required_argument, 0, 3},
        {"log-path", required_argument, 0, 4},
        {0, 0, 0, 0}
    };

    while ((opt = getopt_long(argc, argv, "", long_opts, &option_index)) != -1) {
        switch (opt) {
            case 1:
                cfg.bind_ip = optarg;
                break;

            case 2:
                if (parse_int(optarg, &cfg.port) != 0) {
                    fprintf(stderr, "Invalid --port: %s\n", optarg);
                    print_usage(argv[0]);
                    return 1;
                }
                break;

            case 3:
                if (parse_int(optarg, &cfg.duration_sec) != 0) {
                    fprintf(stderr, "Invalid --duration-sec: %s\n", optarg);
                    print_usage(argv[0]);
                    return 1;
                }
                break;

            case 4:
                cfg.log_path = optarg;
                break;

            default:
                print_usage(argv[0]);
                return 1;
        }
    }

    // 妥当性検証
    if (!cfg.log_path || cfg.port <= 0 || cfg.port > 65535 || cfg.duration_sec <= 0) {
        print_usage(argv[0]);
        return 1;
    }

    FILE *fp = fopen(cfg.log_path, "a");
    if (!fp) {
        perror("fopen(log_path)");
        return 1;
    }
    if (install_signal_handlers() != 0) {
        perror("sigaction");
        fclose(fp);
        return 1;
    }

    char buf[256];

    // Frame v0 の共有定義が見えていることを、起動時ログで確認できるようにする
    snprintf(buf, sizeof(buf),
             "frame_v0 sizeof=%zu payload_bytes=%d offsets(seq=%zu ts=%zu payload=%zu)",
             sizeof(FrameV0),
             FRAME_V0_PAYLOAD_BYTES,
             offsetof(FrameV0, seq),
             offsetof(FrameV0, timestamp_ns),
             offsetof(FrameV0, payload));
    write_log_line(fp, "INFO", buf);
    
    snprintf(buf, sizeof(buf),
             "rx start bind=%s:%d duration_sec=%d",
             cfg.bind_ip, cfg.port, cfg.duration_sec);
    write_log_line(fp, "INFO", buf);

    printf("rx started: bind=%s:%d duration=%d log=%s\n",
           cfg.bind_ip, cfg.port, cfg.duration_sec, cfg.log_path);

        
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("socket");
        fclose(fp);
        return 1;  // または exit(EXIT_FAILURE);
    }

    struct pollfd pfd;
    pfd.fd = sock;
    pfd.events = POLLIN;  // 読み取り可能イベントを待つ
    pfd.revents = 0; // 見やすさのため初期化（必須ではない）

    struct sockaddr_in bind_addr={0};
    if (build_bind_addr(cfg.bind_ip, cfg.port, &bind_addr) != 0) {
        close(sock);
        fclose(fp);
        return 1;
    }

    if (bind(sock, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) != 0) {
        perror("bind");
        close(sock);
        fclose(fp);
        return 1;
    }



    uint64_t now = 0;

    uint64_t t_start_ns = 0;

    // 起動ログを書き込む
    FrameV0 frame;
    uint8_t buf_udp[sizeof(FrameV0)];

    char msg[256];
    ssize_t n = 0;
    struct sockaddr_in src_addr;
    uint64_t rx_recv_any = 0;
    uint64_t rx_recv_ok = 0;
    
    uint64_t rx_recv_any_in_1sec = 0;
    uint64_t rx_recv_ok_in_1sec = 0;


    uint64_t rx_bad_size = 0;
    uint64_t rx_poll_timeout = 0;

    uint32_t prev_seq = 0; 
    bool has_prev_seq = false; 

    uint64_t gap_cnt = 0;
    uint64_t dup_cnt = 0;
    uint64_t reord_cnt = 0;

    uint64_t gap_cnt_in_1sec = 0;
    uint64_t dup_cnt_in_1sec = 0;
    uint64_t reord_cnt_in_1sec = 0;


    uint64_t latency_sum_ns = 0;
    uint64_t latency_sample_cnt = 0;
    uint64_t future_ts_cnt = 0;
    uint64_t future_ts_detected = 0;

    uint64_t recv_now_ns = 0;
    int wait_ms = 0;

    uint64_t latency = 0;
    uint64_t latency_sample_cnt_in_1sec = 0;
    uint64_t latency_sum_ns_in_1sec = 0;

    uint64_t avg_latency_ns_in_1sec = 0;
    uint64_t max_latency_ns_in_1sec = 0;
    uint64_t min_latency_ns_in_1sec = 0;

    uint64_t next_stats_ns = 0; // 1秒ごとに統計ログ出力
    uint64_t now_for_stats = 0; // 1秒ごとに統計ログ出力

    uint64_t avg_latency_ns = 0;
    uint64_t max_latency_ns = 0;
    uint64_t min_latency_ns = 0;


    if (now_monotonic_ns(&t_start_ns) != 0) {
        write_log_line(fp, "ERROR", "clock_gettime failed");
    }
    
    next_stats_ns = t_start_ns + 1000000000ULL;

    while (1) {
        if (g_stop_requested) {
            write_log_line(fp, "INFO", "stop requested by signal");
            break;
        }

        if (now_monotonic_ns(&now) != 0) {
            write_log_line(fp, "ERROR", "clock_gettime failed");
            break;
        }
        if (now - t_start_ns >= (uint64_t)cfg.duration_sec * 1000000000ULL) {
            avg_latency_ns_in_1sec = (latency_sample_cnt_in_1sec > 0) ? (latency_sum_ns_in_1sec / latency_sample_cnt_in_1sec) : 0;
            snprintf(msg, sizeof(msg),
                "rx_stats_final elapsed_ns=%" PRIu64 " avg_latency=%" PRIu64
                " max_latency=%" PRIu64 " min_latency=%" PRIu64 " recv_cnt=%" PRIu64 " ok_recv_cnt=%" PRIu64
                " gap_cnt=%" PRIu64 " dup_cnt=%" PRIu64 " reord_cnt=%" PRIu64,
                now - t_start_ns, avg_latency_ns_in_1sec, max_latency_ns_in_1sec, min_latency_ns_in_1sec, rx_recv_any_in_1sec, rx_recv_ok_in_1sec, gap_cnt_in_1sec, dup_cnt_in_1sec, reord_cnt_in_1sec);
            write_log_line(fp, "INFO", msg);
            write_log_line(fp, "INFO", "duration elapsed, exiting");
            break;
        }

        if (next_stats_ns > now) {
            wait_ms = (int)((next_stats_ns - now + 999999ULL) / 1000000ULL);
        } else {
            wait_ms = 0;
        }
        int ret = poll(&pfd, 1, wait_ms);

        if (ret < 0) {
            if (errno == EINTR) {
                if (g_stop_requested) {
                    write_log_line(fp, "INFO", "poll interrupted by signal");
                    break;
                }
                continue;
            }
            perror("poll");
            break;
        }else if (ret == 0) {
            rx_poll_timeout++;
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
                        write_log_line(fp, "INFO", "recvfrom interrupted by signal");
                        break;
                    }
                    continue;
                }
                perror("recvfrom");
                break;
            }
            
            rx_recv_any++;
            rx_recv_any_in_1sec++;

            if (n != (ssize_t)sizeof(FrameV0)) {
                rx_bad_size++;
                snprintf(msg, sizeof(msg), "unexpected size: %zd (expected %zu)", n, sizeof(FrameV0));
                write_log_line(fp, "WARN", msg);
                continue;
            }
            if (now_monotonic_ns(&recv_now_ns) != 0) {
                write_log_line(fp, "ERROR", "clock_gettime failed");
                break;
            }
            memcpy(&frame, buf_udp, sizeof(frame));
            // seq差分ベースの欠損推定（UDPなので推定値）
            // - 前進: gapを加算
            // - 重複: dupとして計上（gapには入れない）
            // - 逆順: reorderとして計上（gapには入れない）
            //   ※逆順でprev_seqを更新すると後続の推定を崩しやすい
            if (has_prev_seq){
                if (prev_seq == frame.seq) {
                    dup_cnt++;
                    dup_cnt_in_1sec++;
                } else if (prev_seq < frame.seq) {// W01では seq wrap-around（uint32_t周回）は未対応
                    gap_cnt += frame.seq - prev_seq - 1;
                    gap_cnt_in_1sec += frame.seq - prev_seq - 1;
                    prev_seq = frame.seq;
                } else if (frame.seq < prev_seq) {
                    reord_cnt++;
                    reord_cnt_in_1sec++;
                }
            }else {
                has_prev_seq = true;
                prev_seq = frame.seq;
            } 

            if (recv_now_ns >= frame.timestamp_ns) {
                latency = recv_now_ns - frame.timestamp_ns;
                latency_sum_ns += latency;
                latency_sum_ns_in_1sec   += latency;
                latency_sample_cnt++;
                latency_sample_cnt_in_1sec++;
                if (latency > max_latency_ns_in_1sec) {
                    max_latency_ns_in_1sec = latency;
                }
                if (min_latency_ns_in_1sec == 0 || latency < min_latency_ns_in_1sec) {
                    min_latency_ns_in_1sec = latency;
                }
            } else {
                future_ts_cnt++;
            }
            if (recv_now_ns < frame.timestamp_ns) {
                future_ts_detected = 1;
            }
            rx_recv_ok++;
            rx_recv_ok_in_1sec++;


        }
        if (now_monotonic_ns(&now_for_stats) != 0) {
            write_log_line(fp, "ERROR", "clock_gettime failed");
            break;
        }
        if (now_for_stats >= next_stats_ns ) {
            avg_latency_ns_in_1sec = (latency_sample_cnt_in_1sec > 0) ? (latency_sum_ns_in_1sec / latency_sample_cnt_in_1sec) : 0;
            snprintf(msg, sizeof(msg),
                "rx_stats elapsed_ns=%" PRIu64 " avg_latency=%" PRIu64
                " max_latency=%" PRIu64 " min_latency=%" PRIu64 " recv_cnt=%" PRIu64 " ok_recv_cnt=%" PRIu64
                " gap_cnt=%" PRIu64 " dup_cnt=%" PRIu64 " reord_cnt=%" PRIu64,
                now_for_stats - t_start_ns, avg_latency_ns_in_1sec, max_latency_ns_in_1sec, min_latency_ns_in_1sec, rx_recv_any_in_1sec, rx_recv_ok_in_1sec, gap_cnt_in_1sec, dup_cnt_in_1sec, reord_cnt_in_1sec);

            next_stats_ns += 1000000000ULL;            

            latency_sum_ns_in_1sec = 0;
            latency_sample_cnt_in_1sec = 0;
            max_latency_ns_in_1sec = 0;
            min_latency_ns_in_1sec = 0;
            rx_recv_any_in_1sec = 0;
            rx_recv_ok_in_1sec = 0;
            gap_cnt_in_1sec = 0;
            dup_cnt_in_1sec = 0;
            reord_cnt_in_1sec = 0;
            write_log_line(fp, "INFO", msg);
        }
        
    }

    uint64_t elapsed_ns = 0;
    if (now_monotonic_ns(&elapsed_ns) == 0 && elapsed_ns >= t_start_ns) {
        elapsed_ns -= t_start_ns;
    } else {
        elapsed_ns = 0;
    }

    snprintf(msg, sizeof(msg),
            "rx summary recv_any=%" PRIu64 " recv_ok=%" PRIu64
            " bad_size=%" PRIu64 " poll_timeout=%" PRIu64
            " elapsed_ms=%" PRIu64 " avg_latency_ms=%.3f gap_cnt=%" PRIu64 " dup_cnt=%" PRIu64 " reord_cnt=%" PRIu64 " future_ts_cnt=%" PRIu64 " future_ts_detected=%" PRIu64,
            rx_recv_any, rx_recv_ok,
             rx_bad_size, rx_poll_timeout,
            elapsed_ns / 1000000, (latency_sample_cnt > 0 ? (double)latency_sum_ns / latency_sample_cnt / 1000000.0 : 0.0),
            gap_cnt, dup_cnt, reord_cnt, future_ts_cnt, future_ts_detected);
    write_log_line(fp, "INFO", msg);

    write_log_line(fp, "INFO", "rx end");
    fclose(fp);
    close(sock);

    printf("rx finished\n");
    return 0;
}