# W08 Linux UDP Code Inventory

## Scope

This inventory records the current behavior of `src/tx.c` and `src/rx.c` before W08 adds socket-buffer and CPU-affinity controls. It distinguishes controls already exposed by the programs from work required by later W08 issues.

Both programs use `CLOCK_MONOTONIC`. End-to-end latency is calculated from the TX timestamp carried in the frame and the RX timestamp, so W08 must keep `tx` and `rx` on the same Raspberry Pi 5 unless clock synchronization is separately designed and validated.

## `tx` CLI

| option | required | accepted value / default | current behavior |
| --- | --- | --- | --- |
| `--dst-ip` | yes | IPv4 address | Destination passed to `inet_pton()`. |
| `--dst-port` | yes | `1..65535` | UDP destination port. |
| `--rate-hz` | yes | integer `> 0` | Frame rate. With 3 frames per datagram, datagram period is `3e9 / rate_hz` ns with remainder correction. |
| `--duration-sec` | yes | integer `> 0` | Stops the send loop after the configured monotonic duration. |
| `--log-path` | yes | filesystem path | Human-readable start, periodic statistics, summary, and end log; opened in append mode. |
| `--payload-len` | no | default `48`; range `0..1024` | Payload bytes per frame. |
| `--version` | no | default and only supported value `1` | Rejects unsupported versions. |
| `--fault-target` | no | `preamble`, `payload_len`, `crc`, `payload`, `header` | Enables the selected corruption target. Omission means no corruption. |
| `--fault-rate` | no | floating point `0.0..1.0` | Per-frame corruption probability when a fault target is enabled. |
| `--outage-at-sec` | no | integer `>= 0` | Must be paired with `--outage-duration-ms`. |
| `--outage-duration-ms` | no | integer `> 0` | Suppresses sends during the configured outage interval. |
| `--crc32-test` | no | flag | Runs the CRC test path; unlike `rx`, current TX argument validation still requires the normal mandatory options. |

`--rate-hz` already provides the W08 send-interval control. It is a frame rate, not a datagram rate: `rate-hz=100` produces approximately 33.3 datagrams/s with 3 frames per datagram, or 100 frames/s.

## `rx` CLI

| option | required | accepted value / default | current behavior |
| --- | --- | --- | --- |
| `--bind-ip` | no | default `0.0.0.0` | IPv4 bind address. W08 passes `127.0.0.1` explicitly. |
| `--port` | yes | `1..65535` | UDP bind port. |
| `--duration-sec` | yes | integer `> 0` | Stops the receive loop after the configured monotonic duration. |
| `--log-path` | yes | filesystem path | Human-readable configuration, statistics, trial summary, and end log; opened in append mode. |
| `--link-name` | no | default `unknown` | Comparison label. It must be paired with `--trial` to collect latency percentile samples. |
| `--trial` | no | integer `> 0`; default `0` | Trial identifier. It must be paired with `--link-name` for percentile collection. |
| `--csv-in-1sec-log-path` | no | filesystem path | Creates a one-row-per-second statistics CSV. |
| `--csv-by-1recv-log-path` | no | filesystem path | Creates the per-received-frame CSV used as W08 input. |
| `--state-log-path` | no | filesystem path | Creates the FSM transition CSV. |
| `--recovery-mode` | no | `fsm` or `timeout-only`; default `fsm` | Selects link recovery behavior. |
| `--crc32-test` | no | flag | Runs the RX CRC test without requiring the normal mandatory options. |

The usage string presents `--bind-ip` as mandatory, but the implementation defaults it to `0.0.0.0` and does not reject omission. W08 passes it explicitly to avoid ambiguity.

## RX CSV And Summary Outputs

| output | option / location | schema or contents | W08 use |
| --- | --- | --- | --- |
| per receive | `--csv-by-1recv-log-path` | 6 columns: `rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status` | Primary `runN.csv`; supports latency percentiles and sequence-gap/loss analysis. |
| one-second statistics | `--csv-in-1sec-log-path` | 11 columns: `elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt,pps,cpu_pct` | Auxiliary time-series diagnostics. |
| state transition | `--state-log-path` | 7 columns: `link_name,trial,mono_ns,elapsed_ms,from_state,to_state,reason` | Optional; not required for a no-fault W08 baseline. |
| text log | `--log-path` | Configuration, per-second statistics when no statistics CSV is requested, final summary, and `trial_summary` | Records P50/P95/P99/max and receive/error totals. |

The per-receive CSV contains `missing_delta`, but it does not contain the TX sent total. A loss-rate calculation should retain the TX summary or use the fixed expected frame count from validated run metadata as its denominator.

W08 run validation must compare each complete ordered header against these schemas and also confirm its field count. This follows the W07 analyzer's validation method; checking only that a CSV has 6 or 11 comma-separated fields would not detect renamed or reordered columns.

## Existing Controls Versus Required Work

| W08 requirement | current status | decision |
| --- | --- | --- |
| Send interval | Implemented by TX `--rate-hz`. | No C change required; the after run changes only this option. |
| Payload length | Implemented by TX `--payload-len`. | Keep fixed across baseline and all after runs. |
| Duration | Implemented by TX/RX `--duration-sec`. | Keep fixed across comparisons. |
| Run log path | Implemented by TX/RX `--log-path`. | Use unique paths because logs append. |
| Per-receive latency CSV | Implemented by RX `--csv-by-1recv-log-path`. | Use as the official W08 run CSV. |
| One-second CSV | Implemented by RX `--csv-in-1sec-log-path`. | Retain as auxiliary evidence. |
| Socket send/receive buffer | Not implemented. No `setsockopt(SO_SNDBUF/SO_RCVBUF)` or matching `getsockopt()` exists in TX/RX. | Issue #127 must add `--sndbuf` and/or `--rcvbuf`, validate the requested value, fail visibly on `setsockopt()` error, and log the effective value returned by `getsockopt()`. |
| CPU affinity | Not implemented in TX/RX. | Do not add affinity logic to the C programs. Issue #128 should use a `taskset` execution wrapper and record the selected CPU core and full command. |

## W08 Implementation Boundary

- Issue #125 owns the common baseline values and invariant conditions.
- Issue #127 owns socket-buffer CLI and effective-value logging.
- Issue #128 owns the `taskset` wrapper.
- Later measurement issues own real Raspberry Pi 5 runs and CSV capture.

This inventory changes no runtime behavior.
