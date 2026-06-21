# W07 RTOS Jitter Summary

## Analysis Method

- Input directory: `data/w07`
- Dataset: Raspberry Pi Pico measured CSV, bare-metal / FreeRTOS each 3 runs
- Jitter metric: `abs(jitter_us)`
- Jitter samples: exclude sample 1 because its `delta_us=0` and `jitter_us=0` are synthetic
- Samples per jitter run: 999 intervals
- Mode summary: pooled 2997 intervals from 3 runs
- Percentiles: nearest-rank
- Stddev: population standard deviation
- Queue latency: all valid FreeRTOS events, including sample 1
- Deadline miss: the run-level final counter is counted once per run

## Distribution Figures

Bars represent every distinct observed value. The count axis is logarithmic so rare outliers remain visible; the exact count and percentage are printed for each bar.

![w07_baremetal_abs_jitter_distribution](figures/w07_baremetal_abs_jitter_distribution.svg)

![w07_freertos_abs_jitter_distribution](figures/w07_freertos_abs_jitter_distribution.svg)

![w07_freertos_queue_latency_distribution](figures/w07_freertos_queue_latency_distribution.svg)

## Run-level abs(jitter_us)

| mode | run | intervals | P50 (us) | P95 (us) | P99 (us) | max (us) | stddev (us) | deadline miss |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baremetal | run1 | 999 | 882.00 | 1839.00 | 1839.00 | 1840.00 | 447.96 | - |
| baremetal | run2 | 999 | 882.00 | 1839.00 | 1839.00 | 1840.00 | 447.96 | - |
| baremetal | run3 | 999 | 882.00 | 1839.00 | 1839.00 | 1840.00 | 447.96 | - |
| freertos | run1 | 999 | 0.00 | 0.00 | 0.00 | 21.00 | 0.68 | 0 |
| freertos | run2 | 999 | 0.00 | 0.00 | 0.00 | 85.00 | 4.39 | 0 |
| freertos | run3 | 999 | 0.00 | 0.00 | 1.00 | 21.00 | 0.69 | 0 |

## Mode-level abs(jitter_us)

| mode | intervals | P50 (us) | P95 (us) | P99 (us) | max (us) | stddev (us) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baremetal | 2997 | 882.00 | 1839.00 | 1839.00 | 1840.00 | 447.96 |
| freertos | 2997 | 0.00 | 0.00 | 0.00 | 85.00 | 2.60 |

## Bare-metal vs FreeRTOS

| metric | bare-metal (us) | FreeRTOS (us) | reduction (us) | reduction (%) |
| --- | ---: | ---: | ---: | ---: |
| P95 abs jitter | 1839.00 | 0.00 | 1839.00 | 100.00 |
| P99 abs jitter | 1839.00 | 0.00 | 1839.00 | 100.00 |

A positive reduction means that FreeRTOS has lower absolute jitter than bare-metal.
The timestamp is captured when the periodic TX event starts; this firmware does not send a UDP packet. Therefore, these results establish TX-event release jitter, not UDP API latency, driver completion time, or end-to-end packet latency.
A real UDP path may add queueing, task scheduling, buffer allocation, network-stack locking, and driver latency, so its ordering must be measured separately.
This is the Issue #105 numerical comparison draft; the final causal interpretation and evidence package are handled in Issue #107.

## FreeRTOS queue_latency_us

| scope | samples | P50 (us) | P95 (us) | P99 (us) | max (us) | stddev (us) | send fail | not received | deadline miss |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| run1 | 1000 | 8.00 | 8.00 | 8.00 | 80.00 | 2.29 | 0 | 0 | 0 |
| run2 | 1000 | 7.00 | 7.00 | 7.00 | 80.00 | 2.34 | 0 | 0 | 0 |
| run3 | 1000 | 7.00 | 7.00 | 7.00 | 80.00 | 2.33 | 0 | 0 | 0 |
| pooled | 3000 | 7.00 | 8.00 | 8.00 | 80.00 | 2.37 | 0 | 0 | 0 |

## Input Runs

- `data/w07/baremetal_run1.csv`
- `data/w07/baremetal_run2.csv`
- `data/w07/baremetal_run3.csv`
- `data/w07/freertos_run1.csv`
- `data/w07/freertos_run2.csv`
- `data/w07/freertos_run3.csv`
