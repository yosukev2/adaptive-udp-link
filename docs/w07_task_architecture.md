# W07 Task Architecture

## Scope

This document describes the W07 FreeRTOS firmware architecture for Raspberry Pi Pico and how it is compared against the bare-metal single-loop firmware.

W07 runs both firmware variants on Raspberry Pi Pico. Raspberry Pi 5 is only the host for build, UF2 flashing, USB CDC serial capture, analysis, and Git operations.

## Firmware Variants

| variant | target | source | purpose |
| --- | --- | --- | --- |
| bare-metal | `w07_baremetal_jitter` | `firmware/w07_rtos_jitter/baremetal_main.c` | Single-loop baseline with TX timing check and RX-like workload in the same loop |
| FreeRTOS | `w07_freertos_jitter` | `firmware/w07_rtos_jitter/freertos_main.c` | Task-separated design with prioritized TX task and lower-priority RX/state tasks |

## FreeRTOS Tasks

| task | priority | responsibility | timing or blocking behavior |
| --- | ---: | --- | --- |
| `tx_task` | 3 | Captures 10 ms TX-event timestamps and sends event metadata to `state_task` | Highest priority; uses `xTaskDelayUntil()` for periodic timing |
| `rx_task` | 2 | Runs simulated receive workload | Lower than TX; yields after each workload iteration |
| `state_task` | 1 | Receives TX events, calculates queue latency, waits for completion, and prints CSV after capture | Blocks on `xQueueReceive()` and `xSemaphoreTake()` |

`tx_task` is intentionally the highest-priority task so receive-side load and state handling do not preempt the timing-critical TX path.

## Communication

The FreeRTOS firmware uses both a Queue and a Semaphore.

| primitive | producer | consumer | purpose |
| --- | --- | --- | --- |
| Queue `g_tx_event_queue` | `tx_task` | `state_task` | Transfers `sample_index`, TX timestamp, and queue-send timestamp |
| Binary Semaphore `g_capture_done_sem` | `tx_task` | `state_task` | Signals that timestamp capture is complete |

The queue carries per-sample timing metadata. The semaphore is a completion signal. `state_task` does not busy-loop on capture completion.

## 10 ms Timing

### Bare-metal

The bare-metal variant uses an absolute schedule:

```c
target_time_us += PERIOD_TARGET_US;
```

This avoids accumulating drift from each loop iteration into the next target timestamp.

### FreeRTOS

The FreeRTOS variant uses:

```c
xTaskDelayUntil(&last_wake, pdMS_TO_TICKS(10));
```

This keeps the TX task on a periodic schedule relative to the previous planned wake tick. `xTaskCreate()` only registers the task and priority; it does not define the period.

## Capture And CSV Output

Both variants follow the same measurement rule:

- Store timestamps in memory during capture.
- Do not print from the timing-critical path during measurement.
- Output CSV only after 1000 samples are captured.
- Use USB CDC serial for CSV output.
- Do not require GPIO UART wiring.

Bare-metal CSV:

```text
mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

FreeRTOS CSV:

```text
mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us,queue_latency_us,deadline_miss_count
```

The common fields allow direct jitter comparison. The FreeRTOS-only fields capture task-separation overhead and scheduling health.

## Measured Metrics

| metric | source | interpretation |
| --- | --- | --- |
| `jitter_us` | both variants | `delta_us - period_target_us` |
| `abs(jitter_us)` | analysis script | Basis for P50/P95/P99/max/stddev |
| `queue_latency_us` | FreeRTOS only | Approximate timestamp delta from TX event queue send to state-task receive |
| `deadline_miss_count` | FreeRTOS only | Count of missed `xTaskDelayUntil()` wake deadlines |

`queue_latency_us` is the W07 practical proxy for task switch or task handoff overhead in the current design.

Special FreeRTOS latency values:

- `-1`: queue send failed in `tx_task`
- `-2`: queue event was not received before completion handling

## Comparison Conditions

The intended comparison keeps these conditions aligned:

- Same board class: Raspberry Pi Pico.
- Same target period: `10000 us`.
- Same sample count: 1000 per run.
- Same RX workload iteration constant unless explicitly changed and documented.
- Same USB CDC serial output after capture.
- Same statistic basis: `abs(jitter_us)`.

The two implementations intentionally differ in scheduling model:

- bare-metal uses one loop for TX timing and RX-like work.
- FreeRTOS separates TX, RX, and state handling into tasks with explicit priority.

## Limitations

- This document describes the intended architecture; real jitter claims require Pico CSV captures.
- Queue latency is not a full CPU context-switch trace. It is an end-to-end task handoff timestamp delta.
- Results may change with FreeRTOS tick rate, compiler options, RX workload, USB CDC behavior, and Pico SDK/FreeRTOS versions.
