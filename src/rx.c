// src/rx.c
//
// このファイルの役割（#2時点）:
//   - rx 実行ファイルとして起動できること
//   - CLI引数を受け取れること（usageを出せること）
//   - ログファイルに開始/終了を書けること
//
// まだやらないこと（#2では範囲外）:
//   - UDP bind / recv
//   - non-blocking I/O / select/poll
//   - seq確認 / latency算出 / drop推定
//
// #5以降で中身を入れ替える前提の「土台」です。

#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// 受信側の設定をまとめる構造体
//
// bind_ip をポインタにしている理由は tx.c と同じ。
// CLI引数文字列（argv内）を読み取り専用で参照するだけなのでコピー不要。
typedef struct {
    const char *bind_ip;   // bind先IP（例: "127.0.0.1" / "0.0.0.0"）
    int port;              // bindポート
    int duration_sec;      // 実行時間（#2では待機時間として使う）
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

    char buf[256];
    snprintf(buf, sizeof(buf),
             "rx start bind=%s:%d duration_sec=%d",
             cfg.bind_ip, cfg.port, cfg.duration_sec);
    write_log_line(fp, "INFO", buf);

    printf("rx started: bind=%s:%d duration=%d log=%s\n",
           cfg.bind_ip, cfg.port, cfg.duration_sec, cfg.log_path);

    // #2では受信ループの代わりに待機だけする
    // #5でここが select/poll ベースの受信ループに置き換わる予定
    sleep((unsigned int)cfg.duration_sec);

    write_log_line(fp, "INFO", "rx end");
    fclose(fp);

    printf("rx finished\n");
    return 0;
}