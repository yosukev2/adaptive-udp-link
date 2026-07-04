#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

make -j4

OUT_DIR=${OUT_DIR:-/tmp/w10_fec_smoke}
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

run_case() {
  local name=$1
  local rx_fec=$2
  local tx_fec=$3
  local drop_every=$4
  local port=$5

  local rx_log="$OUT_DIR/${name}_rx.log"
  local tx_log="$OUT_DIR/${name}_tx.log"
  local rx_csv="$OUT_DIR/${name}_rx_by_1recv.csv"

  ./bin/rx \
    --bind-ip 127.0.0.1 \
    --port "$port" \
    --duration-sec 4 \
    --log-path "$rx_log" \
    --fec-mode "$rx_fec" \
    --csv-by-1recv-log-path "$rx_csv" \
    > "$OUT_DIR/${name}_rx.out" 2>&1 &
  local rx_pid=$!

  sleep 0.3

  ./bin/tx \
    --dst-ip 127.0.0.1 \
    --dst-port "$port" \
    --rate-hz 120 \
    --duration-sec 2 \
    --log-path "$tx_log" \
    --fec-mode "$tx_fec" \
    --drop-datagram-every "$drop_every" \
    > "$OUT_DIR/${name}_tx.out" 2>&1

  wait "$rx_pid"

  echo "=== $name rx summary ==="
  grep "rx summary" "$rx_log"
  echo "=== $name tx summary ==="
  grep "tx summary" "$tx_log"
}

run_case fec_off_drop4 off off 4 23101
run_case fec_xor_drop4 xor xor 4 23102
run_case fec_xor_drop2 xor xor 2 23103

grep -q "effective_missing_total=60" "$OUT_DIR/fec_off_drop4_rx.log"
grep -q "fec_raw_missing_frames=60 recovered_by_fec_count=60" "$OUT_DIR/fec_xor_drop4_rx.log"
grep -q "fec_effective_missing_total=0" "$OUT_DIR/fec_xor_drop4_rx.log"
grep -q "fec_raw_missing_frames=120 recovered_by_fec_count=0 unrecovered_by_fec_count=120" "$OUT_DIR/fec_xor_drop2_rx.log"

echo "PASS: W10 FEC smoke"