#!/usr/bin/env bash
# Print the MCU telemetry counters that matter during link bring-up.
#
# Reads a bounded amount from the USB CDC port so it always terminates and never
# loses buffered output, then reports the newest row.
#
#   bash scripts/mcu_uart/telemetry_snapshot.sh [port] [seconds]

set -u

PORT="${1:-/dev/ttyACM0}"
SECONDS_TO_READ="${2:-6}"
CAPTURE="$(mktemp)"
trap 'rm -f "$CAPTURE"' EXIT

if [ ! -e "$PORT" ]; then
    echo "$PORT does not exist; the board is not enumerating over USB"
    exit 1
fi

# A reader left over from an earlier run keeps the port busy and starves this one.
pkill -x cat 2>/dev/null || true
sleep 1

# Without raw mode the line discipline holds the rows back and the read comes up
# empty even while the board is emitting normally.
stty -F "$PORT" raw -echo

# cat writes straight through, so the rows already read survive the timeout's
# signal. A byte-counting reader would buffer them and lose the lot when killed
# before reaching its count.
timeout "$SECONDS_TO_READ" cat "$PORT" > "$CAPTURE" || true

if [ ! -s "$CAPTURE" ]; then
    echo "no telemetry from $PORT within ${SECONDS_TO_READ}s"
    echo "the device node exists, so USB is served by interrupt while the main"
    echo "loop is not emitting rows: suspect the main loop is blocked"
    exit 1
fi

awk -F, '
/^#/ { configuration = $0; next }
$1 == "trial_id" { for (i = 1; i <= NF; i++) name[i] = $i; next }
NF > 5 { for (i = 1; i <= NF; i++) value[i] = $i; fields = NF; rows++ }
END {
    if (configuration != "") print configuration
    if (rows == 0) {
        print "header only; no telemetry rows were emitted"
        exit 1
    }
    split("mono_ms state last_error_code rx_byte_count rx_packet_count " \
          "rx_data_count tx_packet_count ack_sent_count heartbeat_sent_count " \
          "preamble_miss_count crc_error_count", keys, " ")
    for (k = 1; k in keys; k++) {
        for (i = 1; i <= fields; i++) {
            if (name[i] == keys[k]) printf "%-22s %s\n", keys[k], value[i]
        }
    }
    printf "%-22s %d\n", "rows_captured", rows
}' "$CAPTURE"
