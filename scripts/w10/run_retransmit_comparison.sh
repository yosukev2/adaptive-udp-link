#!/usr/bin/env bash
set -euo pipefail

RATE_HZ=${RATE_HZ:-120000}
TX_DURATION_SEC=${TX_DURATION_SEC:-30}
RX_DURATION_SEC=${RX_DURATION_SEC:-32}
DATA_PORT=${DATA_PORT:-22001}
FEEDBACK_PORT=${FEEDBACK_PORT:-22000}
TRIALS=${TRIALS:-"1 2 3"}
RX_CORE=${RX_CORE:-2}
TX_CORE=${TX_CORE:-3}
RETRANSMIT_BUFFER_DATAGRAMS=${RETRANSMIT_BUFFER_DATAGRAMS:-262144}
RETRANSMIT_MAX_DATAGRAMS_PER_FEEDBACK=${RETRANSMIT_MAX_DATAGRAMS_PER_FEEDBACK:-4096}
DATA_DIR=${DATA_DIR:-"data/w10/retransmit"}
LOG_DIR=${LOG_DIR:-"logs/w10/retransmit"}

mkdir -p "$DATA_DIR" "$LOG_DIR"
: > "$DATA_DIR/run_metadata.md"

{
  echo "# W10 retransmit comparison metadata"
  echo
  echo "- date: $(date --iso-8601=seconds)"
  echo "- host: $(uname -a)"
  echo "- branch: $(git branch --show-current 2>/dev/null || echo unknown)"
  echo "- commit: $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "- rate_hz: $RATE_HZ"
  echo "- tx_duration_sec: $TX_DURATION_SEC"
  echo "- rx_duration_sec: $RX_DURATION_SEC"
  echo "- data_port: $DATA_PORT"
  echo "- feedback_port: $FEEDBACK_PORT"
  echo "- trials: $TRIALS"
  echo "- rx_core: $RX_CORE"
  echo "- tx_core: $TX_CORE"
  echo "- retransmit_buffer_datagrams: $RETRANSMIT_BUFFER_DATAGRAMS"
  echo "- retransmit_max_datagrams_per_feedback: $RETRANSMIT_MAX_DATAGRAMS_PER_FEEDBACK"
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
      echo "- rx_cmd: taskset -c $RX_CORE ./bin/rx --bind-ip 127.0.0.1 --port $DATA_PORT --duration-sec $RX_DURATION_SEC --log-path $rx_log --feedback-dst-ip 127.0.0.1 --feedback-dst-port $FEEDBACK_PORT --retransmit-request on --csv-in-1sec-log-path $rx_1sec --csv-by-1recv-log-path $rx_by_1recv"
      echo "- tx_cmd: taskset -c $TX_CORE ./bin/tx --dst-ip 127.0.0.1 --dst-port $DATA_PORT --rate-hz $RATE_HZ --duration-sec $TX_DURATION_SEC --log-path $tx_log --feedback-bind-ip 127.0.0.1 --feedback-bind-port $FEEDBACK_PORT --adaptive-log-path $adaptive_log --adaptive-mode off --retransmit-mode $mode --retransmit-buffer-datagrams $RETRANSMIT_BUFFER_DATAGRAMS --retransmit-max-datagrams-per-feedback $RETRANSMIT_MAX_DATAGRAMS_PER_FEEDBACK"
      echo
    } >> "$DATA_DIR/run_metadata.md"

    taskset -c "$RX_CORE" ./bin/rx \
      --bind-ip 127.0.0.1 \
      --port "$DATA_PORT" \
      --duration-sec "$RX_DURATION_SEC" \
      --log-path "$rx_log" \
      --feedback-dst-ip 127.0.0.1 \
      --feedback-dst-port "$FEEDBACK_PORT" \
      --retransmit-request on \
      --csv-in-1sec-log-path "$rx_1sec" \
      --csv-by-1recv-log-path "$rx_by_1recv" \
      > "$run_dir/rx.stdout" 2> "$run_dir/rx.stderr" &
    rx_pid=$!

    sleep 0.5

    set +e
    taskset -c "$TX_CORE" ./bin/tx \
      --dst-ip 127.0.0.1 \
      --dst-port "$DATA_PORT" \
      --rate-hz "$RATE_HZ" \
      --duration-sec "$TX_DURATION_SEC" \
      --log-path "$tx_log" \
      --feedback-bind-ip 127.0.0.1 \
      --feedback-bind-port "$FEEDBACK_PORT" \
      --adaptive-log-path "$adaptive_log" \
      --adaptive-mode off \
      --retransmit-mode "$mode" \
      --retransmit-buffer-datagrams "$RETRANSMIT_BUFFER_DATAGRAMS" \
      --retransmit-max-datagrams-per-feedback "$RETRANSMIT_MAX_DATAGRAMS_PER_FEEDBACK" \
      > "$run_dir/tx.stdout" 2> "$run_dir/tx.stderr"
    tx_status=$?

    wait "$rx_pid"
    rx_status=$?
    set -e

    cp "$rx_by_1recv" "$DATA_DIR/${mode}_run${trial}_rx_by_1recv.csv"
    cp "$rx_1sec" "$DATA_DIR/${mode}_run${trial}_rx_1sec.csv"
    cp "$adaptive_log" "$DATA_DIR/${mode}_run${trial}_adaptive_log.csv"

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

find "$DATA_DIR" -maxdepth 1 -type f -print | sort
