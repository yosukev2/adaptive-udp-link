#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

make -j4

OUT_DIR=${OUT_DIR:-/tmp/w10_adaptive_fec_smoke}
RATE_HZ=${RATE_HZ:-1200}
TX_DURATION_SEC=${TX_DURATION_SEC:-10}
RX_DURATION_SEC=${RX_DURATION_SEC:-12}
DATA_PORT=${DATA_PORT:-23201}
FEEDBACK_PORT=${FEEDBACK_PORT:-23200}
DROP_DATAGRAM_EVERY=${DROP_DATAGRAM_EVERY:-4}
ADAPTIVE_FEC_STABLE_WINDOWS=${ADAPTIVE_FEC_STABLE_WINDOWS:-2}
ADAPTIVE_FEC_HIGH_MISSING_RATE=${ADAPTIVE_FEC_HIGH_MISSING_RATE:-0.001}
ADAPTIVE_FEC_LOW_MISSING_RATE=${ADAPTIVE_FEC_LOW_MISSING_RATE:-0.0}

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

rx_log="$OUT_DIR/rx.log"
tx_log="$OUT_DIR/tx.log"
adaptive_log="$OUT_DIR/adaptive_fec.csv"
rx_1sec="$OUT_DIR/rx_1sec.csv"
rx_by_1recv="$OUT_DIR/rx_by_1recv.csv"

{
  echo "# W10 adaptive FEC smoke metadata"
  echo "- date: $(date --iso-8601=seconds)"
  echo "- branch: $(git branch --show-current 2>/dev/null || echo unknown)"
  echo "- commit: $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "- rate_hz: $RATE_HZ"
  echo "- tx_duration_sec: $TX_DURATION_SEC"
  echo "- rx_duration_sec: $RX_DURATION_SEC"
  echo "- drop_datagram_every: $DROP_DATAGRAM_EVERY"
  echo "- adaptive_fec_stable_windows: $ADAPTIVE_FEC_STABLE_WINDOWS"
  echo "- adaptive_fec_high_missing_rate: $ADAPTIVE_FEC_HIGH_MISSING_RATE"
  echo "- adaptive_fec_low_missing_rate: $ADAPTIVE_FEC_LOW_MISSING_RATE"
  echo "- rx_cmd: ./bin/rx --bind-ip 127.0.0.1 --port $DATA_PORT --duration-sec $RX_DURATION_SEC --log-path $rx_log --fec-mode xor --feedback-dst-ip 127.0.0.1 --feedback-dst-port $FEEDBACK_PORT --csv-in-1sec-log-path $rx_1sec --csv-by-1recv-log-path $rx_by_1recv"
  echo "- tx_cmd: ./bin/tx --dst-ip 127.0.0.1 --dst-port $DATA_PORT --rate-hz $RATE_HZ --duration-sec $TX_DURATION_SEC --log-path $tx_log --feedback-bind-ip 127.0.0.1 --feedback-bind-port $FEEDBACK_PORT --adaptive-log-path $adaptive_log --adaptive-mode off --fec-mode off --adaptive-fec on --adaptive-fec-high-missing-rate $ADAPTIVE_FEC_HIGH_MISSING_RATE --adaptive-fec-low-missing-rate $ADAPTIVE_FEC_LOW_MISSING_RATE --adaptive-fec-stable-windows $ADAPTIVE_FEC_STABLE_WINDOWS --drop-datagram-every $DROP_DATAGRAM_EVERY"
} > "$OUT_DIR/run_metadata.md"

./bin/rx \
  --bind-ip 127.0.0.1 \
  --port "$DATA_PORT" \
  --duration-sec "$RX_DURATION_SEC" \
  --log-path "$rx_log" \
  --fec-mode xor \
  --feedback-dst-ip 127.0.0.1 \
  --feedback-dst-port "$FEEDBACK_PORT" \
  --csv-in-1sec-log-path "$rx_1sec" \
  --csv-by-1recv-log-path "$rx_by_1recv" \
  > "$OUT_DIR/rx.out" 2>&1 &
rx_pid=$!

sleep 0.3

./bin/tx \
  --dst-ip 127.0.0.1 \
  --dst-port "$DATA_PORT" \
  --rate-hz "$RATE_HZ" \
  --duration-sec "$TX_DURATION_SEC" \
  --log-path "$tx_log" \
  --feedback-bind-ip 127.0.0.1 \
  --feedback-bind-port "$FEEDBACK_PORT" \
  --adaptive-log-path "$adaptive_log" \
  --adaptive-mode off \
  --fec-mode off \
  --adaptive-fec on \
  --adaptive-fec-high-missing-rate "$ADAPTIVE_FEC_HIGH_MISSING_RATE" \
  --adaptive-fec-low-missing-rate "$ADAPTIVE_FEC_LOW_MISSING_RATE" \
  --adaptive-fec-stable-windows "$ADAPTIVE_FEC_STABLE_WINDOWS" \
  --drop-datagram-every "$DROP_DATAGRAM_EVERY" \
  > "$OUT_DIR/tx.out" 2>&1

tx_status=$?
wait "$rx_pid"
rx_status=$?

cat >> "$OUT_DIR/run_metadata.md" <<EOF
- tx_status: $tx_status
- rx_status: $rx_status
EOF

echo "=== adaptive log ==="
cat "$adaptive_log"
echo "=== rx summary ==="
grep "rx summary" "$rx_log"
echo "=== tx summary ==="
grep "tx summary" "$tx_log"

grep -q "enable_fec" "$adaptive_log"
grep -q "disable_fec" "$adaptive_log"
grep -q "hold" "$adaptive_log"
grep -q "old_fec_mode" "$adaptive_log"

echo "PASS: W10 adaptive FEC smoke"