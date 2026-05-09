#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -x "./bin/rx" ] || [ ! -x "./bin/tx" ]; then
    echo "[ERROR] ./bin/rx or ./bin/tx is missing. Run make all first."
    exit 1
fi

RUN_ID="${RUN_ID:-$(date +%Y%m%d_%H%M%S)}"
RESULT_DIR="${RESULT_DIR:-logs/fsm_recovery/${RUN_ID}}"
CSV_PATH="${RESULT_DIR}/fsm_recovery_check.csv"
SUMMARY_PATH="${RESULT_DIR}/summary.txt"
TRIALS="${TRIALS:-3}"
LINK_NAME="${LINK_NAME:-host_loopback}"
RATE_HZ="${RATE_HZ:-30}"
OUTAGE_AT_SEC="${OUTAGE_AT_SEC:-2}"
PORT_BASE="${PORT_BASE:-9500}"
POST_OUTAGE_MARGIN_SEC="${POST_OUTAGE_MARGIN_SEC:-2}"
RX_EXTRA_SEC="${RX_EXTRA_SEC:-2}"
TX_FRAMES_PER_DATAGRAM=3
RX_PID=""

scenario_names=("0.5s" "1s" "3s")
scenario_labels=("500ms" "1000ms" "3000ms")
scenario_outage_ms=(500 1000 3000)
scenario_expectations=("no-transitions" "no-transitions" "fsm-recovery")

mkdir -p "${RESULT_DIR}"

cleanup() {
    if [ -n "${RX_PID}" ] && kill -0 "${RX_PID}" 2>/dev/null; then
        kill "${RX_PID}" 2>/dev/null || true
        wait "${RX_PID}" 2>/dev/null || true
    fi
}

trap cleanup EXIT

extract_state_transition_value() {
    local csv_path="$1"
    local from_state="$2"
    local to_state="$3"
    awk -F, -v from_state="${from_state}" -v to_state="${to_state}" '
        NR > 1 && $5 == from_state && $6 == to_state {
            print $4
            exit
        }
    ' "${csv_path}"
}

count_state_transition_rows() {
    local csv_path="$1"
    awk -F, 'NR > 1 { count++ } END { print count + 0 }' "${csv_path}"
}

validate_state_sequence() {
    local csv_path="$1"
    local expected_pattern="$2"
    local transition_rows
    local degraded_detect_ms
    local recover_complete_ms
    local line1
    local line2
    local line3
    local from_state
    local to_state

    transition_rows="$(count_state_transition_rows "${csv_path}")"
    if [ "${expected_pattern}" = "no-transitions" ]; then
        if [ "${transition_rows}" -ne 0 ]; then
            echo "[ERROR] expected no state transitions, got ${transition_rows} in ${csv_path}"
            return 1
        fi
        printf 'na\nna\nnone\n'
        return 0
    fi

    if [ "${transition_rows}" -ne 3 ]; then
        echo "[ERROR] expected exactly 3 state transitions, got ${transition_rows} in ${csv_path}"
        return 1
    fi

    degraded_detect_ms="$(extract_state_transition_value "${csv_path}" Normal Degraded)"
    recover_complete_ms="$(extract_state_transition_value "${csv_path}" Recover Normal)"

    if [ -z "${degraded_detect_ms}" ] || [ -z "${recover_complete_ms}" ]; then
        echo "[ERROR] required state transitions are missing in ${csv_path}"
        return 1
    fi

    line1="$(sed -n '2p' "${csv_path}")"
    line2="$(sed -n '3p' "${csv_path}")"
    line3="$(sed -n '4p' "${csv_path}")"

    IFS=, read -r _ _ _ _ from_state to_state _ <<< "${line1}"
    if [ "${from_state}" != "Normal" ] || [ "${to_state}" != "Degraded" ]; then
        echo "[ERROR] unexpected first transition in ${csv_path}: ${line1}"
        return 1
    fi

    IFS=, read -r _ _ _ _ from_state to_state _ <<< "${line2}"
    if [ "${from_state}" != "Degraded" ] || [ "${to_state}" != "Recover" ]; then
        echo "[ERROR] unexpected second transition in ${csv_path}: ${line2}"
        return 1
    fi

    IFS=, read -r _ _ _ _ from_state to_state _ <<< "${line3}"
    if [ "${from_state}" != "Recover" ] || [ "${to_state}" != "Normal" ]; then
        echo "[ERROR] unexpected third transition in ${csv_path}: ${line3}"
        return 1
    fi

    printf '%s\n%s\n%s\n' "${degraded_detect_ms}" "${recover_complete_ms}" "Normal->Degraded->Recover->Normal"
}

cat > "${CSV_PATH}" <<'HEADER'
scenario,trial,outage_ms,degraded_detect_ms,recover_complete_ms,expected_pattern,observed_pattern,link_name,port,run_dir
HEADER

for idx in "${!scenario_names[@]}"; do
    scenario_name="${scenario_names[$idx]}"
    scenario_label="${scenario_labels[$idx]}"
    outage_ms="${scenario_outage_ms[$idx]}"
    expected_pattern="${scenario_expectations[$idx]}"
    tx_duration_sec=$((OUTAGE_AT_SEC + (outage_ms + 999) / 1000 + POST_OUTAGE_MARGIN_SEC))
    rx_duration_sec=$((tx_duration_sec + RX_EXTRA_SEC))

    for trial in $(seq 1 "${TRIALS}"); do
        port=$((PORT_BASE + idx * TRIALS + trial - 1))
        trial_dir="${RESULT_DIR}/scenario_${scenario_label}/trial_${trial}"
        rx_log="${trial_dir}/rx.log"
        tx_log="${trial_dir}/tx.log"
        state_csv="${trial_dir}/state.csv"

        rm -rf "${trial_dir}"
        mkdir -p "${trial_dir}"

        echo "[INFO] scenario=${scenario_name} trial=${trial} outage_ms=${outage_ms} port=${port} dir=${trial_dir}"

        ./bin/rx \
            --bind-ip 127.0.0.1 \
            --port "${port}" \
            --duration-sec "${rx_duration_sec}" \
            --log-path "${rx_log}" \
            --link-name "${LINK_NAME}" \
            --trial "${trial}" \
            --state-log-path "${state_csv}" &
        RX_PID=$!

        sleep 1

        ./bin/tx \
            --dst-ip 127.0.0.1 \
            --dst-port "${port}" \
            --rate-hz "${RATE_HZ}" \
            --duration-sec "${tx_duration_sec}" \
            --log-path "${tx_log}" \
            --outage-at-sec "${OUTAGE_AT_SEC}" \
            --outage-duration-ms "${outage_ms}"

        wait "${RX_PID}"
        RX_PID=""

        transition_values="$(validate_state_sequence "${state_csv}" "${expected_pattern}")" || exit 1
        degraded_detect_ms="$(printf '%s\n' "${transition_values}" | sed -n '1p')"
        recover_complete_ms="$(printf '%s\n' "${transition_values}" | sed -n '2p')"
        observed_pattern="$(printf '%s\n' "${transition_values}" | sed -n '3p')"

        echo "${scenario_name},${trial},${outage_ms},${degraded_detect_ms},${recover_complete_ms},${expected_pattern},${observed_pattern},${LINK_NAME},${port},${trial_dir}" >> "${CSV_PATH}"
    done
done

{
    echo "# FSM Recovery Matrix"
    echo
    echo "- Run date: $(date -Iseconds)"
    echo "- Link name: ${LINK_NAME}"
    echo "- Trials per scenario: ${TRIALS}"
    echo "- Scenarios: 0.5s, 1s, 3s"
    echo "- Result directory: ${RESULT_DIR}"
    echo "- Aggregate CSV: ${CSV_PATH}"
    echo
    echo "Current W05 thresholding expects:"
    echo
    echo "  0.5s -> no state transition"
    echo "  1s   -> no state transition"
    echo "  3s   -> Normal -> Degraded -> Recover -> Normal"
    echo
    echo "Each run writes raw logs and the FSM state CSV under:"
    echo
    echo "  ${RESULT_DIR}/scenario_500ms/trial_1/"
    echo "  ${RESULT_DIR}/scenario_1000ms/trial_1/"
    echo "  ${RESULT_DIR}/scenario_3000ms/trial_1/"
    echo
    echo "Per-run files:"
    echo
    echo "  rx.log"
    echo "  tx.log"
    echo "  state.csv"
} > "${SUMMARY_PATH}"

echo "[INFO] wrote ${CSV_PATH}"
echo "[INFO] wrote ${SUMMARY_PATH}"
