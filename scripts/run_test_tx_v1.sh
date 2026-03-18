#!/usr/bin/env bash
#
# run_test_tx_v1.sh
#
# 目的:
#   - tx が Frame v1 を継続生成できることを短時間で確認する
#   - payload 長を変えても version / payload_len / crc32 / frame_len が破綻しないことを見る

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="logs/run_${TS}_tx_v1_test"
mkdir -p "$RUN_DIR"

echo "[INFO] run dir: $RUN_DIR"

make all

for payload_len in 0 7 48 128; do
    LOG_PATH="$RUN_DIR/tx_payload_${payload_len}.log"
    EXPECTED_FRAME_LEN=$((25 + payload_len))

    ./bin/tx \
        --dst-ip 127.0.0.1 \
        --dst-port 9000 \
        --rate-hz 10 \
        --duration-sec 1 \
        --log-path "$LOG_PATH" \
        --payload-len "$payload_len"

    if ! grep -q "frame_v1 config version=1 header_len=25 payload_len=${payload_len}" "$LOG_PATH"; then
        echo "[ERROR] missing frame_v1 config log for payload_len=${payload_len}"
        exit 1
    fi

    if ! grep -q "frame_v1 first_frame version=1 payload_len=${payload_len}" "$LOG_PATH"; then
        echo "[ERROR] missing first frame log for payload_len=${payload_len}"
        exit 1
    fi

    if ! grep -q "crc32=0x" "$LOG_PATH"; then
        echo "[ERROR] missing crc32 log for payload_len=${payload_len}"
        exit 1
    fi

    if ! grep -q "frame_len=${EXPECTED_FRAME_LEN}" "$LOG_PATH"; then
        echo "[ERROR] unexpected frame_len for payload_len=${payload_len} (expected ${EXPECTED_FRAME_LEN})"
        exit 1
    fi
done

echo "[INFO] tx v1 test passed"
echo "[INFO] logs:"
ls -l "$RUN_DIR"
