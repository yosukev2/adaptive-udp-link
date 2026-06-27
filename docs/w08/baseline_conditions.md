# W08 共通 baseline 条件

## 対象範囲

W08 では、Raspberry Pi 5 Linux 上の既存 UDP `tx` / `rx` プログラムを計測対象にする。`tx` と `rx` は同じ Raspberry Pi 5 上で動かし、host loopback 経由で通信する。Raspberry Pi Pico とその firmware はこの実験の対象外であり、変更しない。

この共通 baseline は、送信間隔、socket buffer、CPU affinity の比較で `before` 条件として使い回す。各 `after` 実験では、候補因子を 1 つだけ変える。

## baseline 条件

| category | 固定する baseline 値 | 確認方法または注記 |
| --- | --- | --- |
| target host | Raspberry Pi 5 Linux、`tx` と `rx` は同一ホストで実行 | `uname -a` とリポジトリの commit を `run_metadata.md` に記録する。 |
| Pico firmware | 使用しない、変更しない | W08 の一部として Pico を flash / rebuild / 再接続しない。 |
| network path | host loopback のみ。有線・無線は使わない | 物理 Ethernet と Wi-Fi は baseline の対象外。 |
| Linux interface | `lo` | `ip -brief address show lo` で確認する。 |
| bind / destination IP | `127.0.0.1` / `127.0.0.1` | 両方の timestamp を同じ `CLOCK_MONOTONIC` 系で扱う。 |
| UDP port | `9000` | `rx --port` と `tx --dst-port` で同じ値を使う。 |
| protocol version | Frame v1 (`--version 1`) | `tx` は現時点で version 1 のみ受け付ける。 |
| payload length | 1 frame あたり `48` bytes | `--payload-len 48` を指定する。1 datagram に 3 frame 入る。 |
| send rate | `100` frames/s | `--rate-hz 100` を指定する。これは datagram rate ではなく frame rate。 |
| TX duration | `60` seconds | `tx --duration-sec 60` を指定する。 |
| RX duration | `62` seconds | 先に `rx` を起動し、1 秒待ってから `tx` を 60 秒実行し、最後に 1 秒分の受信 tail を残す。 |
| fault injection | 無効 | `--fault-target`、`--fault-rate`、`--outage-at-sec`、`--outage-duration-ms` は指定しない。 |
| recovery mode | `fsm` | `rx --recovery-mode fsm` を指定する。outage は注入しない。 |
| socket buffers | Linux のデフォルト。`setsockopt()` で上書きしない | 実行前に `net.core.wmem_default` と `net.core.rmem_default` を記録する。 |
| CPU affinity | 制限しない | baseline では `taskset` を使わない。 |
| background load | 意図的な負荷生成をしない | 予期しない重いプロセスがあれば記録するか、run を invalid にする。 |
| trials | 有効な run を 3 回 | trial number は 1, 2, 3 を使う。 |
| official latency CSV | `data/w08/baseline/runN.csv` | `rx --csv-by-1recv-log-path` を使う。`N` は trial number。 |
| auxiliary output | `data/w08/baseline/runN_rx.log`, `runN_tx.log`, `runN_1sec.csv` | text log は append mode なので、run ごとに別 path を使う。 |
| run metadata | `data/w08/baseline/run_metadata.md` | コマンド、開始時刻、commit、kernel、buffer defaults、validity を記録する。 |

condition 名、trial number、出力先、実行時刻などの metadata は run ごとに変わってよい。これらは実験因子ではない。

## 各 after 条件で固定する項目

| after condition | 変更してよい項目 | それ以外の baseline 項目 |
| --- | --- | --- |
| send interval | `--rate-hz` | loopback path、payload、duration、socket defaults、affinity 制限なしは固定。 |
| socket buffer | Issue #127 で導入する `--sndbuf` / `--rcvbuf` | `--rate-hz 100` と affinity 制限なしは固定。要求値と実際の buffer size を記録する。 |
| CPU affinity | Issue #128 で導入する `taskset` による CPU 選択 | `--rate-hz 100` と socket buffer のデフォルト値は固定。 |

after 条件は組み合わせない。特に、socket-buffer run で `taskset` を併用しないこと、affinity run で socket buffer を上書きしないこと。

## コマンドテンプレート

`bin/tx` と `bin/rx` を build したあと、Raspberry Pi 5 の repository root から実行する。`N` は `1`、`2`、`3` のいずれかに置き換える。

```bash
mkdir -p data/w08/baseline
N=1

rm -f \
  "data/w08/baseline/run${N}.csv" \
  "data/w08/baseline/run${N}_1sec.csv" \
  "data/w08/baseline/run${N}_rx.log" \
  "data/w08/baseline/run${N}_tx.log"

./bin/rx \
  --bind-ip 127.0.0.1 \
  --port 9000 \
  --duration-sec 62 \
  --log-path "data/w08/baseline/run${N}_rx.log" \
  --link-name w08_baseline \
  --trial "${N}" \
  --csv-in-1sec-log-path "data/w08/baseline/run${N}_1sec.csv" \
  --csv-by-1recv-log-path "data/w08/baseline/run${N}.csv" \
  --recovery-mode fsm &
rx_pid=$!

sleep 1

./bin/tx \
  --dst-ip 127.0.0.1 \
  --dst-port 9000 \
  --rate-hz 100 \
  --duration-sec 60 \
  --log-path "data/w08/baseline/run${N}_tx.log" \
  --payload-len 48 \
  --version 1
tx_status=$?

wait "$rx_pid"
rx_status=$?

printf 'trial=%s tx_status=%s rx_status=%s\n' \
  "$N" "$tx_status" "$rx_status"
```

`N` を 1, 2, 3 と順に変えて実行する。run 前に 4 つの path を削除するのは必須である。text log は追記型であり、invalid な retry に stale output を残してはいけないためである。

最初の run の前に、host state を変更せずに記録する。

```bash
date --iso-8601=seconds
uname -a
git rev-parse HEAD
ip -brief address show lo
sysctl net.core.wmem_default net.core.rmem_default
```

## run の有効条件

run が有効なのは、以下をすべて満たす場合だけである。

- `tx_status=0` と `rx_status=0` を、両方の process 待ち合わせ後に記録していること。W07 の USB capture status `124` のような timeout exit は、この Linux process では想定しないし受け入れない。
- `runN.csv` の header が、6 列 `rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status` と完全一致し、少なくとも 1 行の data があること。
- `runN_1sec.csv` の header が、11 列 `elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt,pps,cpu_pct` と完全一致し、少なくとも 1 行の data があること。
- header 検証は W07 analyzer と同じく、field count だけでなく ordered field list 全体を比較すること。
- `runN_tx.log` に `tx summary` と `tx end` が含まれ、`runN_rx.log` に `rx summary`、`rx end`、および選択した `N` に対する `trial_summary link_name=w08_baseline trial=N` がちょうど 1 回含まれること。
- 両方の process log に `ERROR` が含まれないこと。
- 選択した trial number `N`、`--trial N` 引数、RX summary の `trial=N`、そして 4 つの `runN*` 出力 path が一致していること。他 trial や以前の retry の出力は受け入れない。
- metadata に、実際のコマンド、両方の exit code、開始時刻、commit、kernel、socket-buffer defaults、予期しない background load の有無が記録されていること。
- 関連する `after` run に割り当てられた 1 つの変更以外は、この baseline から変わっていないこと。

以下のコマンドは、各 run 後に schema と log を確認するためのものです。header の文字列と field 数の両方を意図的に確認します。

```bash
test "$tx_status" -eq 0
test "$rx_status" -eq 0

test "$(head -n 1 "data/w08/baseline/run${N}.csv")" = \
  'rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status'
test "$(awk -F, 'NR==1{print NF}' "data/w08/baseline/run${N}.csv")" -eq 6
test "$(wc -l < "data/w08/baseline/run${N}.csv")" -gt 1

test "$(head -n 1 "data/w08/baseline/run${N}_1sec.csv")" = \
  'elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt,pps,cpu_pct'
test "$(awk -F, 'NR==1{print NF}' "data/w08/baseline/run${N}_1sec.csv")" -eq 11
test "$(wc -l < "data/w08/baseline/run${N}_1sec.csv")" -gt 1

grep -q 'tx summary' "data/w08/baseline/run${N}_tx.log"
grep -q 'tx end' "data/w08/baseline/run${N}_tx.log"
grep -q 'rx summary' "data/w08/baseline/run${N}_rx.log"
grep -q 'rx end' "data/w08/baseline/run${N}_rx.log"
test "$(grep -c "trial_summary link_name=w08_baseline trial=${N} " \
  "data/w08/baseline/run${N}_rx.log")" -eq 1
! grep -q 'ERROR' "data/w08/baseline/run${N}_tx.log"
! grep -q 'ERROR' "data/w08/baseline/run${N}_rx.log"
```

## 除外条件

W08 baseline と、各 one-factor comparison は Raspberry Pi 5 の host loopback のみを使う。Wi-Fi、物理 Ethernet、別ホスト、その他の network namespace や virtual network path は除外する。Raspberry Pi Pico、Pico firmware、USB CDC capture、W07 bare-metal / FreeRTOS の計測も W08 の比較対象外である。

除外した path や device を使った場合は、それを W08 の結果として解釈せず、その run を invalid とする。理由を記録し、同じ trial number でやり直す。invalid run は 3 回の比較には含めない。
