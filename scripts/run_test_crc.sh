#!/usr/bin/env bash
#
# run_test_crc.sh
#
# 目的:
#   - tx/rx の --crc32-test を同じ手順で実行する
#   - 共有の test frame から同じ CRC32 が得られることを確認する
#   - 実行結果を logs/ に残して比較しやすくする

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
RUN_DIR="logs/run_${TS}_crc_test"
mkdir -p "$RUN_DIR"

TX_OUT="$RUN_DIR/tx_crc_test.log"
RX_OUT="$RUN_DIR/rx_crc_test.log"
DIFF_OUT="$RUN_DIR/tx_rx_crc.diff"

echo "[INFO] run dir: $RUN_DIR"

# 既存の build 手順に合わせて、先に tx/rx を作る。
make all

# CRC テストモードはネットワークを使わないので、個別に実行して出力を保存する。
./bin/tx --crc32-test > "$TX_OUT" 2>&1
./bin/rx --crc32-test > "$RX_OUT" 2>&1

# 同じ test frame を共有しているため、出力が一致しない場合は tx/rx の実装差分を疑う。
if ! diff -u "$TX_OUT" "$RX_OUT" > "$DIFF_OUT"; then
    echo "[ERROR] tx/rx crc32 test outputs differ"
    echo "[ERROR] diff: $DIFF_OUT"
    exit 1
fi

echo "[INFO] crc32 test passed"
echo "[INFO] tx output:"
cat "$TX_OUT"
echo "[INFO] logs:"
ls -l "$RUN_DIR"
