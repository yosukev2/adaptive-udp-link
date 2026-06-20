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
