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
RUNS_CSV="${RESULT_DIR}/compare_runs.csv"
SUMMARY_CSV="${RESULT_DIR}/compare_summary.csv"
INTERPRETATION_PATH="${RESULT_DIR}/interpretation.md"
TRIALS="${TRIALS:-3}"
LINK_NAME="${LINK_NAME:-host_loopback}"
RATE_HZ="${RATE_HZ:-30}"
OUTAGE_AT_SEC="${OUTAGE_AT_SEC:-2}"
PORT_BASE="${PORT_BASE:-9600}"
POST_OUTAGE_MARGIN_SEC="${POST_OUTAGE_MARGIN_SEC:-2}"
RX_EXTRA_SEC="${RX_EXTRA_SEC:-2}"
TX_START_DELAY_SEC="${TX_START_DELAY_SEC:-1}"
RX_PID=""

mode_names=("fsm" "timeout-only")
mode_labels=("fsm" "timeout_only")
scenario_names=("0.5s" "1s" "3s")
scenario_labels=("500ms" "1000ms" "3000ms")
scenario_outage_ms=(500 1000 3000)

mkdir -p "${RESULT_DIR}"

cleanup() {
    if [ -n "${RX_PID}" ] && kill -0 "${RX_PID}" 2>/dev/null; then
        kill "${RX_PID}" 2>/dev/null || true
        wait "${RX_PID}" 2>/dev/null || true
    fi
}

trap cleanup EXIT

expected_pattern_for() {
    local mode="$1"
    local outage_ms="$2"

    case "${mode}:${outage_ms}" in
        fsm:500|fsm:1000|timeout-only:500|timeout-only:1000)
            printf 'no-transitions\n'
            ;;
        fsm:3000)
            printf 'fsm-recovery\n'
            ;;
        timeout-only:3000)
            printf 'timeout-only-recovery\n'
            ;;
        *)
            echo "[ERROR] unsupported mode/outage combination: ${mode}/${outage_ms}" >&2
            return 1
            ;;
    esac
}

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
    local -a rows=()
    local from_state
    local to_state
    local elapsed_ms
    local observed_pattern
    local expected_from
    local expected_to

    transition_rows="$(count_state_transition_rows "${csv_path}")"

    if [ "${expected_pattern}" = "no-transitions" ]; then
        if [ "${transition_rows}" -ne 0 ]; then
            echo "[ERROR] expected no state transitions, got ${transition_rows} in ${csv_path}"
            return 1
        fi
        printf 'na\nna\nnone\n'
        return 0
    fi

    if [ "${expected_pattern}" = "fsm-recovery" ]; then
        if [ "${transition_rows}" -lt 3 ]; then
            echo "[ERROR] expected at least 3 state transitions, got ${transition_rows} in ${csv_path}"
            return 1
        fi

        mapfile -t rows < <(tail -n +2 "${csv_path}")
        IFS=, read -r _ _ _ elapsed_ms from_state to_state _ <<< "${rows[0]}"
        if [ "${from_state}" != "Normal" ] || [ "${to_state}" != "Degraded" ]; then
            echo "[ERROR] unexpected first transition in ${csv_path}: ${rows[0]}"
            return 1
        fi
        degraded_detect_ms="${elapsed_ms}"
        observed_pattern="Normal->${to_state}"

        expected_from="Degraded"
        expected_to="Recover"
        for ((i = 1; i < transition_rows - 1; i++)); do
            IFS=, read -r _ _ _ _ from_state to_state _ <<< "${rows[$i]}"
            if [ "${from_state}" != "${expected_from}" ] || [ "${to_state}" != "${expected_to}" ]; then
                echo "[ERROR] unexpected middle transition in ${csv_path}: ${rows[$i]}"
                return 1
            fi
            observed_pattern="${observed_pattern}->${to_state}"
            if [ "${expected_from}" = "Degraded" ]; then
                expected_from="Recover"
                expected_to="Degraded"
            else
                expected_from="Degraded"
                expected_to="Recover"
            fi
        done

        IFS=, read -r _ _ _ elapsed_ms from_state to_state _ <<< "${rows[$((transition_rows - 1))]}"
        if [ "${from_state}" != "Recover" ] || [ "${to_state}" != "Normal" ]; then
            echo "[ERROR] unexpected final transition in ${csv_path}: ${rows[$((transition_rows - 1))]}"
            return 1
        fi
        recover_complete_ms="${elapsed_ms}"
        observed_pattern="${observed_pattern}->${to_state}"

        printf '%s\n%s\n%s\n' "${degraded_detect_ms}" "${recover_complete_ms}" "${observed_pattern}"
        return 0
    fi

    if [ "${expected_pattern}" = "timeout-only-recovery" ]; then
        if [ "${transition_rows}" -ne 2 ]; then
            echo "[ERROR] expected exactly 2 state transitions, got ${transition_rows} in ${csv_path}"
            return 1
        fi

        degraded_detect_ms="$(extract_state_transition_value "${csv_path}" Normal Degraded)"
        recover_complete_ms="$(extract_state_transition_value "${csv_path}" Degraded Normal)"
        if [ -z "${degraded_detect_ms}" ] || [ -z "${recover_complete_ms}" ]; then
            echo "[ERROR] required timeout-only transitions are missing in ${csv_path}"
            return 1
        fi

        line1="$(sed -n '2p' "${csv_path}")"
        line2="$(sed -n '3p' "${csv_path}")"

        IFS=, read -r _ _ _ _ from_state to_state _ <<< "${line1}"
        if [ "${from_state}" != "Normal" ] || [ "${to_state}" != "Degraded" ]; then
            echo "[ERROR] unexpected first transition in ${csv_path}: ${line1}"
            return 1
        fi

        IFS=, read -r _ _ _ _ from_state to_state _ <<< "${line2}"
        if [ "${from_state}" != "Degraded" ] || [ "${to_state}" != "Normal" ]; then
            echo "[ERROR] unexpected second transition in ${csv_path}: ${line2}"
            return 1
        fi

        printf '%s\n%s\n%s\n' "${degraded_detect_ms}" "${recover_complete_ms}" "Normal->Degraded->Normal"
        return 0
    fi

    echo "[ERROR] unsupported expected pattern: ${expected_pattern}"
    return 1
}

cat > "${RUNS_CSV}" <<'HEADER'
mode,scenario,trial,outage_ms,degraded_detect_ms,recover_complete_ms,expected_pattern,observed_pattern,link_name,port,run_dir
HEADER

for mode_idx in "${!mode_names[@]}"; do
    mode_name="${mode_names[$mode_idx]}"
    mode_label="${mode_labels[$mode_idx]}"

    for scenario_idx in "${!scenario_names[@]}"; do
        scenario_name="${scenario_names[$scenario_idx]}"
        scenario_label="${scenario_labels[$scenario_idx]}"
        outage_ms="${scenario_outage_ms[$scenario_idx]}"
        expected_pattern="$(expected_pattern_for "${mode_name}" "${outage_ms}")"
        tx_duration_sec=$((OUTAGE_AT_SEC + (outage_ms + 999) / 1000 + POST_OUTAGE_MARGIN_SEC))
        rx_duration_sec=$((tx_duration_sec + RX_EXTRA_SEC))

        for trial in $(seq 1 "${TRIALS}"); do
            port=$((PORT_BASE + mode_idx * 100 + scenario_idx * TRIALS + trial - 1))
            trial_dir="${RESULT_DIR}/mode_${mode_label}/scenario_${scenario_label}/trial_${trial}"
            rx_log="${trial_dir}/rx.log"
            tx_log="${trial_dir}/tx.log"
            state_csv="${trial_dir}/state.csv"

            rm -rf "${trial_dir}"
            mkdir -p "${trial_dir}"

            echo "[INFO] mode=${mode_name} scenario=${scenario_name} trial=${trial} outage_ms=${outage_ms} port=${port} dir=${trial_dir}"

            ./bin/rx \
                --bind-ip 127.0.0.1 \
                --port "${port}" \
                --duration-sec "${rx_duration_sec}" \
                --log-path "${rx_log}" \
                --link-name "${LINK_NAME}" \
                --trial "${trial}" \
                --state-log-path "${state_csv}" \
                --recovery-mode "${mode_name}" &
            RX_PID=$!

            sleep "${TX_START_DELAY_SEC}"

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

            echo "${mode_name},${scenario_name},${trial},${outage_ms},${degraded_detect_ms},${recover_complete_ms},${expected_pattern},${observed_pattern},${LINK_NAME},${port},${trial_dir}" >> "${RUNS_CSV}"
        done
    done
done

awk -F, '
    BEGIN {
        OFS = ","
    }
    NR == 1 {
        next
    }
    {
        key = $1 FS $4
        if (!(key in seen)) {
            seen[key] = 1
            order[++count] = key
        }
        mode[key] = $1
        outage[key] = $4
        expected[key] = $7
        observed[key] = $8
        trials[key]++
        if ($5 != "na") {
            degraded_sum[key] += $5
            degraded_count[key]++
            if (!(key in degraded_min) || $5 < degraded_min[key]) {
                degraded_min[key] = $5
            }
            if (!(key in degraded_max) || $5 > degraded_max[key]) {
                degraded_max[key] = $5
            }
        }
        if ($6 != "na") {
            recover_sum[key] += $6
            recover_count[key]++
            if (!(key in recover_min) || $6 < recover_min[key]) {
                recover_min[key] = $6
            }
            if (!(key in recover_max) || $6 > recover_max[key]) {
                recover_max[key] = $6
            }
        }
    }
    END {
        print "outage_ms,mode,degraded_detect_ms,recover_complete_ms,expected_pattern,observed_pattern,trials,degraded_range_ms,recover_range_ms"
        for (i = 1; i <= count; i++) {
            key = order[i]
            degraded_mean = (degraded_count[key] > 0) ? sprintf("%.0f", degraded_sum[key] / degraded_count[key]) : "na"
            recover_mean = (recover_count[key] > 0) ? sprintf("%.0f", recover_sum[key] / recover_count[key]) : "na"
            degraded_range = (degraded_count[key] > 0) ? sprintf("%.0f", degraded_max[key] - degraded_min[key]) : "na"
            recover_range = (recover_count[key] > 0) ? sprintf("%.0f", recover_max[key] - recover_min[key]) : "na"
            print outage[key], mode[key], degraded_mean, recover_mean, expected[key], observed[key], trials[key], degraded_range, recover_range
        }
    }
' "${RUNS_CSV}" > "${SUMMARY_CSV}"

VARIATION_NOTE="$(awk -F, '
    NR == 1 {
        next
    }
    {
        if ($8 != "na" && ($8 + 0) > 0) {
            varied = 1
        }
        if ($9 != "na" && ($9 + 0) > 0) {
            varied = 1
        }
    }
    END {
        if (varied) {
            print "一部の mode / outage で trial 間のばらつきがあるため、CPU scheduling や tx 開始オフセットの揺れを候補として再確認してください。"
        } else {
            print "今回の baseline では、mode ごとの Degraded 検知時刻と Recover 完了時刻に大きな trial 差は観測されませんでした。"
        }
    }
' "${SUMMARY_CSV}")"

summary_value() {
    local outage_ms="$1"
    local mode="$2"
    local field_index="$3"
    awk -F, -v outage_ms="${outage_ms}" -v mode="${mode}" -v field_index="${field_index}" '
        NR > 1 && $1 == outage_ms && $2 == mode {
            print $field_index
            exit
        }
    ' "${SUMMARY_CSV}"
}

FSM_3S_DEGRADED_MS="$(summary_value 3000 fsm 3)"
FSM_3S_RECOVER_MS="$(summary_value 3000 fsm 4)"
TIMEOUT_3S_RECOVER_MS="$(summary_value 3000 timeout-only 4)"

{
    echo "# FSM vs Timeout Comparison"
    echo
    echo "- Run date: $(date -Iseconds)"
    echo "- Link name: ${LINK_NAME}"
    echo "- Trials per mode/scenario: ${TRIALS}"
    echo "- Result directory: ${RESULT_DIR}"
    echo "- Per-run CSV: ${RUNS_CSV}"
    echo "- Summary CSV: ${SUMMARY_CSV}"
    echo
    echo "| Outage | Mode | Degraded Detect (ms) | Recover Complete (ms) | Observed Pattern |"
    echo "|--------|------|----------------------|------------------------|------------------|"
    tail -n +2 "${SUMMARY_CSV}" | while IFS=, read -r outage_ms mode degraded_ms recover_ms _ observed_pattern _ _ _; do
        echo "| ${outage_ms} | ${mode} | ${degraded_ms} | ${recover_ms} | ${observed_pattern} |"
    done
    echo
    echo "0.5s と 1s の outage は、現行の recv_ok == 0 が 2 つの 1 秒窓連続で必要という Degraded 条件を跨がないため、fsm と timeout-only のどちらでも state transition は発生しませんでした。したがって両 mode とも degraded_detect_ms / recover_complete_ms は na です。"
    echo
    echo "3s の outage では両 mode とも Degraded 検知は ${FSM_3S_DEGRADED_MS}ms で揃いました。fsm は Normal->Degraded->Recover->Normal と明示的な復旧フェーズを残し、timeout-only は Normal->Degraded->Normal へ直接戻ります。今回の baseline では fsm の Recover 完了は ${FSM_3S_RECOVER_MS}ms、timeout-only の Normal 復帰は ${TIMEOUT_3S_RECOVER_MS}ms でした。"
    echo
    echo "${VARIATION_NOTE}"
} > "${INTERPRETATION_PATH}"

echo "[INFO] wrote ${RUNS_CSV}"
echo "[INFO] wrote ${SUMMARY_CSV}"
echo "[INFO] wrote ${INTERPRETATION_PATH}"
