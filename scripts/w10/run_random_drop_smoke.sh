#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

make -j4

OUT_DIR=${OUT_DIR:-/tmp/w10_random_drop_smoke}
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

run_case() {
  local name=$1
  local port=$2
  local drop_rate=$3
  local seed=$4

  local rx_log="$OUT_DIR/${name}_rx.log"
  local tx_log="$OUT_DIR/${name}_tx.log"
  local rx_csv="$OUT_DIR/${name}_rx_by_1recv.csv"

  ./bin/rx \
    --bind-ip 127.0.0.1 \
    --port "$port" \
    --duration-sec 4 \
    --log-path "$rx_log" \
    --csv-by-1recv-log-path "$rx_csv" \
    > "$OUT_DIR/${name}_rx.out" 2>&1 &
  local rx_pid=$!

  sleep 0.3

  ./bin/tx \
    --dst-ip 127.0.0.1 \
    --dst-port "$port" \
    --rate-hz 600 \
    --duration-sec 2 \
    --log-path "$tx_log" \
    --drop-rate "$drop_rate" \
    --drop-seed "$seed" \
    --drop-target datagram \
    > "$OUT_DIR/${name}_tx.out" 2>&1

  wait "$rx_pid"

  echo "=== $name tx summary ==="
  grep "tx summary" "$tx_log"
  echo "=== $name rx summary ==="
  grep "rx summary" "$rx_log"
}

run_case drop0 23301 0.0 123
run_case drop20 23302 0.20 123

grep -q "dropped_datagrams=0" "$OUT_DIR/drop0_tx.log"
grep -q "dropped_frames=0" "$OUT_DIR/drop0_tx.log"

drop20_datagrams=$(grep "tx summary" "$OUT_DIR/drop20_tx.log" | sed -n 's/.*dropped_datagrams=\([0-9][0-9]*\).*/\1/p')
drop20_frames=$(grep "tx summary" "$OUT_DIR/drop20_tx.log" | sed -n 's/.*dropped_frames=\([0-9][0-9]*\).*/\1/p')
drop20_gap=$(grep "rx summary" "$OUT_DIR/drop20_rx.log" | sed -n 's/.*gap_cnt=\([0-9][0-9]*\).*/\1/p')

if [ "${drop20_datagrams:-0}" -le 0 ]; then
  echo "expected dropped_datagrams > 0" >&2
  exit 1
fi
if [ "${drop20_frames:-0}" -le 0 ]; then
  echo "expected dropped_frames > 0" >&2
  exit 1
fi
if [ "${drop20_gap:-0}" -le 0 ]; then
  echo "expected rx gap_cnt > 0" >&2
  exit 1
fi

echo "PASS: W10 random drop smoke"