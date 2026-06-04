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
