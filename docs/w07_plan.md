# W07 Plan

## Scope

W07 compares Raspberry Pi Pico firmware variants:

- bare-metal single-loop timing
- FreeRTOS task-separated timing

Raspberry Pi 5 is used only as the host for build, flashing, USB CDC serial capture, analysis, and Git operations. W07 does not run an RTOS experiment on Raspberry Pi 5 Linux.

## Reference Files

The `ref/` directory supplied for W07 contains:

- `ref/baremetal_main.c`
- `ref/freertos_main.c`
- `ref/CMakeLists.txt`

These files are reference inputs, not final repository layout.

## Reference Assessment

### `baremetal_main.c`

Role: bare-metal Pico comparison target.

Assessment:

- Captures 1000 TX-event timestamps.
- Uses an absolute 10 ms schedule with `target_time_us += PERIOD_TARGET_US`.
- Includes simulated RX workload in the same loop.
- Does not print during capture.
- Prints CSV after capture completes.
- CSV fields are comparable with the FreeRTOS output for the common jitter fields.

Required adjustment:

- Use `sample_index` as `1..1000` in the formal repository version to match existing W06 data conventions.

### `freertos_main.c`

Role: FreeRTOS Pico task-separated comparison target.

Assessment:

- Defines `tx_task`, `rx_task`, and `state_task`.
- Gives `tx_task` the highest priority.
- Uses `xTaskDelayUntil()` for 10 ms periodic timing.
- Does not print from `tx_task` during capture.
- Stores timestamps in memory before CSV output.
- Prints CSV from `state_task` after capture completes.
- Uses both Queue and Semaphore.
- Records `queue_latency_us`.
- Records `deadline_miss_count`.

Required adjustment:

- Add `FreeRTOSConfig.h`; the reference set does not include it.
- Keep FreeRTOS tasks from returning; use `vTaskSuspend(NULL)` or equivalent terminal handling.
- Ensure `state_task` waits on Queue/Semaphore rather than busy-looping on completion state.

### `CMakeLists.txt`

Role: standalone Pico SDK build definition for the two W07 firmware targets.

Assessment:

- Defines the intended `w07_baremetal_jitter` and `w07_freertos_jitter` targets.
- Imports Pico SDK externally.
- References FreeRTOS-Kernel externally.
- Does not vendor Pico SDK or FreeRTOS-Kernel.

Required adjustment:

- Use the repository's existing Pico firmware style from `firmware/w06_pico_jitter/`.
- Require `PICO_SDK_PATH` explicitly through CMake variable or environment.
- Require `FREERTOS_KERNEL_PATH` explicitly through CMake variable or environment.
- Add `FreeRTOSConfig.h` in the W07 firmware directory.

## Formal Placement

The formal W07 firmware location is:

```text
firmware/w07_rtos_jitter/
```

Expected files:

- `firmware/w07_rtos_jitter/baremetal_main.c`
- `firmware/w07_rtos_jitter/freertos_main.c`
- `firmware/w07_rtos_jitter/CMakeLists.txt`
- `firmware/w07_rtos_jitter/FreeRTOSConfig.h`
- `firmware/w07_rtos_jitter/README.md`

## External Dependencies

Do not commit these dependencies:

- Pico SDK
- FreeRTOS-Kernel

The build should use:

- `PICO_SDK_PATH`
- `FREERTOS_KERNEL_PATH`

## Milestone 8 DoD Mapping

| Milestone DoD | Planned evidence |
| --- | --- |
| bare-metal vs RTOS comparison table with P95/P99 for three runs | `reports/w07_rtos_jitter_summary.md`, `data/w07/w07_jitter_summary.csv` |
| Task architecture with task names, priorities, and communication method | `docs/w07_task_architecture.md` |
| Three or more CSV logs saved | `data/w07/baremetal_run1.csv` through `baremetal_run3.csv`, `data/w07/freertos_run1.csv` through `freertos_run3.csv` |
| Interpretation of RTOS improvement or regression | `reports/w07_rtos_jitter_summary.md` |
| Task switch overhead or equivalent timestamp delta | `queue_latency_us` in FreeRTOS CSV and derived statistics |

## Execution Order

1. #100: Confirm `ref/` code and W07 plan.
2. #101: Place W07 firmware and build targets.
3. #102: Build both firmware targets on Raspberry Pi 5.
4. #103: Capture bare-metal CSV runs on Pico.
5. #104: Capture FreeRTOS CSV runs on Pico.
6. #105: Analyze CSVs and generate comparison tables.
7. #106: Document FreeRTOS task architecture.
8. #107: Final interpretation and evidence package.

## Non-Scope For Planning Issue

- No Pico flashing.
- No USB CDC serial capture.
- No generated CSV data.
- No measured jitter claims.

Real measurements start only after the W07 firmware is built and run on Raspberry Pi Pico.
