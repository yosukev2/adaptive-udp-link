# w07_rtos_jitter

Issue #101 adds the W07 Raspberry Pi Pico firmware layout for comparing a bare-metal single-loop sender against a FreeRTOS task-separated sender.

## Targets

- `w07_baremetal_jitter`: single loop, absolute 10 ms schedule, simulated RX workload in the same loop
- `w07_freertos_jitter`: `tx_task`, `rx_task`, and `state_task` with FreeRTOS Queue/Semaphore coordination

Both targets use USB CDC serial for CSV output. GPIO UART wiring is not required for W07.

## Measurement Rules

- Target period: `10000 us`
- Sample count: 1000
- Measurement timestamps are stored in memory during capture
- No `printf` is performed inside the timing-critical measurement path
- CSV output happens only after capture completes
- Pico SDK and FreeRTOS-Kernel are external dependencies and are not committed to this repository

## CSV Schemas

Bare-metal:

```text
mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

FreeRTOS:

```text
mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us,queue_latency_us,deadline_miss_count
```

`queue_latency_us` uses:

```text
state_task_receive_time_us - tx_task_queue_send_time_us
```

Special values:

- `-1`: queue send failed
- `-2`: queue event was not received before completion handling

## Build

Prerequisites:

- Pico SDK installed outside this repository
- FreeRTOS-Kernel installed outside this repository
- `PICO_SDK_PATH` points to Pico SDK
- `FREERTOS_KERNEL_PATH` points to FreeRTOS-Kernel
- `arm-none-eabi-gcc`, CMake, and a supported generator are available

Example:

```bash
export PICO_SDK_PATH=/home/pi5/pico/pico-sdk
export FREERTOS_KERNEL_PATH=/home/pi5/pico/FreeRTOS-Kernel
cmake -G Ninja -S firmware/w07_rtos_jitter -B firmware/w07_rtos_jitter/build
cmake --build firmware/w07_rtos_jitter/build
```

Expected UF2 outputs:

- `firmware/w07_rtos_jitter/build/w07_baremetal_jitter.uf2`
- `firmware/w07_rtos_jitter/build/w07_freertos_jitter.uf2`

## Current Status

This issue is build-layout work only. Pico hardware execution and CSV capture are handled by later W07 issues.
