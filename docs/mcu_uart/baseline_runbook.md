# MCU UART Baseline Runbook

## 目的

Issue #194 の実機 baseline を取得するための手順を固定する。dry-run は実装検証には使えるが、正常通信 baseline の完了条件には含めない。

## 前提

- MCU firmware が `docs/mcu_uart/protocol.md` の packet v1 を受信できる。
- MCU firmware が `docs/mcu_uart/log_schema.md` の `mcu_telemetry.csv` 相当の telemetry を出せる。
- PC 側に Python 3 と `pyserial` がある。
- PC と MCU の UART 配線、GND 共有、電圧レベルが正しい。

## dry-run

```bash
python scripts/mcu_uart/pc_harness.py \
  --dry-run \
  --trial-id m0_dryrun_001 \
  --packet-count 10 \
  --payload-len 16 \
  --output-dir logs/mcu_uart/m0_dryrun_001
```

```bash
python scripts/mcu_uart/generate_summary.py \
  --input-dir logs/mcu_uart/m0_dryrun_001 \
  --output logs/mcu_uart/m0_dryrun_001/summary.csv \
  --note "dry-run only; no MCU hardware observed"
```

期待結果:

- `pc_tx_log.csv` に 10 行の DATA packet が出る。
- `summary.csv` の `pass_fail` は `TEMPLATE_ONLY`。
- `hardware_observed=false`。

## 実機 baseline

Linux:

```bash
python -m pip install pyserial
python scripts/mcu_uart/pc_harness.py \
  --port /dev/ttyUSB0 \
  --baudrate 115200 \
  --trial-id m0_baseline_001 \
  --packet-count 10 \
  --payload-len 16 \
  --output-dir logs/mcu_uart/m0_baseline_001
```

Windows:

```powershell
python -m pip install pyserial
python scripts/mcu_uart/pc_harness.py `
  --port COM5 `
  --baudrate 115200 `
  --trial-id m0_baseline_001 `
  --packet-count 10 `
  --payload-len 16 `
  --output-dir logs/mcu_uart/m0_baseline_001
```

MCU telemetry を別経路で保存する場合は、同じ trial directory に `mcu_telemetry.csv` として置く。

summary 生成:

```bash
python scripts/mcu_uart/generate_summary.py \
  --input-dir logs/mcu_uart/m0_baseline_001 \
  --output logs/mcu_uart/m0_baseline_001/summary.csv \
  --note "M0 no-fault 10 packet baseline"
```

## PASS 条件

- `sent_count=10`
- `received_count=10`
- `crc_error_count=0`
- `seq_gap_count=0`
- `duplicate_count=0`
- `overflow_count=0`
- `buffer_miss_count=0`
- `unrecovered_count=0`
- `safe_enter_count=0`
- `hardware_observed=true`
- `pass_fail=PASS`

## FAIL 時に確認する項目

- UART TX/RX のクロス接続
- GND 共有
- baudrate 不一致
- 3.3V/5V レベル不一致
- MCU firmware が packet v1 と同じ endian/CRC 対象範囲を使っているか
- `mcu_telemetry.csv` の `last_error_code`
