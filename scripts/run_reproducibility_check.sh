#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -x "./bin/rx" ] || [ ! -x "./bin/tx" ]; then
    echo "[ERROR] ./bin/rx or ./bin/tx is missing. Run make all first."
    exit 1
fi

RUN_ID="${RUN_ID:-$(date +%Y%m%d_%H%M%S)}"
RESULT_DIR="${RESULT_DIR:-logs/reproducibility/${RUN_ID}}"
CSV_PATH="${RESULT_DIR}/reproducibility_check.csv"
NOTES_PATH="${RESULT_DIR}/interpretation.md"
SUMMARY_PATH="${RESULT_DIR}/summary.txt"
TRIALS="${TRIALS:-3}"
RATE_HZ="${RATE_HZ:-120}"
DURATION_SEC="${DURATION_SEC:-5}"
RX_DURATION_SEC="${RX_DURATION_SEC:-$((DURATION_SEC + 2))}"
PAYLOAD_LEN="${PAYLOAD_LEN:-64}"
PORT_BASE="${PORT_BASE:-9400}"
LINK_NAME="${LINK_NAME:-host_loopback}"
REPRO_THRESHOLD_PCT="${REPRO_THRESHOLD_PCT:-15}"
TX_FRAMES_PER_DATAGRAM=3
RX_PID=""

mkdir -p "${RESULT_DIR}"

cleanup() {
    if [ -n "${RX_PID}" ] && kill -0 "${RX_PID}" 2>/dev/null; then
        kill "${RX_PID}" 2>/dev/null || true
        wait "${RX_PID}" 2>/dev/null || true
    fi
}

trap cleanup EXIT

extract_key_from_kv_line() {
    local line="$1"
    local key="$2"
    printf '%s\n' "$line" | tr ' ' '\n' | grep "^${key}=" | tail -1 | cut -d= -f2-
}

average_csv_column() {
    local csv_path="$1"
    local field_index="$2"
    awk -F, -v field_index="${field_index}" '
        NR == 1 { next }
        $field_index != "" {
            sum += $field_index
            count++
        }
        END {
            if (count == 0) {
                printf "0.00"
            } else {
                printf "%.2f", sum / count
            }
        }
    ' "${csv_path}"
}

cat > "${CSV_PATH}" <<'HEADER'
trial,link_name,rate_hz,duration_sec,payload_len,tx_frames_per_datagram,recv_ok,gap_est,crc_fail,len_invalid,preamble_miss,resync_count,latency_p95_ms,latency_p99_ms,latency_max_ms,avg_pps,avg_cpu_pct,p99_deviation_pct_from_mean,reproducible
HEADER

for trial in $(seq 1 "${TRIALS}"); do
    port=$((PORT_BASE + trial - 1))
    trial_dir="${RESULT_DIR}/trial_${trial}"
    rx_log="${trial_dir}/rx.log"
    rx_csv="${trial_dir}/rx_in_1sec.csv"
    rx_recv_csv="${trial_dir}/rx_by_1recv.csv"
    tx_log="${trial_dir}/tx.log"

    rm -rf "${trial_dir}"
    mkdir -p "${trial_dir}"

    echo "[INFO] reproducibility trial=${trial} port=${port} dir=${trial_dir}"

    ./bin/rx \
        --bind-ip 127.0.0.1 \
        --port "${port}" \
        --duration-sec "${RX_DURATION_SEC}" \
        --log-path "${rx_log}" \
        --link-name "${LINK_NAME}" \
        --trial "${trial}" \
        --csv-in-1sec-log-path "${rx_csv}" \
        --csv-by-1recv-log-path "${rx_recv_csv}" &
    RX_PID=$!

    sleep 1

    ./bin/tx \
        --dst-ip 127.0.0.1 \
        --dst-port "${port}" \
        --rate-hz "${RATE_HZ}" \
        --duration-sec "${DURATION_SEC}" \
        --payload-len "${PAYLOAD_LEN}" \
        --log-path "${tx_log}"

    wait "${RX_PID}"
    RX_PID=""

    trial_summary="$(grep 'trial_summary' "${rx_log}" | tail -1 || true)"
    if [ -z "${trial_summary}" ]; then
        echo "[ERROR] trial_summary missing for trial ${trial}"
        exit 1
    fi

    recv_ok="$(extract_key_from_kv_line "${trial_summary}" "recv_ok")"
    gap_est="$(extract_key_from_kv_line "${trial_summary}" "gap_est")"
    crc_fail="$(extract_key_from_kv_line "${trial_summary}" "crc_fail")"
    len_invalid="$(extract_key_from_kv_line "${trial_summary}" "len_invalid")"
    preamble_miss="$(extract_key_from_kv_line "${trial_summary}" "preamble_miss")"
    resync_count="$(extract_key_from_kv_line "${trial_summary}" "resync_count")"
    latency_p95_ms="$(extract_key_from_kv_line "${trial_summary}" "latency_p95_ms")"
    latency_p99_ms="$(extract_key_from_kv_line "${trial_summary}" "latency_p99_ms")"
    latency_max_ms="$(extract_key_from_kv_line "${trial_summary}" "latency_max_ms")"
    avg_pps="$(average_csv_column "${rx_csv}" 10)"
    avg_cpu_pct="$(average_csv_column "${rx_csv}" 11)"

    echo "${trial},${LINK_NAME},${RATE_HZ},${DURATION_SEC},${PAYLOAD_LEN},${TX_FRAMES_PER_DATAGRAM},${recv_ok},${gap_est},${crc_fail},${len_invalid},${preamble_miss},${resync_count},${latency_p95_ms},${latency_p99_ms},${latency_max_ms},${avg_pps},${avg_cpu_pct},pending,pending" >> "${CSV_PATH}"
done

awk -F, -v threshold="${REPRO_THRESHOLD_PCT}" '
    BEGIN {
        OFS = ","
    }
    NR == 1 {
        header = $0
        next
    }
    {
        rows[NR] = $0
        p99[NR] = $14 + 0
        sum += p99[NR]
        count++
    }
    END {
        if (count == 0) {
            exit 1
        }
        print header
        mean = sum / count
        pass = "yes"
        max_dev = 0.0
        for (i = 2; i <= NR; i++) {
            dev = (mean == 0.0) ? 0.0 : ((p99[i] - mean) < 0 ? -(p99[i] - mean) : (p99[i] - mean)) * 100.0 / mean
            if (dev > threshold) {
                pass = "no"
            }
            if (dev > max_dev) {
                max_dev = dev
            }
            split(rows[i], cols, FS)
            cols[18] = sprintf("%.2f", dev)
            cols[19] = pass
            out = cols[1]
            for (j = 2; j <= 19; j++) {
                out = out OFS cols[j]
            }
            print out
        }
        printf "mean_p99_ms=%.3f\nmax_deviation_pct=%.2f\nthreshold_pct=%.2f\nreproducible=%s\n", mean, max_dev, threshold, pass > "/dev/stderr"
    }
' "${CSV_PATH}" > "${CSV_PATH}.tmp" 2> "${SUMMARY_PATH}"

mv "${CSV_PATH}.tmp" "${CSV_PATH}"

MEAN_P99_MS="$(sed -n 's/^mean_p99_ms=//p' "${SUMMARY_PATH}" | tail -1)"
MAX_DEVIATION_PCT="$(sed -n 's/^max_deviation_pct=//p' "${SUMMARY_PATH}" | tail -1)"
ACTUAL_THRESHOLD_PCT="$(sed -n 's/^threshold_pct=//p' "${SUMMARY_PATH}" | tail -1)"
REPRODUCIBLE="$(sed -n 's/^reproducible=//p' "${SUMMARY_PATH}" | tail -1)"

if [ "${REPRODUCIBLE}" = "yes" ]; then
    INTERPRETATION="P99 deviation stayed within +/-${ACTUAL_THRESHOLD_PCT}% of the three-run mean. The stable avg_pps and low cpu_pct spread suggest scheduler jitter stayed bounded in this host-loopback setup."
else
    INTERPRETATION="P99 deviation exceeded +/-${ACTUAL_THRESHOLD_PCT}% of the three-run mean. Compare avg_pps and cpu_pct across trials first; a large spread there usually indicates local scheduler or background-load interference rather than frame parsing drift."
fi

{
    echo "# Reproducibility Result"
    echo
    echo "- Run date: $(date -Iseconds)"
    echo "- Link name: ${LINK_NAME}"
    echo "- Trials: ${TRIALS}"
    echo "- Rate: ${RATE_HZ} frame/s"
    echo "- Duration: ${DURATION_SEC}s tx / ${RX_DURATION_SEC}s rx"
    echo "- Payload length: ${PAYLOAD_LEN} bytes"
    echo "- Mean P99: ${MEAN_P99_MS} ms"
    echo "- Max deviation from mean: ${MAX_DEVIATION_PCT}%"
    echo "- Criterion: reproducible when every trial stays within +/-${ACTUAL_THRESHOLD_PCT}% of mean P99"
    echo "- Result: ${REPRODUCIBLE}"
    echo
    echo "${INTERPRETATION}"
} > "${NOTES_PATH}"

echo "[INFO] wrote ${CSV_PATH}"
echo "[INFO] wrote ${NOTES_PATH}"
