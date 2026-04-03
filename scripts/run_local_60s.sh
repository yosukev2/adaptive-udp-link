#!/usr/bin/env bash
#
# run_local_60s.sh
#
# 目的:
#   - #2のAC「60秒実行のスクリプトがある」を満たす
#   - 後続 issue でも同じ手順で60秒安定性を確認できるようにする
#
# 10秒版とほぼ同じ構造にしている理由:
#   手順差分を最小化して、比較や保守を楽にするため。
#   （差分は duration と run_dir suffix 程度）

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="logs/run_${TS}_60s"
mkdir -p "$RUN_DIR"

RX_LOG="$RUN_DIR/rx.log"
RX_CSV_IN_1SEC_LOG="$RUN_DIR/rx_in_1sec.csv"
RX_CSV_BY_1RECV_LOG="$RUN_DIR/rx_by_1recv.csv"
TX_LOG="$RUN_DIR/tx.log"

echo "[INFO] run dir: $RUN_DIR"

# 受信側を先に起動（本実装時の取りこぼし防止）
./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 62 --log-path "$RX_LOG"  --csv-in-1sec-log-path "$RX_CSV_IN_1SEC_LOG" --csv-by-1recv-log-path "$RX_CSV_BY_1RECV_LOG" &
RX_PID=$!

# 起動安定化のための待機
# rx の duration-sec を tx より 2 秒長くしている理由:
#   sleep 1 の間も rx のタイマーが進むため、同じ duration にすると
#   最後の ~1 秒分（約 100 frame）を取りこぼす。+2 で全量を確実に捕捉する。
sleep 1

./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 100 --duration-sec 60 --log-path "$TX_LOG"

# 受信側終了待ち
wait "$RX_PID" || true

echo "[INFO] finished"
echo "[INFO] logs:"
ls -l "$RUN_DIR"