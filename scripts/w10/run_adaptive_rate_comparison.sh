#!/usr/bin/env bash
set -euo pipefail

INITIAL_RATE_HZ=${INITIAL_RATE_HZ:-1000}
TX_DURATION_SEC=${TX_DURATION_SEC:-30}
RX_DURATION_SEC=${RX_DURATION_SEC:-32}
DATA_PORT=${DATA_PORT:-20001}
FEEDBACK_PORT=${FEEDBACK_PORT:-20000}
TRIALS=${TRIALS:-"1 2 3"}
ADAPTIVE_MIN_RATE_HZ=${ADAPTIVE_MIN_RATE_HZ:-1000}
ADAPTIVE_MAX_RATE_HZ=${ADAPTIVE_MAX_RATE_HZ:-500000}
ADAPTIVE_HIGH_LATENCY_MS=${ADAPTIVE_HIGH_LATENCY_MS:-0}

DATA_DIR=${DATA_DIR:-"data/w10/adaptive_rate"}
LOG_DIR=${LOG_DIR:-"logs/w10/adaptive_rate"}

mkdir -p "$DATA_DIR" "$LOG_DIR"
: > "$DATA_DIR/run_metadata.md"

{
  echo "# W10 adaptive rate comparison metadata"
  echo
  echo "- date: $(date --iso-8601=seconds)"
  echo "- host: $(uname -a)"
  echo "- branch: $(git branch --show-current)"
  echo "- commit: $(git rev-parse HEAD)"
  echo "- initial_rate_hz: $INITIAL_RATE_HZ"
  echo "- tx_duration_sec: $TX_DURATION_SEC"
  echo "- rx_duration_sec: $RX_DURATION_SEC"
  echo "- data_port: $DATA_PORT"
  echo "- feedback_port: $FEEDBACK_PORT"
  echo "- adaptive_min_rate_hz: $ADAPTIVE_MIN_RATE_HZ"
  echo "- adaptive_max_rate_hz: $ADAPTIVE_MAX_RATE_HZ"
  echo "- adaptive_high_latency_ms: $ADAPTIVE_HIGH_LATENCY_MS"
  echo "- trials: $TRIALS"
  echo
} >> "$DATA_DIR/run_metadata.md"

for mode in off on; do
  for trial in $TRIALS; do
    run_dir="$LOG_DIR/${mode}_trial${trial}"
    mkdir -p "$run_dir"

    rx_log="$run_dir/rx.log"
    tx_log="$run_dir/tx.log"
    rx_1sec="$run_dir/rx_1sec.csv"
    rx_by_1recv="$run_dir/rx_by_1recv.csv"
    adaptive_log="$run_dir/adaptive_log.csv"

    {
      echo "## mode=$mode trial=$trial"
      echo
      echo "- time: $(date --iso-8601=seconds)"
      echo "- run_dir: $run_dir"
      echo "- rx_cmd: ./bin/rx --bind-ip 127.0.0.1 --port $DATA_PORT --duration-sec $RX_DURATION_SEC --log-path $rx_log --feedback-dst-ip 127.0.0.1 --feedback-dst-port $FEEDBACK_PORT --csv-in-1sec-log-path $rx_1sec --csv-by-1recv-log-path $rx_by_1recv"
      echo "- tx_cmd: ./bin/tx --dst-ip 127.0.0.1 --dst-port $DATA_PORT --rate-hz $INITIAL_RATE_HZ --duration-sec $TX_DURATION_SEC --log-path $tx_log --feedback-bind-ip 127.0.0.1 --feedback-bind-port $FEEDBACK_PORT --adaptive-log-path $adaptive_log --adaptive-mode $mode --adaptive-min-rate-hz $ADAPTIVE_MIN_RATE_HZ --adaptive-max-rate-hz $ADAPTIVE_MAX_RATE_HZ --adaptive-high-latency-ms $ADAPTIVE_HIGH_LATENCY_MS"
      echo
    } >> "$DATA_DIR/run_metadata.md"

    ./bin/rx \
      --bind-ip 127.0.0.1 \
      --port "$DATA_PORT" \
      --duration-sec "$RX_DURATION_SEC" \
      --log-path "$rx_log" \
      --feedback-dst-ip 127.0.0.1 \
      --feedback-dst-port "$FEEDBACK_PORT" \
      --csv-in-1sec-log-path "$rx_1sec" \
      --csv-by-1recv-log-path "$rx_by_1recv" \
      > "$run_dir/rx.stdout" 2> "$run_dir/rx.stderr" &
    rx_pid=$!

    sleep 0.5

    set +e
    ./bin/tx \
      --dst-ip 127.0.0.1 \
      --dst-port "$DATA_PORT" \
      --rate-hz "$INITIAL_RATE_HZ" \
      --duration-sec "$TX_DURATION_SEC" \
      --log-path "$tx_log" \
      --feedback-bind-ip 127.0.0.1 \
      --feedback-bind-port "$FEEDBACK_PORT" \
      --adaptive-log-path "$adaptive_log" \
      --adaptive-mode "$mode" \
      --adaptive-min-rate-hz "$ADAPTIVE_MIN_RATE_HZ" \
      --adaptive-max-rate-hz "$ADAPTIVE_MAX_RATE_HZ" \
      --adaptive-high-latency-ms "$ADAPTIVE_HIGH_LATENCY_MS" \
      > "$run_dir/tx.stdout" 2> "$run_dir/tx.stderr"
    tx_status=$?

    wait "$rx_pid"
    rx_status=$?
    set -e

    if [ -f "$rx_by_1recv" ]; then
      cp "$rx_by_1recv" "$DATA_DIR/${mode}_run${trial}_rx_by_1recv.csv"
    fi
    if [ -f "$rx_1sec" ]; then
      cp "$rx_1sec" "$DATA_DIR/${mode}_run${trial}_rx_1sec.csv"
    fi
    if [ -f "$adaptive_log" ]; then
      cp "$adaptive_log" "$DATA_DIR/${mode}_run${trial}_adaptive_log.csv"
    fi

    {
      echo "- tx_status: $tx_status"
      echo "- rx_status: $rx_status"
      echo
    } >> "$DATA_DIR/run_metadata.md"

    if [ "$tx_status" -ne 0 ] || [ "$rx_status" -ne 0 ]; then
      echo "ERROR: mode=$mode trial=$trial tx_status=$tx_status rx_status=$rx_status" >&2
      exit 1
    fi
  done
done

echo
echo "=== generated data files ==="
find "$DATA_DIR" -maxdepth 1 -type f -print | sort

echo
echo "=== adaptive log preview ==="
for f in "$DATA_DIR"/*_adaptive_log.csv; do
  echo "=== $f ==="
  head -n 5 "$f"
  tail -n 5 "$f"
done

echo
echo "=== rate change lines ==="
grep -R "increase\|decrease\|set_rate" "$DATA_DIR"/*_adaptive_log.csv || true

echo
echo "DONE"
