#!/usr/bin/env bash
#
# run_frame_integrity.sh
#
# 目的:
#   - W02 DoD: 破損率 4 条件 × 3 回 = 12 実験を実施し frame_integrity.csv を生成する
#   - 各条件で recv_ok / crc_fail / preamble_miss / len_invalid / resync_count を収集する
#   - W03 以降の単一 fault 比較基準として残す
#
# 実験条件:
#   - fault-target: crc（CRC 棄却 → resync の関係を中心に観測）
#   - fault-rate: 0.00 / 0.01 / 0.05 / 0.10（各 3 回）
#   - rate-hz: 100 frame/s、duration: 30 秒
#
# 実行方法:
#   bash scripts/run_frame_integrity.sh
#
# 出力:
#   logs/frame_integrity/frame_integrity.csv
#   logs/frame_integrity/run_*/  （各実験の生ログ）

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

RESULT_DIR="logs/frame_integrity"
mkdir -p "$RESULT_DIR"

CSV="$RESULT_DIR/frame_integrity.csv"

# 実験パラメータ
FAULT_TARGET="crc"
RATE_HZ=100
DURATION_SEC=30
PORT=9000
BIND_IP="127.0.0.1"
DST_IP="127.0.0.1"

# 破損率 4 条件
FAULT_RATES=("0.00" "0.01" "0.05" "0.10")
CONDITION_NAMES=("A_none" "B_low" "C_mid" "D_high")
TRIALS=3

# OS情報（実験条件の記録用）
OS_INFO="$(uname -sr)"

echo "[INFO] frame_integrity 実験開始"
echo "[INFO] fault_target=${FAULT_TARGET} rate_hz=${RATE_HZ} duration_sec=${DURATION_SEC}"
echo "[INFO] 出力先: ${CSV}"

# CSV ヘッダ
cat > "$CSV" <<'HEADER'
condition,trial,fault_rate,recv_ok,crc_fail,preamble_miss,len_invalid,resync_count,parse_ok_rate
HEADER

# parse_ok_rate 計算関数
# parse_ok_rate = recv_ok / (recv_ok + crc_fail + preamble_miss + len_invalid)
calc_parse_ok_rate() {
    local recv_ok="$1"
    local crc_fail="$2"
    local preamble_miss="$3"
    local len_invalid="$4"
    local total=$(( recv_ok + crc_fail + preamble_miss + len_invalid ))
    if [ "$total" -eq 0 ]; then
        echo "0.000"
    else
        python3 -c "print(f'{${recv_ok}/${total}:.3f}')"
    fi
}

# サマリログからカウンタ値を抽出する関数
extract_counter() {
    local log="$1"
    local key="$2"
    grep "rx summary" "$log" | grep -o "${key}=[0-9]*" | cut -d= -f2 | tail -1
}

# 全実験ループ
for ci in "${!FAULT_RATES[@]}"; do
    FAULT_RATE="${FAULT_RATES[$ci]}"
    COND_NAME="${CONDITION_NAMES[$ci]}"

    echo ""
    echo "[INFO] === 条件 ${COND_NAME} (fault_rate=${FAULT_RATE}) ==="

    for trial in $(seq 1 $TRIALS); do
        TS="$(date +%Y%m%d_%H%M%S)"
        RUN_DIR="${RESULT_DIR}/run_${COND_NAME}_trial${trial}_${TS}"
        mkdir -p "$RUN_DIR"

        RX_LOG="${RUN_DIR}/rx.log"
        TX_LOG="${RUN_DIR}/tx.log"

        echo "[INFO] trial=${trial} run_dir=${RUN_DIR}"

        # rx をバックグラウンドで起動
        ./bin/rx \
            --bind-ip "$BIND_IP" \
            --port "$PORT" \
            --duration-sec "$DURATION_SEC" \
            --log-path "$RX_LOG" &
        RX_PID=$!
        sleep 1

        # tx をフォアグラウンドで起動
        if [ "$(echo "$FAULT_RATE > 0" | bc -l)" -eq 1 ]; then
            ./bin/tx \
                --dst-ip "$DST_IP" \
                --dst-port "$PORT" \
                --rate-hz "$RATE_HZ" \
                --duration-sec "$DURATION_SEC" \
                --log-path "$TX_LOG" \
                --fault-target "$FAULT_TARGET" \
                --fault-rate "$FAULT_RATE"
        else
            ./bin/tx \
                --dst-ip "$DST_IP" \
                --dst-port "$PORT" \
                --rate-hz "$RATE_HZ" \
                --duration-sec "$DURATION_SEC" \
                --log-path "$TX_LOG"
        fi

        wait "$RX_PID" || true

        # カウンタ抽出
        RECV_OK=$(extract_counter "$RX_LOG" "recv_ok")
        CRC_FAIL=$(extract_counter "$RX_LOG" "crc_fail")
        PREAMBLE_MISS=$(extract_counter "$RX_LOG" "preamble_miss")
        LEN_INVALID=$(extract_counter "$RX_LOG" "len_invalid")
        RESYNC_COUNT=$(extract_counter "$RX_LOG" "resync_count")

        # parse_ok_rate 計算
        TOTAL=$(( RECV_OK + CRC_FAIL + PREAMBLE_MISS + LEN_INVALID ))
        if [ "$TOTAL" -gt 0 ]; then
            PARSE_OK_RATE=$(python3 -c "print(f'{${RECV_OK}/${TOTAL}:.3f}')")
        else
            PARSE_OK_RATE="0.000"
        fi

        echo "[INFO]   recv_ok=${RECV_OK} crc_fail=${CRC_FAIL} preamble_miss=${PREAMBLE_MISS} len_invalid=${LEN_INVALID} resync_count=${RESYNC_COUNT} parse_ok_rate=${PARSE_OK_RATE}"

        # CSV 追記
        echo "${COND_NAME},${trial},${FAULT_RATE},${RECV_OK},${CRC_FAIL},${PREAMBLE_MISS},${LEN_INVALID},${RESYNC_COUNT},${PARSE_OK_RATE}" >> "$CSV"

        # 連続実行の間隔
        sleep 2
    done
done

echo ""
echo "[INFO] === 全実験完了 ==="
echo "[INFO] 結果: ${CSV}"
echo ""

# 集計サマリ表示
echo "=== frame_integrity.csv ==="
cat "$CSV"
echo ""

# 実験条件の記録
META="${RESULT_DIR}/experiment_conditions.txt"
cat > "$META" <<EOF
# 実験条件

実施日時: $(date '+%Y-%m-%d %H:%M:%S')
OS: ${OS_INFO}
送信レート: ${RATE_HZ} frame/s
計測時間: ${DURATION_SEC} 秒/試行
ペイロードサイズ: tx デフォルト（frame_v1_wire.h の kFrameV1DefaultPayloadLen による）
fault-target: ${FAULT_TARGET}
破損率（fault-rate）:
  条件A: 0.00（破損なし）
  条件B: 0.01（約1%）
  条件C: 0.05（約5%）
  条件D: 0.10（約10%）
試行回数: ${TRIALS} 回/条件
ネットワーク: ローカルループバック（127.0.0.1）
TX_FRAMES_PER_DATAGRAM: 3（1 datagram = 3 frame 連結）

# parse_ok_rate の計算式
# parse_ok_rate = recv_ok / (recv_ok + crc_fail + preamble_miss + len_invalid)
EOF

echo "[INFO] 実験条件: ${META}"
