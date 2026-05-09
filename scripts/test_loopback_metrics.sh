#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -x "./bin/rx" ] || [ ! -x "./bin/tx" ]; then
    echo "[ERROR] ./bin/rx or ./bin/tx is missing. Run make all first."
    exit 1
fi

TMP_DIR="$(mktemp -d)"
RX_LOG="${TMP_DIR}/rx.log"
RX_CSV="${TMP_DIR}/rx_in_1sec.csv"
RX_RECV_CSV="${TMP_DIR}/rx_by_1recv.csv"
TX_LOG="${TMP_DIR}/tx.log"
PORT=9310
RX_PID=""

cleanup() {
    if [ -n "${RX_PID}" ] && kill -0 "${RX_PID}" 2>/dev/null; then
        kill "${RX_PID}" 2>/dev/null || true
        wait "${RX_PID}" 2>/dev/null || true
    fi
    rm -rf "${TMP_DIR}"
}

trap cleanup EXIT

./bin/rx \
    --bind-ip 127.0.0.1 \
    --port "${PORT}" \
    --duration-sec 4 \
    --log-path "${RX_LOG}" \
    --link-name test_loopback \
    --trial 1 \
    --csv-in-1sec-log-path "${RX_CSV}" \
    --csv-by-1recv-log-path "${RX_RECV_CSV}" &
RX_PID=$!

sleep 1

./bin/tx \
    --dst-ip 127.0.0.1 \
    --dst-port "${PORT}" \
    --rate-hz 60 \
    --duration-sec 2 \
    --payload-len 64 \
    --log-path "${TX_LOG}"

wait "${RX_PID}"
RX_PID=""

TRIAL_SUMMARY="$(grep 'trial_summary' "${RX_LOG}" | tail -1 || true)"
if [ -z "${TRIAL_SUMMARY}" ]; then
    echo "[ERROR] trial_summary was not emitted"
    exit 1
fi

printf '%s\n' "${TRIAL_SUMMARY}" | grep -q 'latency_p95_ms='
printf '%s\n' "${TRIAL_SUMMARY}" | grep -q 'latency_p99_ms='
printf '%s\n' "${TRIAL_SUMMARY}" | grep -q 'latency_max_ms='

HEADER="$(head -1 "${RX_CSV}")"
printf '%s\n' "${HEADER}" | grep -q 'pps'
printf '%s\n' "${HEADER}" | grep -q 'cpu_pct'

DATA_ROWS="$(tail -n +2 "${RX_CSV}" | wc -l)"
if [ "${DATA_ROWS}" -lt 1 ]; then
    echo "[ERROR] rx_in_1sec.csv has no data rows"
    exit 1
fi

tail -n +2 "${RX_CSV}" | awk -F, '
    NF < 11 { exit 1 }
    {
        if ($10 + 0 < 0) exit 1
        if ($11 + 0 < 0) exit 1
    }
' || {
    echo "[ERROR] rx_in_1sec.csv is missing pps/cpu_pct values"
    exit 1
}

grep -q 'tx_stats ' "${TX_LOG}" || {
    echo "[ERROR] tx_stats was not emitted"
    exit 1
}

echo "[PASS] loopback metrics smoke test"
