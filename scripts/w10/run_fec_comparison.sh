#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

RATE_HZ=${RATE_HZ:-1200}
DROP_RATE=${DROP_RATE:-0.10}
DROP_SEEDS=${DROP_SEEDS:-"101 102 103 104 105 106 107 108 109 110"}
TX_DURATION_SEC=${TX_DURATION_SEC:-30}
RX_DURATION_SEC=${RX_DURATION_SEC:-32}
DATA_PORT=${DATA_PORT:-24001}
TRIALS=${TRIALS:-"1 2 3 4 5 6 7 8 9 10"}
RX_CORE=${RX_CORE:-2}
TX_CORE=${TX_CORE:-3}
DATA_DIR=${DATA_DIR:-"data/w10/fec_comparison"}
LOG_DIR=${LOG_DIR:-"logs/w10/fec_comparison"}
SUMMARY_CSV=${SUMMARY_CSV:-"$DATA_DIR/fec_comparison.csv"}
REPORT=${REPORT:-"reports/w10_fec_comparison_summary.md"}
RX_BY_1RECV=${RX_BY_1RECV:-1}

mkdir -p "$DATA_DIR" "$LOG_DIR"
: > "$DATA_DIR/run_metadata.md"

make -j4

{
  echo "# W10 random_drop + XOR FEC comparison metadata"
  echo
  echo "- date: $(date --iso-8601=seconds)"
  echo "- host: $(uname -a)"
  echo "- branch: $(git branch --show-current 2>/dev/null || echo unknown)"
  echo "- commit: $(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "- rate_hz: $RATE_HZ"
  echo "- drop_rate: $DROP_RATE"
  echo "- drop_seeds: $DROP_SEEDS"
  echo "- tx_duration_sec: $TX_DURATION_SEC"
  echo "- rx_duration_sec: $RX_DURATION_SEC"
  echo "- data_port: $DATA_PORT"
  echo "- trials: $TRIALS"
  echo "- rx_core: $RX_CORE"
  echo "- tx_core: $TX_CORE"
  echo "- data_dir: $DATA_DIR"
  echo "- log_dir: $LOG_DIR"
  echo "- rx_by_1recv: $RX_BY_1RECV"
  echo
  echo "## 固定条件"
  echo
  echo "- loopback: 127.0.0.1"
  echo "- payload_len: 48"
  echo "- FEC ON: tx/rx both --fec-mode xor"
  echo "- FEC OFF: tx/rx both --fec-mode off"
  echo "- random drop target: datagram"
  echo "- 同じtrial番号ではFEC OFF/ONで同じdrop_seedを使う"
  echo
} >> "$DATA_DIR/run_metadata.md"

seed_for_trial() {
  local trial=$1
  local idx=1
  local seed
  for seed in $DROP_SEEDS; do
    if [ "$idx" -eq "$trial" ]; then
      echo "$seed"
      return 0
    fi
    idx=$((idx + 1))
  done
  echo "ERROR: no drop seed for trial=$trial" >&2
  return 1
}

for mode in off xor; do
  for trial in $TRIALS; do
    seed=$(seed_for_trial "$trial")
    run_dir="$LOG_DIR/fec_${mode}_trial${trial}"
    mkdir -p "$run_dir"

    rx_log="$run_dir/rx.log"
    tx_log="$run_dir/tx.log"
    rx_1sec="$run_dir/rx_1sec.csv"
    rx_by_1recv="$run_dir/rx_by_1recv.csv"
    rx_by_1recv_args=()
    rx_by_1recv_cmd_suffix=""
    if [ "$RX_BY_1RECV" != "0" ]; then
      rx_by_1recv_args=(--csv-by-1recv-log-path "$rx_by_1recv")
      rx_by_1recv_cmd_suffix=" --csv-by-1recv-log-path $rx_by_1recv"
    fi

    {
      echo "## fec_mode=$mode trial=$trial"
      echo
      echo "- time: $(date --iso-8601=seconds)"
      echo "- seed: $seed"
      echo "- run_dir: $run_dir"
      echo "- rx_cmd: taskset -c $RX_CORE ./bin/rx --bind-ip 127.0.0.1 --port $DATA_PORT --duration-sec $RX_DURATION_SEC --log-path $rx_log --link-name w10_fec_comparison --trial $trial --fec-mode $mode --csv-in-1sec-log-path $rx_1sec${rx_by_1recv_cmd_suffix}"
      echo "- tx_cmd: taskset -c $TX_CORE ./bin/tx --dst-ip 127.0.0.1 --dst-port $DATA_PORT --rate-hz $RATE_HZ --duration-sec $TX_DURATION_SEC --log-path $tx_log --payload-len 48 --version 1 --fec-mode $mode --drop-rate $DROP_RATE --drop-seed $seed --drop-target datagram"
      echo
    } >> "$DATA_DIR/run_metadata.md"

    taskset -c "$RX_CORE" ./bin/rx \
      --bind-ip 127.0.0.1 \
      --port "$DATA_PORT" \
      --duration-sec "$RX_DURATION_SEC" \
      --log-path "$rx_log" \
      --link-name w10_fec_comparison \
      --trial "$trial" \
      --fec-mode "$mode" \
      --csv-in-1sec-log-path "$rx_1sec" \
      "${rx_by_1recv_args[@]}" \
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
      --payload-len 48 \
      --version 1 \
      --fec-mode "$mode" \
      --drop-rate "$DROP_RATE" \
      --drop-seed "$seed" \
      --drop-target datagram \
      > "$run_dir/tx.stdout" 2> "$run_dir/tx.stderr"
    tx_status=$?

    wait "$rx_pid"
    rx_status=$?
    set -e

    if [ "$RX_BY_1RECV" != "0" ]; then
      cp "$rx_by_1recv" "$DATA_DIR/fec_${mode}_run${trial}_rx_by_1recv.csv"
    fi
    cp "$rx_1sec" "$DATA_DIR/fec_${mode}_run${trial}_rx_1sec.csv"

    {
      echo "- tx_status: $tx_status"
      echo "- rx_status: $rx_status"
      echo
    } >> "$DATA_DIR/run_metadata.md"

    if [ "$tx_status" -ne 0 ] || [ "$rx_status" -ne 0 ]; then
      echo "ERROR: fec_mode=$mode trial=$trial tx_status=$tx_status rx_status=$rx_status" >&2
      exit 1
    fi
  done
done

find "$DATA_DIR" -maxdepth 1 -type f -print | sort

python3 scripts/analyze_w10_fec_comparison.py \
  --log-dir "$LOG_DIR" \
  --metadata "$DATA_DIR/run_metadata.md" \
  --summary-csv "$SUMMARY_CSV" \
  --report "$REPORT"

echo "summary_csv=$SUMMARY_CSV"
echo "report=$REPORT"
