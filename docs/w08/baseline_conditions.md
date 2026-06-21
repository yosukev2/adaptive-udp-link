# W08 Common Baseline Conditions

## Scope

W08 measures the existing Linux UDP `tx` and `rx` programs on Raspberry Pi 5 Linux. Both processes run on the same Raspberry Pi 5 and communicate through host loopback. Raspberry Pi Pico and its firmware are not part of this experiment and must not be changed.

The common baseline is reused as the `before` condition for the send-interval, socket-buffer, and CPU-affinity comparisons. Each `after` run changes exactly one candidate factor.

## Baseline Condition

| category | fixed baseline value | verification or note |
| --- | --- | --- |
| target host | Raspberry Pi 5 Linux, same host for `tx` and `rx` | Record `uname -a` and the repository commit in `run_metadata.md`. |
| Pico firmware | Not used and not changed | Do not flash, rebuild, or reconnect Pico as part of W08. |
| network path | Host loopback; neither wired nor wireless | Physical Ethernet and Wi-Fi are outside this baseline. |
| Linux interface | `lo` | Confirm with `ip -brief address show lo`. |
| bind / destination IP | `127.0.0.1` / `127.0.0.1` | Keeps both timestamps in the same `CLOCK_MONOTONIC` domain. |
| UDP port | `9000` | Same for `rx --port` and `tx --dst-port`. |
| protocol version | Frame v1 (`--version 1`) | `tx` currently accepts only version 1. |
| payload length | `48` bytes per frame | Pass `--payload-len 48`; one datagram contains 3 frames. |
| send rate | `100` frames/s | Pass `--rate-hz 100`; this is a frame rate, not a datagram rate. |
| TX duration | `60` seconds | Pass `tx --duration-sec 60`. |
| RX duration | `62` seconds | Start `rx` first, wait 1 second, run `tx` for 60 seconds, and retain a 1-second receive tail. |
| fault injection | Disabled | Omit `--fault-target`, `--fault-rate`, `--outage-at-sec`, and `--outage-duration-ms`. |
| recovery mode | `fsm` | Pass `rx --recovery-mode fsm`; no outage is injected. |
| socket buffers | Linux defaults; no `setsockopt()` override | Record `net.core.wmem_default` and `net.core.rmem_default` before the runs. |
| CPU affinity | Unrestricted | Do not invoke `taskset` for the baseline. |
| background load | No intentionally started load generator | Record unexpected heavy processes or invalidate the run. |
| trials | 3 valid runs | Use trial numbers 1, 2, and 3. |
| official latency CSV | `data/w08/baseline/runN.csv` | Use `rx --csv-by-1recv-log-path`; `N` is the trial number. |
| auxiliary output | `data/w08/baseline/runN_rx.log`, `runN_tx.log`, `runN_1sec.csv` | Use a distinct path per run because text logs are opened in append mode. |
| run metadata | `data/w08/baseline/run_metadata.md` | Record commands, start time, commit, kernel, buffer defaults, and validity. |

Metadata fields such as condition name, trial number, output path, and execution timestamp may differ between runs. They are not experimental factors.

## Fixed Items In Every After Condition

| after condition | only allowed change | all other baseline items |
| --- | --- | --- |
| send interval | `--rate-hz` | Fixed, including loopback path, payload, durations, socket defaults, and unrestricted affinity. |
| socket buffer | `--sndbuf` and/or `--rcvbuf` introduced by Issue #127 | Fixed, including `--rate-hz 100` and unrestricted affinity. Record requested and effective buffer sizes. |
| CPU affinity | `taskset` CPU selection introduced by Issue #128 | Fixed, including `--rate-hz 100` and default socket buffers. |

Do not combine after conditions. In particular, a socket-buffer run must not also use `taskset`, and an affinity run must not override socket buffers.

## Command Template

Run from the repository root on Raspberry Pi 5 after building `bin/tx` and `bin/rx`. Replace `N` with `1`, `2`, or `3`.

```bash
mkdir -p data/w08/baseline

./bin/rx \
  --bind-ip 127.0.0.1 \
  --port 9000 \
  --duration-sec 62 \
  --log-path data/w08/baseline/runN_rx.log \
  --link-name w08_baseline \
  --trial N \
  --csv-in-1sec-log-path data/w08/baseline/runN_1sec.csv \
  --csv-by-1recv-log-path data/w08/baseline/runN.csv \
  --recovery-mode fsm &
rx_pid=$!

sleep 1

./bin/tx \
  --dst-ip 127.0.0.1 \
  --dst-port 9000 \
  --rate-hz 100 \
  --duration-sec 60 \
  --log-path data/w08/baseline/runN_tx.log \
  --payload-len 48 \
  --version 1

wait "$rx_pid"
```

Before the first run, record the host state without changing it:

```bash
date --iso-8601=seconds
uname -a
git rev-parse HEAD
ip -brief address show lo
sysctl net.core.wmem_default net.core.rmem_default
```

## Run Validity

A run is valid only when both processes exit normally, the per-receive CSV has its expected header, the TX and RX summaries are present, and the metadata records no unintended condition change. Record the reason and repeat the same trial number when a run is invalid; do not mix an invalid run into the three-run comparison.
