# W06 Jitter Summary

- Dataset kind: `measured`
- Input CSV: `data/w06/jitter_comparison.csv`
- Metric basis: `abs(jitter_us)`
- Percentiles: nearest-rank
- Stddev: population standard deviation
- Caution: This report reflects the measured CSV supplied to this script.

## Comparison Table

| env | board | samples | P50 abs jitter (us) | P95 abs jitter (us) | P99 abs jitter (us) | max abs jitter (us) | stddev abs jitter (us) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| linux_rpi5 | raspberry_pi_5 | 1000 | 0.00 | 3.00 | 5.00 | 55.00 | 1.97 |
| pico | raspberry_pi_pico | 1000 | 0.00 | 0.00 | 0.00 | 2.00 | 0.06 |

## P99 Difference

`linux_rpi5` P99 abs jitter is 5.00 us and `pico` P99 abs jitter is 0.00 us, so the difference (`linux_rpi5 - pico`) is 5.00 us.

## Final Interpretation

In this W06 dataset, the Raspberry Pi 5 Linux 10ms loop has P99 abs jitter 5.00 us, while the Raspberry Pi Pico hardware-timer loop has P99 abs jitter 0.00 us. The measured P99 difference is 5.00 us.

For UDP latency measurement, sender-side period jitter can be mixed into the observed timing as measurement noise. The Pico result in this dataset suggests that a hardware-timer sender can reduce that sender-side timing noise compared with the Linux user-space loop used here.

## Experimental Conditions

- Linux side: Raspberry Pi 5 Linux user-space logger
- MCU side: Raspberry Pi Pico firmware using a hardware timer path
- Target period: 10000 us
- Samples: 1000 rows per environment
- Jitter definition: `jitter_us = delta_us - period_target_us`
- Statistic basis: `abs(jitter_us)`
- Percentiles: nearest-rank
- Stddev: population standard deviation

## Constraints And Untested Items

- This is a timing-jitter comparison for the W06 logger paths, not a direct UDP latency benchmark.
- The timestamps are monotonic within each device and are not compared as shared absolute time.
- The result does not prove behavior across other kernels, system load profiles, Pico firmware variants, or network paths.
- The Pico result depends on keeping serial/USB output outside the timer callback or interrupt path.

## W06 Claims

- Supported: Under the recorded W06 conditions, Pico hardware-timer periodic execution had lower P99 abs jitter than the Raspberry Pi 5 Linux user-space loop.
- Supported: Sender-side period jitter is a plausible source of noise in UDP latency measurements, so reducing sender jitter can make later latency measurements cleaner.
- Not supported: W06 does not claim that Pico has lower UDP latency than Linux.
- Not supported: W06 does not claim that all Linux or all MCU implementations behave like these two measured paths.

## Evidence Package

- Bringup log: `docs/w06_bringup_log.md`
- Board selection and scope: `docs/board_selection.md`
- Measurement specification: `docs/w06_measurement_spec.md`
- Linux logger source: `experiments/w06_jitter/linux_jitter.c`
- Linux run log: `docs/w06_run_log.md`
- Linux raw CSV: `data/w06/linux_jitter_raw.csv`
- Pico firmware source: `firmware/w06_pico_jitter/main.c`
- Pico run log: `docs/w06_pico_jitter_run_log.md`
- Pico raw CSV: `data/w06/pico_jitter_raw.csv`
- Merge script: `scripts/merge_jitter_csv.py`
- Analysis script: `scripts/analyze_jitter.py`
- Merged comparison CSV: `data/w06/jitter_comparison.csv`
- Final summary: `reports/w06_jitter_summary.md`
