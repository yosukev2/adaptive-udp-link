# W06 Jitter Summary

- Dataset kind: `sample`
- Input CSV: `data/w06/jitter_comparison.csv`
- Metric basis: `abs(jitter_us)`
- Percentiles: nearest-rank
- Stddev: population standard deviation
- Caution: This report is generated from sample CSV only. Replace the sample raw CSVs with measured `linux_jitter_raw.csv` / `pico_jitter_raw.csv` before treating the values as experimental results.

## Comparison Table

| env | board | samples | P50 abs jitter (us) | P95 abs jitter (us) | P99 abs jitter (us) | max abs jitter (us) | stddev abs jitter (us) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| linux_rpi5 | raspberry_pi_5 | 20 | 15.00 | 55.00 | 60.00 | 60.00 | 16.18 |
| pico | raspberry_pi_pico | 20 | 2.00 | 4.00 | 5.00 | 5.00 | 1.16 |

## P99 Difference

`linux_rpi5` P99 abs jitter is 60.00 us and `pico` P99 abs jitter is 5.00 us, so the difference (`linux_rpi5 - pico`) is 55.00 us.
