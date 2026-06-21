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
N=1

rm -f \
  "data/w08/baseline/run${N}.csv" \
  "data/w08/baseline/run${N}_1sec.csv" \
  "data/w08/baseline/run${N}_rx.log" \
  "data/w08/baseline/run${N}_tx.log"

./bin/rx \
  --bind-ip 127.0.0.1 \
  --port 9000 \
  --duration-sec 62 \
  --log-path "data/w08/baseline/run${N}_rx.log" \
  --link-name w08_baseline \
  --trial "${N}" \
  --csv-in-1sec-log-path "data/w08/baseline/run${N}_1sec.csv" \
  --csv-by-1recv-log-path "data/w08/baseline/run${N}.csv" \
  --recovery-mode fsm &
rx_pid=$!

sleep 1

./bin/tx \
  --dst-ip 127.0.0.1 \
  --dst-port 9000 \
  --rate-hz 100 \
  --duration-sec 60 \
  --log-path "data/w08/baseline/run${N}_tx.log" \
  --payload-len 48 \
  --version 1
tx_status=$?

wait "$rx_pid"
rx_status=$?

printf 'trial=%s tx_status=%s rx_status=%s\n' \
  "$N" "$tx_status" "$rx_status"
```

Set `N` to `1`, `2`, and `3` in turn. Removing the four paths before a run is required because the text logs are append-only and an invalid retry must not retain stale output.

Before the first run, record the host state without changing it:

```bash
date --iso-8601=seconds
uname -a
git rev-parse HEAD
ip -brief address show lo
sysctl net.core.wmem_default net.core.rmem_default
```

## Run Validity

A run is valid only when every item below passes.

- `tx_status=0` and `rx_status=0` are recorded after waiting for both processes. A timeout exit such as the W07 USB capture status `124` is not expected or accepted for these Linux processes.
- `runN.csv` has the exact 6-column header `rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status` and at least one data row.
- `runN_1sec.csv` has the exact 11-column header `elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt,pps,cpu_pct` and at least one data row.
- Header validation compares the complete ordered field list, as in the W07 analyzer. Matching only the field count is insufficient.
- `runN_tx.log` contains `tx summary` and `tx end`; `runN_rx.log` contains `rx summary`, `rx end`, and exactly one `trial_summary link_name=w08_baseline trial=N` for the selected `N`.
- Neither process log contains an `ERROR` entry.
- The selected trial number `N`, the `--trial N` argument, `trial=N` in the RX summary, and all four `runN*` output paths agree. Output from another trial or an earlier retry is not accepted.
- The metadata records the exact commands, both exit codes, start time, commit, kernel, socket-buffer defaults, and whether unexpected background load was observed.
- No experimental condition other than the one assigned to the relevant `after` run differs from this baseline.

The following commands perform the schema and log checks after each run. They intentionally test both the exact header text and the resulting number of fields.

```bash
test "$tx_status" -eq 0
test "$rx_status" -eq 0

test "$(head -n 1 "data/w08/baseline/run${N}.csv")" = \
  'rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status'
test "$(awk -F, 'NR==1{print NF}' "data/w08/baseline/run${N}.csv")" -eq 6
test "$(wc -l < "data/w08/baseline/run${N}.csv")" -gt 1

test "$(head -n 1 "data/w08/baseline/run${N}_1sec.csv")" = \
  'elapsed_sec,avg_latency_ms,max_latency_ms,min_latency_ms,recv_cnt,ok_recv_cnt,gap_cnt,dup_cnt,reord_cnt,pps,cpu_pct'
test "$(awk -F, 'NR==1{print NF}' "data/w08/baseline/run${N}_1sec.csv")" -eq 11
test "$(wc -l < "data/w08/baseline/run${N}_1sec.csv")" -gt 1

grep -q 'tx summary' "data/w08/baseline/run${N}_tx.log"
grep -q 'tx end' "data/w08/baseline/run${N}_tx.log"
grep -q 'rx summary' "data/w08/baseline/run${N}_rx.log"
grep -q 'rx end' "data/w08/baseline/run${N}_rx.log"
test "$(grep -c "trial_summary link_name=w08_baseline trial=${N} " \
  "data/w08/baseline/run${N}_rx.log")" -eq 1
! grep -q 'ERROR' "data/w08/baseline/run${N}_tx.log"
! grep -q 'ERROR' "data/w08/baseline/run${N}_rx.log"
```

## Excluded Conditions

The W08 baseline and every one-factor comparison use only Raspberry Pi 5 host loopback. Wi-Fi, physical Ethernet, another host, and any other network namespace or virtual network path are excluded. Raspberry Pi Pico, Pico firmware, USB CDC capture, and W07 bare-metal/FreeRTOS measurements are also outside the W08 comparison target.

If any excluded path or device is used, mark the run invalid rather than interpreting it as a W08 result. Record the reason and repeat the same trial number. Invalid runs are never included in the three-run comparison.
