#!/usr/bin/env bash
#
# run_local_10s.sh
#
# 目的:
#   - ローカルPC（127.0.0.1）で tx/rx を10秒動かす
#   - 毎回同じ手順で実行できるようにする
#   - ログ保存先を固定ルールで作る（比較しやすくする）
#
# #2時点では tx/rx はスタブだが、このスクリプト自体の価値は大きい。
# 後続 issue で中身が本実装に変わっても、実行手順はなるべく変えない。

# set -euo pipefail の意味:
# -e : コマンド失敗時に即終了（エラー見逃し防止）
# -u : 未定義変数を使うとエラー（typo検出）
# -o pipefail : パイプ途中の失敗も拾う（将来の拡張で重要）
set -euo pipefail

# スクリプトの場所を基準にリポジトリルートへ移動する
#
# なぜ必要か:
#   カレントディレクトリ依存をなくすため。
#   どこから実行しても logs/ や bin/ の相対パスが安定する。
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# 実行ごとにユニークなログディレクトリを作る
# 例: logs/run_20260223_123456_10s
#
# なぜタイムスタンプ付きにするのか:
#   - 過去実行を上書きしない
#   - 比較しやすい
#   - PR証跡として残しやすい
TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="logs/run_${TS}_10s"
mkdir -p "$RUN_DIR"

# tx/rx のログファイルパスを固定

RX_LOG="$RUN_DIR/rx.log"
RX_CSV_IN_1SEC_LOG="$RUN_DIR/rx_in_1sec.csv"
RX_CSV_BY_1RECV_LOG="$RUN_DIR/rx_by_1recv.csv"

TX_LOG="$RUN_DIR/tx.log"

echo "[INFO] run dir: $RUN_DIR"

# 先に rx をバックグラウンドで起動する
#
# なぜ rx 先行か:
#   受信側が先に待ち受け状態になってから送信を始めるため。
#   本実装になった時、先にtxを起動すると最初のパケットを取りこぼしやすい。
#
# "&" を付けるとバックグラウンド実行になる。
./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 10 --log-path "$RX_LOG"  --csv-in-1sec-log-path "$RX_CSV_IN_1SEC_LOG" --csv-by-1recv-log-path "$RX_CSV_BY_1RECV_LOG" &
RX_PID=$!

# $! は「直前に起動したバックグラウンドプロセスのPID」
# なぜ保持するのか:
#   後で wait して終了を待つため（スクリプトが先に終わらないように）
#
# ここで少し待つ理由:
#   rx起動直後にtxを開始すると、本実装時に起動競合しやすい。
sleep 1

# tx をフォアグラウンドで起動
# フォアグラウンドにしている理由:
#   tx側のエラーをこのスクリプトの終了コードに反映しやすい
./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 100 --duration-sec 10 --log-path "$TX_LOG"

# rx の終了を待つ
#
# "|| true" の理由:
#   #2時点や将来の検証中に rx が先に終了していても、
#   スクリプト全体を最後まで進めてログ一覧を見たい場合があるため。
#   （厳密運用にしたい場合は外してもよい）
wait "$RX_PID" || true

echo "[INFO] finished"
echo "[INFO] logs:"
ls -l "$RUN_DIR"