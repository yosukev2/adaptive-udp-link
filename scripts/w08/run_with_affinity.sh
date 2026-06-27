#!/usr/bin/env bash
#
# run_with_affinity.sh
#
# W08 の CPU affinity 比較用に、tx/rx を同じ手順で起動する。
# 既定では tx と rx の両方を同じ CPU core に固定する。
# --target none を指定すると taskset を使わず baseline 相当にできる。

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: scripts/w08/run_with_affinity.sh [options]

Options:
  --run-dir DIR            Result directory (default: logs/w08/cpu_affinity/<timestamp>)
  --trial N                Trial number (default: 1)
  --target MODE            both|tx|rx|none (default: both)
  --core N                 CPU core to pin when target is not none (default: 0)
  --link-name NAME         Link name for rx log (default: w08_cpu_affinity)
  --bind-ip IP             RX bind IP (default: 127.0.0.1)
  --dst-ip IP              TX destination IP (default: 127.0.0.1)
  --port N                 UDP port (default: 9000)
  --rate-hz N              TX frame rate (default: 100)
  --duration-sec N         TX duration in seconds (default: 60)
  --rx-duration-sec N      RX duration in seconds (default: 62)
  --payload-len N          Payload length in bytes (default: 48)
  --start-delay-sec N      Delay before TX starts (default: 1)
  --help                   Show this help

The script writes:
  <run-dir>/trial_<N>/run.log
  <run-dir>/trial_<N>/rx.log
  <run-dir>/trial_<N>/tx.log
  <run-dir>/trial_<N>/rx_1sec.csv
  <run-dir>/trial_<N>/rx_by_1recv.csv
EOF
}

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

RUN_ID="${RUN_ID:-$(date +%Y%m%d_%H%M%S)}"
RUN_DIR="${RESULT_DIR:-logs/w08/cpu_affinity/${RUN_ID}}"
TRIAL="1"
TARGET="both"
CORE="0"
LINK_NAME="w08_cpu_affinity"
BIND_IP="127.0.0.1"
DST_IP="127.0.0.1"
PORT="9000"
RATE_HZ="100"
DURATION_SEC="60"
RX_DURATION_SEC="62"
PAYLOAD_LEN="48"
START_DELAY_SEC="1"

while [ $# -gt 0 ]; do
    case "$1" in
        --run-dir)
            RUN_DIR="$2"
            shift 2
            ;;
        --trial)
            TRIAL="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --core)
            CORE="$2"
            shift 2
            ;;
        --link-name)
            LINK_NAME="$2"
            shift 2
            ;;
        --bind-ip)
            BIND_IP="$2"
            shift 2
            ;;
        --dst-ip)
            DST_IP="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --rate-hz)
            RATE_HZ="$2"
            shift 2
            ;;
        --duration-sec)
            DURATION_SEC="$2"
            shift 2
            ;;
        --rx-duration-sec)
            RX_DURATION_SEC="$2"
            shift 2
            ;;
        --payload-len)
            PAYLOAD_LEN="$2"
            shift 2
            ;;
        --start-delay-sec)
            START_DELAY_SEC="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "[ERROR] unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [ ! -x "./bin/rx" ] || [ ! -x "./bin/tx" ]; then
    echo "[ERROR] ./bin/rx or ./bin/tx is missing. Run make first." >&2
    exit 1
fi

case "$TARGET" in
    both|tx|rx|none)
        ;;
    *)
        echo "[ERROR] --target must be one of both|tx|rx|none: $TARGET" >&2
        exit 1
        ;;
esac

if [ "$TARGET" != "none" ] && [ "${CORE}" -lt 0 ]; then
    echo "[ERROR] --core must be >= 0 when --target is not none" >&2
    exit 1
fi

TRIAL_DIR="${RUN_DIR}/trial_${TRIAL}"
RX_LOG="${TRIAL_DIR}/rx.log"
TX_LOG="${TRIAL_DIR}/tx.log"
RUN_LOG="${TRIAL_DIR}/run.log"
RX_CSV_1SEC="${TRIAL_DIR}/rx_1sec.csv"
RX_CSV_BY_1RECV="${TRIAL_DIR}/rx_by_1recv.csv"
RX_PID=""

mkdir -p "${TRIAL_DIR}"
: > "${RUN_LOG}"

log_line() {
    local level="$1"
    shift
    printf '%s [%s] %s\n' "$(date +'%Y-%m-%d %H:%M:%S')" "$level" "$*" | tee -a "${RUN_LOG}"
}

quote_cmd() {
    local out=""
    local arg
    for arg in "$@"; do
        out+=$(printf '%q ' "$arg")
    done
    printf '%s' "$out"
}

build_rx_cmd() {
    local -a cmd=("./bin/rx"
        "--bind-ip" "${BIND_IP}"
        "--port" "${PORT}"
        "--duration-sec" "${RX_DURATION_SEC}"
        "--log-path" "${RX_LOG}"
        "--link-name" "${LINK_NAME}"
        "--trial" "${TRIAL}"
        "--csv-in-1sec-log-path" "${RX_CSV_1SEC}"
        "--csv-by-1recv-log-path" "${RX_CSV_BY_1RECV}"
        "--recovery-mode" "fsm")
    if [ "$TARGET" = "both" ] || [ "$TARGET" = "rx" ]; then
        cmd=(taskset -c "${CORE}" "${cmd[@]}")
    fi
    printf '%s\0' "${cmd[@]}"
}

build_tx_cmd() {
    local -a cmd=("./bin/tx"
        "--dst-ip" "${DST_IP}"
        "--dst-port" "${PORT}"
        "--rate-hz" "${RATE_HZ}"
        "--duration-sec" "${DURATION_SEC}"
        "--log-path" "${TX_LOG}"
        "--payload-len" "${PAYLOAD_LEN}"
        "--version" "1")
    if [ "$TARGET" = "both" ] || [ "$TARGET" = "tx" ]; then
        cmd=(taskset -c "${CORE}" "${cmd[@]}")
    fi
    printf '%s\0' "${cmd[@]}"
}

log_line INFO "run_dir=${TRIAL_DIR}"
log_line INFO "trial=${TRIAL} target=${TARGET} core=${CORE}"
log_line INFO "bind_ip=${BIND_IP} dst_ip=${DST_IP} port=${PORT} rate_hz=${RATE_HZ} duration_sec=${DURATION_SEC} rx_duration_sec=${RX_DURATION_SEC} payload_len=${PAYLOAD_LEN}"

mapfile -d '' -t RX_CMD < <(build_rx_cmd)
mapfile -d '' -t TX_CMD < <(build_tx_cmd)

log_line INFO "rx_cmd=$(quote_cmd "${RX_CMD[@]}")"
log_line INFO "tx_cmd=$(quote_cmd "${TX_CMD[@]}")"

"${RX_CMD[@]}" &
RX_PID=$!

sleep "${START_DELAY_SEC}"

set +e
"${TX_CMD[@]}"
TX_STATUS=$?

wait "${RX_PID}"
RX_STATUS=$?
set -e

log_line INFO "tx_status=${TX_STATUS} rx_status=${RX_STATUS}"

printf 'run_dir=%s\ntrial=%s\ntarget=%s\ncore=%s\ntx_status=%s\nrx_status=%s\n' \
    "${TRIAL_DIR}" "${TRIAL}" "${TARGET}" "${CORE}" "${TX_STATUS}" "${RX_STATUS}"

exit $((TX_STATUS != 0 || RX_STATUS != 0))
