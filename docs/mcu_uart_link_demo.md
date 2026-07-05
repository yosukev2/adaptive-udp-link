# MCU UART Link Control Demo

## Purpose

MCU UART Link Control Demo は、PC を相手端末として UART 経由で packet v1 を送受信し、MCU 側の通信状態と復旧結果を CSV で比較できるようにするための実験系である。

この文書では Issue #188 の範囲として、リポジトリ構成、build、flash、run、log 保存先を固定する。

## Repository Layout

```text
adaptive-udp-link/
├── firmware/
│   └── mcu_uart_link/          # MCU firmware
├── scripts/
│   └── mcu_uart/               # PC-side UART harness and analysis tools
├── docs/
│   └── mcu_uart/
│       ├── protocol.md         # packet format v1
│       ├── telemetry_schema.md # MCU telemetry counters
│       └── log_schema.md       # CSV log columns
├── logs/
│   └── mcu_uart/<trial_id>/    # real run logs
└── data/
    └── mcu_uart/               # sample logs and curated datasets
```

## Fixed Paths

| Item | Path | Notes |
|------|------|-------|
| MCU firmware | `firmware/mcu_uart_link/` | Raspberry Pi Pico SDK style CMake project by default |
| PC test harness | `scripts/mcu_uart/pc_harness.py` | Serial sender/receiver and dry-run packet generator |
| Summary generator | `scripts/mcu_uart/generate_summary.py` | Creates `summary.csv` from run logs |
| Protocol spec | `docs/mcu_uart/protocol.md` | Packet v1 source of truth |
| Telemetry schema | `docs/mcu_uart/telemetry_schema.md` | MCU counter definitions |
| Run logs | `logs/mcu_uart/<trial_id>/` | One directory per trial |
| Sample logs | `data/mcu_uart/sample_baseline/` | Hardware-free sample input/output |

## Prerequisites

Host-side:

- Python 3.10 or newer
- Optional: `pyserial` for real UART access

MCU-side default:

- Raspberry Pi Pico SDK outside this repository
- `PICO_SDK_PATH` pointing at the Pico SDK
- CMake and Ninja or Make
- `arm-none-eabi-gcc`

## Build

Default firmware build target is `firmware/mcu_uart_link`.

```bash
export PICO_SDK_PATH=/path/to/pico-sdk
cmake -G Ninja -S firmware/mcu_uart_link -B firmware/mcu_uart_link/build
cmake --build firmware/mcu_uart_link/build
```

Expected output when firmware sources are present:

```text
firmware/mcu_uart_link/build/mcu_uart_link.uf2
```

If a different MCU board is used, keep the same repository paths and replace only the board-specific toolchain commands in `firmware/mcu_uart_link/README.md`.

## Flash

Raspberry Pi Pico UF2 copy flow:

```bash
export PICO_MOUNT=/media/$USER/RPI-RP2
cp firmware/mcu_uart_link/build/mcu_uart_link.uf2 "$PICO_MOUNT/"
```

Pico steps:

1. Hold `BOOTSEL`.
2. Connect USB.
3. Confirm the board is mounted as `RPI-RP2`.
4. Copy the UF2.
5. The board reboots automatically.

## Run

Dry-run without MCU:

```bash
python scripts/mcu_uart/pc_harness.py \
  --dry-run \
  --trial-id m0_dryrun_001 \
  --packet-count 10 \
  --payload-len 16 \
  --output-dir logs/mcu_uart/m0_dryrun_001
```

Real UART run:

```bash
python scripts/mcu_uart/pc_harness.py \
  --port /dev/ttyUSB0 \
  --baudrate 115200 \
  --trial-id m0_baseline_001 \
  --packet-count 10 \
  --payload-len 16 \
  --output-dir logs/mcu_uart/m0_baseline_001
```

Windows port example:

```powershell
python scripts/mcu_uart/pc_harness.py `
  --port COM5 `
  --baudrate 115200 `
  --trial-id m0_baseline_001 `
  --packet-count 10 `
  --payload-len 16 `
  --output-dir logs/mcu_uart/m0_baseline_001
```

Generate summary:

```bash
python scripts/mcu_uart/generate_summary.py \
  --input-dir logs/mcu_uart/m0_baseline_001 \
  --output logs/mcu_uart/m0_baseline_001/summary.csv
```

## Log Outputs

Each trial directory should contain:

| File | Producer | Required for summary | Notes |
|------|----------|----------------------|-------|
| `run_metadata.csv` or `run_metadata.md` | Operator or harness | Yes | Trial condition metadata |
| `pc_tx_log.csv` | PC harness | Yes | Transmitted packet records |
| `pc_rx_log.csv` | PC harness | Yes | Received ACK/NACK/telemetry records |
| `mcu_telemetry.csv` | MCU firmware | Recommended | MCU counters by timestamp |
| `summary.csv` | Summary generator | Output | Pass/fail and aggregate counts |

## Minimum M0 Baseline Conditions

| Field | Value |
|-------|-------|
| Packet count | 10 |
| Packet type | `DATA` |
| Payload length | 16 bytes unless a trial states otherwise |
| Baudrate | 115200 by default |
| Fault injection | Disabled |
| Expected CRC errors | 0 |
| Expected sequence gaps | 0 |
| Expected MCU state | `RUN` or equivalent healthy state |

## Completion Boundary

Issue #188 is complete when:

- The firmware, PC harness, docs, logs, and sample data paths are fixed.
- The build, flash, run, and summary commands are documented.
- A dry-run can produce PC-side logs without MCU hardware.
- A real baseline run has an explicit log directory and command sequence.

Real hardware execution belongs to Issue #194 and must not be marked complete from dry-run logs alone.
