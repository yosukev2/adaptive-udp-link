#!/usr/bin/env bash
#
# run_cpu_affinity_matrix.sh
#
# W08 / Issue #132:
# Sweep RX/TX CPU affinity on/off and rate_hz.
#
# Matrix:
# - RX affinity: off / on
# - TX affinity: off / on
# - rate_hz: 5000 / 10000 / 50000 / 100000 / 500000
# - trials: 1 / 2 / 3
# - total: 60 runs
#
# Defaults:
# - RX pinned core: 0
# - TX pinned core: 1
# Override with RX_CORE=<n> TX_CORE=<n>.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ROOT="data/w08/cpu_affinity_matrix"
LOG_ROOT="logs/w08/cpu_affinity_matrix"

RATES=(5000 10000 50000 100000 500000)
PIN_OPTIONS=(off on)
TRIALS=(1 2 3)

BIND_IP="${BIND_IP:-127.0.0.1}"
DST_IP="${DST_IP:-127.0.0.1}"
PORT="${PORT:-9000}"
TX_DURATION_SEC="${TX_DURATION_SEC:-10}"
RX_DURATION_SEC="${RX_DURATION_SEC:-12}"
PAYLOAD_LEN="${PAYLOAD_LEN:-48}"
RECOVERY_MODE="${RECOVERY_MODE:-fsm}"
START_DELAY_SEC="${START_DELAY_SEC:-1}"
RX_CORE="${RX_CORE:-0}"
TX_CORE="${TX_CORE:-1}"

mkdir -p "$RUN_ROOT" "$LOG_ROOT"

if [ ! -x ./bin/tx ] || [ ! -x ./bin/rx ]; then
  make -j4
fi

if ! command -v taskset >/dev/null 2>&1; then
  echo "[ERROR] taskset is required but not found" >&2
  exit 1
fi

: > "$RUN_ROOT/run_metadata.md"

{
  echo "date=$(date --iso-8601=seconds)"
  echo "host=$(uname -a)"
  echo "branch=$(git branch --show-current)"
  echo "commit=$(git rev-parse HEAD)"
  echo "lo=$(ip -brief address show lo 2>/dev/null | tr '\n' ' ')"
  echo "purpose=cpu_affinity_matrix"
  echo "matrix_rates=${RATES[*]}"
  echo "matrix_rx_pin=${PIN_OPTIONS[*]}"
  echo "matrix_tx_pin=${PIN_OPTIONS[*]}"
  echo "rx_core=${RX_CORE}"
  echo "tx_core=${TX_CORE}"
  echo "trials=${TRIALS[*]}"
  echo "fixed_conditions=loopback ${BIND_IP}:${PORT} payload_len=${PAYLOAD_LEN} tx_duration_sec=${TX_DURATION_SEC} rx_duration_sec=${RX_DURATION_SEC} recovery_mode=${RECOVERY_MODE} socket_buffer_default no_socket_buffer_tuning"
  echo
} >> "$RUN_ROOT/run_metadata.md"

quote_cmd() {
  local arg
  for arg in "$@"; do
    printf '%q ' "$arg"
  done
}

for rate in "${RATES[@]}"; do
  for rx_pin in "${PIN_OPTIONS[@]}"; do
    for tx_pin in "${PIN_OPTIONS[@]}"; do
      for trial in "${TRIALS[@]}"; do
        run_dir="$LOG_ROOT/rate_${rate}_rxpin_${rx_pin}_txpin_${tx_pin}_trial${trial}"
        out_csv="$RUN_ROOT/rate_${rate}_rxpin_${rx_pin}_txpin_${tx_pin}_run${trial}.csv"

        mkdir -p "$run_dir"
        rm -f "$out_csv"

        rx_cmd=(./bin/rx
          --bind-ip "$BIND_IP"
          --port "$PORT"
          --duration-sec "$RX_DURATION_SEC"
          --log-path "$run_dir/rx.log"
          --link-name w08_cpu_affinity_matrix
          --trial "$trial"
          --csv-in-1sec-log-path "$run_dir/rx_1sec.csv"
          --csv-by-1recv-log-path "$run_dir/rx_by_1recv.csv"
          --recovery-mode "$RECOVERY_MODE")

        tx_cmd=(./bin/tx
          --dst-ip "$DST_IP"
          --dst-port "$PORT"
          --rate-hz "$rate"
          --duration-sec "$TX_DURATION_SEC"
          --log-path "$run_dir/tx.log"
          --payload-len "$PAYLOAD_LEN"
          --version 1)

        if [ "$rx_pin" = "on" ]; then
          rx_cmd=(taskset -c "$RX_CORE" "${rx_cmd[@]}")
        fi
        if [ "$tx_pin" = "on" ]; then
          tx_cmd=(taskset -c "$TX_CORE" "${tx_cmd[@]}")
        fi

        {
          echo "rate_hz=$rate"
          echo "rx_pin=$rx_pin"
          echo "tx_pin=$tx_pin"
          echo "rx_core=$RX_CORE"
          echo "tx_core=$TX_CORE"
          echo "trial=$trial"
          echo "time=$(date --iso-8601=seconds)"
          echo "run_dir=$run_dir"
          echo "rx_csv=$out_csv"
          printf 'rx_cmd='
          quote_cmd "${rx_cmd[@]}"
          printf '\n'
          printf 'tx_cmd='
          quote_cmd "${tx_cmd[@]}"
          printf '\n'
        } >> "$RUN_ROOT/run_metadata.md"

        "${rx_cmd[@]}" &
        rx_pid=$!

        sleep "$START_DELAY_SEC"

        set +e
        "${tx_cmd[@]}"
        tx_status=$?

        wait "$rx_pid"
        rx_status=$?
        set -e

        copy_status=0
        if [ -f "$run_dir/rx_by_1recv.csv" ]; then
          cp "$run_dir/rx_by_1recv.csv" "$out_csv"
        else
          copy_status=1
        fi

        rx_effective_core="default"
        tx_effective_core="default"
        if [ "$rx_pin" = "on" ]; then
          rx_effective_core="$RX_CORE"
        fi
        if [ "$tx_pin" = "on" ]; then
          tx_effective_core="$TX_CORE"
        fi

        run_validity=ok
        if [ "$tx_status" -ne 0 ] || [ "$rx_status" -ne 0 ] || [ "$copy_status" -ne 0 ]; then
          run_validity=invalid
        fi

        {
          echo "tx_status=$tx_status"
          echo "rx_status=$rx_status"
          echo "copy_status=$copy_status"
          echo "rx_effective_core=$rx_effective_core"
          echo "tx_effective_core=$tx_effective_core"
          echo "run_validity=$run_validity"
          echo
        } >> "$RUN_ROOT/run_metadata.md"
      done
    done
  done
done

find "$RUN_ROOT" -maxdepth 1 -type f -name 'rate_*_rxpin_*_txpin_*_run*.csv' -print | sort
