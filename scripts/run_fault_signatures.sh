#!/usr/bin/env bash
#
# run_fault_signatures.sh
#
# 目的:
#   - W03 #56: fault-target ごとの主シグネチャを最小実行で確認する
#   - preamble / payload_len / header / crc / payload を各 1 回ずつ流す
#   - trial_summary の共通列と、Host 補助観測の bad_header を CSV に残す

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -x "./bin/rx" ] || [ ! -x "./bin/tx" ]; then
    echo "[ERROR] ./bin/rx または ./bin/tx が見つかりません。先にビルドしてください。"
    exit 1
fi

RESULT_DIR="logs/fault_signatures"
mkdir -p "$RESULT_DIR"

CSV="$RESULT_DIR/fault_signatures.csv"
META="$RESULT_DIR/experiment_conditions.txt"

TARGETS=("preamble" "payload_len" "header" "crc" "payload")
RATE_HZ=30
DURATION_SEC=3
RX_DURATION_SEC=$(( DURATION_SEC + 2 ))
PAYLOAD_LEN=48
FAULT_RATE="0.50"
TRIAL=1
PORT_BASE=9200
BIND_IP="127.0.0.1"
DST_IP="127.0.0.1"
LINK_NAME_PREFIX="host_loopback"
TX_FRAMES_PER_DATAGRAM=3
OS_INFO="$(uname -sr)"

RX_PID=""

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

extract_trial_summary_line() {
    local log_path="$1"
    grep "trial_summary" "$log_path" | tail -1
}

extract_rx_summary_value() {
    local log_path="$1"
    local key="$2"
    grep "rx summary" "$log_path" | tail -1 | grep -o "${key}=[0-9]*" | cut -d= -f2
}

signature_hint_for_target() {
    local target="$1"
    case "$target" in
        preamble)
            echo "trial_summary では header と曖昧 (preamble_miss + resync_count)"
            ;;
        payload_len)
            echo "len_invalid + resync_count"
            ;;
        header)
            echo "trial_summary では preamble と曖昧; Host補助では bad_header"
            ;;
        crc)
            echo "crc_fail"
            ;;
        payload)
            echo "crc_fail"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

cat > "$CSV" <<'HEADER'
target,trial,link_name,rate_hz,duration_sec,payload_len,fault_rate,recv_ok,gap_est,crc_fail,len_invalid,preamble_miss,resync_count,bad_header,signature_hint
HEADER

cat > "$META" <<EOF
# fault signature 条件

実施目的: fault-target ごとの主シグネチャを最小 1 回で比較する
対象 target: preamble / payload_len / header / crc / payload
trial: ${TRIAL}
link_name prefix: ${LINK_NAME_PREFIX}
送信レート: ${RATE_HZ} frame/s
tx_duration_sec: ${DURATION_SEC} 秒
rx_duration_sec: ${RX_DURATION_SEC} 秒
payload_len: ${PAYLOAD_LEN}
fault_rate: ${FAULT_RATE}
tx_frames_per_datagram: ${TX_FRAMES_PER_DATAGRAM}
bind_ip: ${BIND_IP}
dst_ip: ${DST_IP}
port_base: ${PORT_BASE}
OS: ${OS_INFO}
EOF

echo "[INFO] fault-target 別シグネチャ確認を開始します"
echo "[INFO] 結果 CSV: ${CSV}"

for idx in "${!TARGETS[@]}"; do
    target="${TARGETS[$idx]}"
    port=$(( PORT_BASE + idx ))
    link_name="${LINK_NAME_PREFIX}_${target}"
    run_dir="${RESULT_DIR}/run_${target}_trial${TRIAL}"
    rx_log="${run_dir}/rx.log"
    tx_log="${run_dir}/tx.log"

    rm -rf "$run_dir"
    mkdir -p "$run_dir"

    echo "[INFO] target=${target} port=${port} run_dir=${run_dir}"

    ./bin/rx \
        --bind-ip "$BIND_IP" \
        --port "$port" \
        --duration-sec "$RX_DURATION_SEC" \
        --log-path "$rx_log" \
        --link-name "$link_name" \
        --trial "$TRIAL" &
    RX_PID=$!

    sleep 1

    ./bin/tx \
        --dst-ip "$DST_IP" \
        --dst-port "$port" \
        --rate-hz "$RATE_HZ" \
        --duration-sec "$DURATION_SEC" \
        --log-path "$tx_log" \
        --payload-len "$PAYLOAD_LEN" \
        --fault-target "$target" \
        --fault-rate "$FAULT_RATE"

    wait "$RX_PID"
    RX_PID=""

    trial_summary="$(extract_trial_summary_line "$rx_log")"
    duration_sec="$(extract_key_from_kv_line "$trial_summary" "duration_sec")"
    recv_ok="$(extract_key_from_kv_line "$trial_summary" "recv_ok")"
    gap_est="$(extract_key_from_kv_line "$trial_summary" "gap_est")"
    crc_fail="$(extract_key_from_kv_line "$trial_summary" "crc_fail")"
    len_invalid="$(extract_key_from_kv_line "$trial_summary" "len_invalid")"
    preamble_miss="$(extract_key_from_kv_line "$trial_summary" "preamble_miss")"
    resync_count="$(extract_key_from_kv_line "$trial_summary" "resync_count")"
    bad_header="$(extract_rx_summary_value "$rx_log" "bad_header")"
    signature_hint="$(signature_hint_for_target "$target")"

    echo "${target},${TRIAL},${link_name},${RATE_HZ},${duration_sec},${PAYLOAD_LEN},${FAULT_RATE},${recv_ok},${gap_est},${crc_fail},${len_invalid},${preamble_miss},${resync_count},${bad_header},${signature_hint}" >> "$CSV"
    echo "[INFO]   summary=${trial_summary}"
done

echo "[INFO] 完了: ${CSV}"
