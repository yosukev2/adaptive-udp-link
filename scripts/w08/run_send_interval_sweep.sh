#!/usr/bin/env bash
#
# run_send_interval_sweep.sh
#
# W08-6: send interval 変更条件の sweep を実行する。
# baseline と同じ loopback 条件を維持しつつ、--rate-hz だけを変えて
# 5 種類 × 3 trial を計測する。

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ROOT="data/w08/send_interval"
LOG_ROOT="logs/w08/send_interval"
SUMMARY_FILE="docs/w08/send_interval_summary.md"

RATES=(50 200 500 1000 10000)
TRIALS=(1 2 3)

mkdir -p "$RUN_ROOT" "$LOG_ROOT" docs/w08

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
  echo "summary_file=$SUMMARY_FILE"
  echo
} >> "$RUN_ROOT/run_metadata.md"

for rate in "${RATES[@]}"; do
  for trial in "${TRIALS[@]}"; do
    run_dir="$LOG_ROOT/rate_${rate}_trial${trial}"
    out_csv="$RUN_ROOT/rate_${rate}_run${trial}.csv"

    mkdir -p "$run_dir"
    rm -f "$out_csv"

    {
      echo "rate_hz=$rate"
      echo "trial=$trial"
      echo "time=$(date --iso-8601=seconds)"
      echo "run_dir=$run_dir"
      echo "rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path $run_dir/rx.log --link-name w08_send_interval --trial $trial --csv-in-1sec-log-path $run_dir/rx_1sec.csv --csv-by-1recv-log-path $run_dir/rx_by_1recv.csv --recovery-mode fsm"
      echo "tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz $rate --duration-sec 10 --log-path $run_dir/tx.log --payload-len 48 --version 1"
    } >> "$RUN_ROOT/run_metadata.md"

    ./bin/rx \
      --bind-ip 127.0.0.1 \
      --port 9000 \
      --duration-sec 12 \
      --log-path "$run_dir/rx.log" \
      --link-name w08_send_interval \
      --trial "$trial" \
      --csv-in-1sec-log-path "$run_dir/rx_1sec.csv" \
      --csv-by-1recv-log-path "$run_dir/rx_by_1recv.csv" \
      --recovery-mode fsm &
    rx_pid=$!

    sleep 1

    set +e
    ./bin/tx \
      --dst-ip 127.0.0.1 \
      --dst-port 9000 \
      --rate-hz "$rate" \
      --duration-sec 10 \
      --log-path "$run_dir/tx.log" \
      --payload-len 48 \
      --version 1
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

    run_validity=ok
    if [ "$tx_status" -ne 0 ] || [ "$rx_status" -ne 0 ] || [ "$copy_status" -ne 0 ]; then
      run_validity=invalid
    fi

    {
      echo "tx_status=$tx_status"
      echo "rx_status=$rx_status"
      echo "copy_status=$copy_status"
      echo "run_validity=$run_validity"
      echo "rx_csv=$out_csv"
      echo
    } >> "$RUN_ROOT/run_metadata.md"
  done
done

ls -l "$RUN_ROOT"
