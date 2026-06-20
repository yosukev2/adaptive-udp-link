# W07 Run Log

## Scope

Issue #101 places the W07 Raspberry Pi Pico firmware sources into the repository and defines build targets for:

- `w07_baremetal_jitter`
- `w07_freertos_jitter`

This log records build-layout status only. Raspberry Pi Pico flashing and USB CDC CSV capture are not performed in this issue.

## Source Placement

- `firmware/w07_rtos_jitter/baremetal_main.c`
- `firmware/w07_rtos_jitter/freertos_main.c`
- `firmware/w07_rtos_jitter/CMakeLists.txt`
- `firmware/w07_rtos_jitter/FreeRTOSConfig.h`
- `firmware/w07_rtos_jitter/README.md`

## External Dependencies

The following dependencies are expected outside the repository:

- Pico SDK via `PICO_SDK_PATH`
- FreeRTOS-Kernel via `FREERTOS_KERNEL_PATH`

Neither dependency is committed to this repository.

## Build Commands

Target Raspberry Pi 5 command plan:

```bash
export PICO_SDK_PATH=/home/pi5/pico/pico-sdk
export FREERTOS_KERNEL_PATH=/home/pi5/pico/FreeRTOS-Kernel
cmake -G Ninja -S firmware/w07_rtos_jitter -B firmware/w07_rtos_jitter/build
cmake --build firmware/w07_rtos_jitter/build
```

Expected outputs:

```text
firmware/w07_rtos_jitter/build/w07_baremetal_jitter.uf2
firmware/w07_rtos_jitter/build/w07_freertos_jitter.uf2
```

## Local Verification

- Firmware files were added under `firmware/w07_rtos_jitter/`.
- `CMakeLists.txt` defines both W07 targets.
- `FreeRTOSConfig.h` is included in the firmware directory.
- Pico SDK and FreeRTOS-Kernel are still external dependencies.

### Windows local configure check

Environment observed on the local development machine:

- `cmake`: available
- `arm-none-eabi-gcc`: available
- `PICO_SDK_PATH`: `C:\pico\pico-sdk`
- `FREERTOS_KERNEL_PATH`: not set
- `C:\pico\FreeRTOS-Kernel`: not present

Command:

```powershell
cmake -S firmware\w07_rtos_jitter -B firmware\w07_rtos_jitter\build-local-check -DW07_ENABLE_PICOTOOL=OFF
```

Result:

```text
Configuring incomplete.
FREERTOS_KERNEL_PATH is not set. Export it or pass -DFREERTOS_KERNEL_PATH=/path/to/FreeRTOS-Kernel.
```

Interpretation:

- Pico SDK discovery works on this machine.
- FreeRTOS-Kernel is intentionally not vendored in this repository.
- Full configure/build is deferred to W07-2 on Raspberry Pi 5 with `FREERTOS_KERNEL_PATH` set.

## Not Performed In This Issue

- Raspberry Pi 5 build with real Pico SDK and FreeRTOS-Kernel
- UF2 generation
- Pico flashing
- USB CDC serial CSV capture
- Real jitter measurement

These steps are intentionally left for W07-2, W07-3, and W07-4.

## Raspberry Pi 5でのビルド確認（Issue #102）

- 実施日時: `2026-06-11T08:15:03+09:00`
- ホスト: Raspberry Pi 5 / aarch64
- OS: Debian、Linux `6.12.75+rpt-rpi-2712`
- CMake: `3.31.6`
- ARM GCC: `14.2.1`
- Pico SDK: `2.2.0`
- FreeRTOS-Kernel: `V10.4.3-776-gd877cd539`
- Pico SDKパス: `/home/pi5/pico/pico-sdk`
- FreeRTOS-Kernelパス: `/home/pi5/pico/FreeRTOS-Kernel`

### 実行コマンド

```bash
export PICO_SDK_PATH=/home/pi5/pico/pico-sdk
export FREERTOS_KERNEL_PATH=/home/pi5/pico/FreeRTOS-Kernel
rm -rf firmware/w07_rtos_jitter/build
cmake -G Ninja -S firmware/w07_rtos_jitter -B firmware/w07_rtos_jitter/build
cmake --build firmware/w07_rtos_jitter/build --parallel
```

### ビルド結果

- CMake configure: 成功
- `w07_baremetal_jitter.uf2`: 生成成功、77K
- `w07_freertos_jitter.uf2`: 生成成功、100K
- `picotool`はUSBサポートなしでビルドされているが、UF2生成には影響しなかった

```text
113fd7585dcad4a571833aa2497a826b783727b86724e70416ad1fc64b275ff4  w07_baremetal_jitter.uf2
141232fedd42290e337c3c122964676ad7bcd35b4d6ccb548cbb45b00a616117  w07_freertos_jitter.uf2
```

### 未確認事項

- PicoへのUF2書き込み
- Pico実機でのfirmware実行
- USB CDC serialからのCSV取得

実機確認とCSV取得はIssue #103および#104で実施する。

## Pico bare-metal実機計測（Issue #103）

- 実施日時: `2026-06-20T21:55:44+09:00`
- ホスト: Raspberry Pi 5 / aarch64
- OS: Debian、Linux `6.12.75+rpt-rpi-2712`
- Git branch: `issue-103-w07-baremetal-csv`
- Git commit: `4cdb3a7ac1b1f60863fc3f648141b9ac9ea52c29`
- firmware: `w07_baremetal_jitter.uf2`
- firmware SHA256: `78402461cfafa6d5ece5a19c43fc485e880be14f3dc1b483bc64c92eb8ffcd85`
- USB CDC ID: `/dev/serial/by-id/usb-Raspberry_Pi_Pico_5303284728FC519C-if00`
- USB CDC device: `/dev/ttyACM0`

### UF2書き込み

PicoをBOOTSELモードで接続し、`/dev/sdb1`をマウントした。

```bash
udisksctl mount -b /dev/sdb1
cp firmware/w07_rtos_jitter/build/w07_baremetal_jitter.uf2 \
  /media/pi5/RPI-RP2/
```

UF2書き込み後、Picoは自動的に通常起動し、USB CDC serialとして認識された。

### CSV取得

各runの取得前にPicoを通常再起動した。run 2とrun 3ではBOOTSELを使用せず、USBの抜き差しで再起動した。

```bash
stty -F /dev/ttyACM0 115200 raw -echo
timeout 20s cat /dev/ttyACM0 > data/w07/baremetal_run1.csv
```

run 2、run 3も同じ方法で、それぞれ以下へ保存した。

- `data/w07/baremetal_run1.csv`
- `data/w07/baremetal_run2.csv`
- `data/w07/baremetal_run3.csv`

`timeout`の終了コードは全runで`124`だった。firmwareがCSV出力後もUSB CDCを閉じないためであり、想定どおりである。

### 検証結果

全runで以下を確認した。

- CSVはheader 1行 + data 1000行の合計1001行
- headerは`mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us`
- `mode=baremetal`
- `sample_index=1..1000`
- `period_target_us=10000`
- `jitter_us = delta_us - period_target_us`
- timestamp差分と`delta_us`が一致
- `index_errors=0`
- `mode_period_errors=0`
- `formula_errors=0`

計測中はtimestampをメモリへ保存し、1000サンプル取得後にまとめて`printf`する実装である。
