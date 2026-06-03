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
