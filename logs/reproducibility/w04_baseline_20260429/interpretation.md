# Reproducibility Result

- Run date: 2026-04-29T09:00:12+09:00
- Link name: host_loopback
- Trials: 3
- Rate: 120 frame/s
- Duration: 5s tx / 7s rx
- Payload length: 64 bytes
- Mean P99: 0.360 ms
- Max deviation from mean: 6.94%
- Criterion: reproducible when every trial stays within +/-15.00% of mean P99
- Result: yes

P99 deviation stayed within +/-15.00% of the three-run mean. The stable avg_pps and low cpu_pct spread suggest scheduler jitter stayed bounded in this host-loopback setup.
