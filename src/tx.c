// src/tx.c
//
// このファイルの役割（#2時点）:
//   - tx 実行ファイルとして起動できること
//   - CLI引数を受け取れること（usageを出せること）
//   - ログファイルに開始/終了を書けること
//
// まだやらないこと（#2では範囲外）:
//   - UDPソケット送信
//   - seq付与
//   - timestamp付与
//
// なぜこの段階でスタブ（仮実装）を作るのか:
//   後続 issue で毎回同じ手順で「起動」「ログ確認」ができる土台を先に固定するため。
//   計測系は手順の再現性が命。

#include <errno.h>    // errno（エラー原因の保持）
#include <getopt.h>   // getopt_long（長い形式のCLI引数解析: --dst-ip など）
#include <stdio.h>    // printf, fprintf, fopen, fclose
#include <stdlib.h>   // strtol, exit系
#include <string.h>   // 文字列処理（今回は直接は少なめだが将来使いやすい）
#include <time.h>     // time, localtime_r, strftime（ログの時刻表示）
#include <unistd.h>   // sleep

#include "frame.h"
// 設定値をまとめる構造体
//
// なぜ構造体にまとめるのか:
//   1) 引数が増えたときに関数へ渡しやすい
//   2) 「設定」の概念を1つにできる
//   3) グローバル変数を増やさずに済む
//
// なぜ const char* なのか（ポインタの話）:
//   - CLI引数文字列は argv に入っている
//   - argvの各要素は「文字列の先頭アドレス（ポインタ）」
//   - 今回は文字列を"読むだけ"なので、コピーせず参照だけで十分
//   - だから const char*（読み取り専用の文字列ポインタ）で持つ
//
// もし後でこの文字列を編集したいなら:
//   - 自前バッファにコピーして char[] / malloc で管理する必要がある
typedef struct {
    const char *dst_ip;   // 送信先IPアドレス（例: "127.0.0.1"）
    int dst_port;         // 送信先ポート（1〜65535）
    int rate_hz;          // 送信レート（Hz） ※#2では受け取るだけ
    int duration_sec;     // 実行時間（秒）
    const char *log_path; // ログファイルパス（例: logs/run_xxx/tx.log）
} TxConfig;

// usage表示関数
//
// なぜ関数に分けるのか:
//   - 引数不足/不正時に何度も同じ文を出すため
//   - mainを見やすくするため
static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s --dst-ip <ip> --dst-port <port> --rate-hz <hz> "
            "--duration-sec <sec> --log-path <path>\n",
            prog);
}

// 文字列 -> int 変換の共通関数
//
// なぜ atoi を使わないのか:
//   atoi はエラー検出が弱い（"abc" などで0になる等、区別しづらい）
//   strtol は失敗判定がしやすい（errno / endポインタを見られる）
//
// endポインタとは:
//   strtol が「どこまで数値として読めたか」を返してくれる位置。
//   例: "123abc" なら end は 'a' を指す。
//   今回は完全一致したいので *end == '\0' を要求する。
static int parse_int(const char *s, int *out) {
    char *end = NULL;
    errno = 0;

    long v = strtol(s, &end, 10);

    // 失敗条件:
    // - errno != 0        : オーバーフロー等
    // - end == s          : 1文字も数値を読めていない
    // - *end != '\0'      : 数値の後ろに余計な文字がある（例: 100hz）
    if (errno != 0 || end == s || *end != '\0') return -1;

    // int範囲チェック（環境依存を避けるため明示）
    if (v < -2147483648L || v > 2147483647L) return -1;

    *out = (int)v;
    return 0;
}

// 1行ログを書き込む関数
//
// なぜ毎回 fflush するのか:
//   #2段階では「ログがちゃんと出たこと」を確認したいので、即時反映を優先。
//   バッファリング効率は多少落ちるが、学習・検証段階ではメリットが大きい。
static void write_log_line(FILE *fp, const char *level, const char *msg) {
    time_t now = time(NULL);

    // struct tm は時刻の分解結果（年/月/日/時/分/秒）
    struct tm tmv;

    // localtime_r:
    //   スレッドセーフ版の localtime
    //   今回は単一スレッドだが、癖としてこちらを使っておくと安全
    localtime_r(&now, &tmv);

    char ts[64];
    strftime(ts, sizeof(ts), "%Y-%m-%d %H:%M:%S", &tmv);

    fprintf(fp, "%s [%s] %s\n", ts, level, msg);
    fflush(fp);
}

int main(int argc, char **argv) {
    // argc: 引数の個数
    // argv: 引数文字列の配列（正確には「文字列へのポインタの配列」）
    //
    // なぜ char **argv なのか:
    //   argv[i] は各文字列の先頭アドレス（char*）
    //   それが並んでいるので「char* の配列」
    //   配列は関数引数に渡すと先頭ポインタに変わるため char**
    //
    // ざっくり:
    //   argv -> ["./bin/tx", "--dst-ip", "127.0.0.1", ...]
    //
    // cfg = {0} は全フィールドを0/NULLで初期化する記法
    TxConfig cfg = {0};

    int opt;
    int option_index = 0; // getopt_longがどのlong optionを見つけたか入れる用（今回は主に慣例）

    // 長い形式のオプション定義
    //
    // {"dst-ip", required_argument, 0, 1}
    //   name = "dst-ip"
    //   required_argument = 値が必須（--dst-ip 127.0.0.1）
    //   flag = 0
    //   val = 1（switchで識別するための番号）
    //
    // ※文字1文字の短いオプション（-p 等）を使わず、可読性優先で long option のみにしている
    static struct option long_opts[] = {
        {"dst-ip", required_argument, 0, 1},
        {"dst-port", required_argument, 0, 2},
        {"rate-hz", required_argument, 0, 3},
        {"duration-sec", required_argument, 0, 4},
        {"log-path", required_argument, 0, 5},
        {0, 0, 0, 0} // 配列終端（getopt_longの慣例）
    };

    // 引数を順に解析
    // 第3引数 "" は短いオプション文字列（今回は使わないので空）
    while ((opt = getopt_long(argc, argv, "", long_opts, &option_index)) != -1) {
        switch (opt) {
            case 1:
                // dst-ip文字列をそのまま参照（コピーしない）
                cfg.dst_ip = optarg;
                break;

            case 2:
                if (parse_int(optarg, &cfg.dst_port) != 0) {
                    fprintf(stderr, "Invalid --dst-port: %s\n", optarg);
                    print_usage(argv[0]);
                    return 1;
                }
                break;

            case 3:
                if (parse_int(optarg, &cfg.rate_hz) != 0) {
                    fprintf(stderr, "Invalid --rate-hz: %s\n", optarg);
                    print_usage(argv[0]);
                    return 1;
                }
                break;

            case 4:
                if (parse_int(optarg, &cfg.duration_sec) != 0) {
                    fprintf(stderr, "Invalid --duration-sec: %s\n", optarg);
                    print_usage(argv[0]);
                    return 1;
                }
                break;

            case 5:
                cfg.log_path = optarg;
                break;

            default:
                // 未知のオプションなど
                print_usage(argv[0]);
                return 1;
        }
    }

    // 必須項目チェック + 範囲チェック
    //
    // なぜここでまとめて検証するのか:
    //   パース時は「形式としてintに読めるか」
    //   ここでは「意味として妥当か（port範囲、正の値か）」を確認する
    if (!cfg.dst_ip || !cfg.log_path || cfg.dst_port <= 0 || cfg.dst_port > 65535 ||
        cfg.rate_hz <= 0 || cfg.duration_sec <= 0) {
        print_usage(argv[0]);
        return 1;
    }

    // ログファイルを追記モードで開く
    // "a" にする理由:
    //   - 同じファイルに複数回書く可能性がある
    //   - 存在しなければ作成される
    FILE *fp = fopen(cfg.log_path, "a");
    if (!fp) {
        perror("fopen(log_path)");
        return 1;
    }

    // 起動ログを書き込む
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
             "tx start dst=%s:%d rate_hz=%d duration_sec=%d",
             cfg.dst_ip, cfg.dst_port, cfg.rate_hz, cfg.duration_sec);
    write_log_line(fp, "INFO", buf);

    // 画面にも表示（使っている人間に分かりやすく）
    printf("tx started: dst=%s:%d rate_hz=%d duration=%d log=%s\n",
           cfg.dst_ip, cfg.dst_port, cfg.rate_hz, cfg.duration_sec, cfg.log_path);

    // #2ではまだ送信ループを作らないので、実行時間分だけ待機して終了する
    // #4でここが「固定レート送信ループ」に置き換わる予定
    sleep((unsigned int)cfg.duration_sec);

    write_log_line(fp, "INFO", "tx end");
    fclose(fp);

    printf("tx finished\n");
    return 0;
}