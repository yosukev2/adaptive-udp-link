#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

BUILD_DIR="firmware/w06_pico_jitter/build"
UF2_GLOB="$BUILD_DIR/*.uf2"
MOUNT_DIR="/mnt/pico"
OUT_CSV="data/w06/pico_jitter_raw.csv"

echo "[1/7] Check Pico BOOTSEL device"

PICO_DEV=$(lsblk -rno NAME,SIZE,RM,TYPE | \
    awk '$2=="128M" && $3=="1" && $4=="part"{print "/dev/"$1; exit}')

if [ -z "${PICO_DEV:-}" ]; then
    echo "ERROR: Pico BOOTSEL device not found."
    echo "Hold BOOTSEL, reconnect Pico, then run again."
    exit 1
fi

LABEL=$(sudo blkid -o value -s LABEL "$PICO_DEV" 2>/dev/null || true)

if [ "$LABEL" != "RPI-RP2" ]; then
    echo "ERROR: Found 128M removable partition, but label is not RPI-RP2."
    echo "Device: $PICO_DEV"
    echo "Label : ${LABEL:-none}"
    exit 1
fi

echo "Found Pico: $PICO_DEV"

echo "[2/7] Build firmware"

rm -rf "$BUILD_DIR"

cmake -S firmware/w06_pico_jitter \
      -B "$BUILD_DIR"

cmake --build "$BUILD_DIR"

echo "[3/7] Check UF2"

UF2_FILE=$(find "$BUILD_DIR" -maxdepth 1 -name "*.uf2" | head -n 1)

if [ -z "${UF2_FILE:-}" ]; then
    echo "ERROR: UF2 file not found."
    exit 1
fi

echo "UF2: $UF2_FILE"

echo "[4/7] Flash UF2 to Pico"

sudo mkdir -p "$MOUNT_DIR"
sudo umount "$MOUNT_DIR" 2>/dev/null || true
sudo mount "$PICO_DEV" "$MOUNT_DIR"

sudo cp "$UF2_FILE" "$MOUNT_DIR/"
sync
sudo umount "$MOUNT_DIR"

echo "[5/7] Wait for Pico reboot"

sleep 5

if [ ! -e /dev/ttyACM0 ]; then
    echo "ERROR: /dev/ttyACM0 not found."
    echo "Check USB connection or run: ls /dev/ttyACM*"
    exit 1
fi

echo "[6/7] Capture CSV"

mkdir -p "$(dirname "$OUT_CSV")"
rm -f "$OUT_CSV"

timeout 20s cat /dev/ttyACM0 > "$OUT_CSV" || true

echo "[7/7] Verify result"

wc -l "$OUT_CSV"
head -n 2 "$OUT_CSV"
tail -n 2 "$OUT_CSV"

echo "Saved: $OUT_CSV"
