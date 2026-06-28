#!/usr/bin/env bash
#
# run_socket_buffer_matrix.sh
#
# W08-7 / Issue #131:
# send interval × SO_RCVBUF size の matrix 計測を Pi5 上で実行する。
#
# 方針:
# - #130 の send interval 結果を受けて、低〜中負荷の代表 rate を見る
# - socket buffer は SO_RCVBUF のみ変更する
# - requested value と getsockopt() actual value を rx.log / metadata に残す
# - それ以外の条件は W08 baseline / send interval sweep と揃える

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ROOT="data/w08/socket_buffer_matrix"
LOG_ROOT="logs/w08/socket_buffer_matrix"

RATES=(10000 14000 18000)
RCVBUFS=(8192 16384 32768 49152 65536 98304)
TRIALS=(1 2 3)

BIND_IP="${BIND_IP:-127.0.0.1}"
DST_IP="${DST_IP:-127.0.0.1}"
PORT="${PORT:-9000}"
TX_DURATION_SEC="${TX_DURATION_SEC:-10}"
RX_DURATION_SEC="${RX_DURATION_SEC:-12}"
PAYLOAD_LEN="${PAYLOAD_LEN:-48}"
RECOVERY_MODE="${RECOVERY_MODE:-fsm}"
START_DELAY_SEC="${START_DELAY_SEC:-1}"

mkdir -p "$RUN_ROOT" "$LOG_ROOT"

if [ ! -x ./bin/tx ] || [ ! -x ./bin/rx ]; then
  make -j4
fi

: > "$RUN_ROOT/run_metadata.md"

{
  echo "date=$(date --iso-8601=seconds)"
  echo "host=$(uname -a)"
  echo "branch=$(git branch --show-current)"
  echo "commit=$(git rev-parse HEAD)"
  echo "lo=$(ip -brief address show lo 2>/dev/null | tr '\n' ' ')"
  echo "socket_buf_defaults=$(sysctl -n net.core.wmem_default)/$(sysctl -n net.core.rmem_default)"
  echo "purpose=socket_buffer_matrix_sweep"
  echo "buffer_option=SO_RCVBUF"
  echo "rates=${RATES[*]}"
  echo "requested_rcvbufs=${RCVBUFS[*]}"
  echo "trials=${TRIALS[*]}"
  echo "fixed_conditions=loopback ${BIND_IP}:${PORT} payload_len=${PAYLOAD_LEN} tx_duration_sec=${TX_DURATION_SEC} rx_duration_sec=${RX_DURATION_SEC} recovery_mode=${RECOVERY_MODE} no_affinity sndbuf_default"
  echo
} >> "$RUN_ROOT/run_metadata.md"

for rate in "${RATES[@]}"; do
  for rcvbuf in "${RCVBUFS[@]}"; do
    for trial in "${TRIALS[@]}"; do
      run_dir="$LOG_ROOT/rate_${rate}_rcvbuf_${rcvbuf}_trial${trial}"
      out_csv="$RUN_ROOT/rate_${rate}_rcvbuf_${rcvbuf}_run${trial}.csv"

      mkdir -p "$run_dir"
      rm -f "$out_csv"

      rx_cmd=(./bin/rx
        --bind-ip "$BIND_IP"
        --port "$PORT"
        --duration-sec "$RX_DURATION_SEC"
        --log-path "$run_dir/rx.log"
        --rcvbuf "$rcvbuf"
        --link-name w08_socket_buffer_matrix
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

      {
        echo "rate_hz=$rate"
        echo "rcvbuf_requested=$rcvbuf"
        echo "trial=$trial"
        echo "time=$(date --iso-8601=seconds)"
        echo "run_dir=$run_dir"
        echo "rx_csv=$out_csv"
        printf 'rx_cmd='
        printf '%q ' "${rx_cmd[@]}"
        printf '\n'
        printf 'tx_cmd='
        printf '%q ' "${tx_cmd[@]}"
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

      rcvbuf_line="$(grep -E 'socket buffer option=SO_RCVBUF' "$run_dir/rx.log" | tail -n 1 || true)"
      rcvbuf_actual="$(printf '%s\n' "$rcvbuf_line" | sed -n 's/.* actual=\([0-9][0-9]*\).*/\1/p')"

      run_validity=ok
      if [ "$tx_status" -ne 0 ] || [ "$rx_status" -ne 0 ] || [ "$copy_status" -ne 0 ] || [ -z "$rcvbuf_actual" ]; then
        run_validity=invalid
      fi

      {
        echo "tx_status=$tx_status"
        echo "rx_status=$rx_status"
        echo "copy_status=$copy_status"
        echo "rcvbuf_line=$rcvbuf_line"
        echo "rcvbuf_actual=$rcvbuf_actual"
        echo "run_validity=$run_validity"
        echo
      } >> "$RUN_ROOT/run_metadata.md"
    done
  done
done

find "$RUN_ROOT" -maxdepth 1 -type f -name 'rate_*_rcvbuf_*_run*.csv' -print | sort

