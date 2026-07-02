# W08 #131 highrate socket buffer summary

## 目的

- 送信側 default のまま `SO_RCVBUF × rate_hz` を見る。
- 送信側 `SO_SNDBUF` も明示した条件で `SO_RCVBUF × SO_SNDBUF` を見る。

## 実験データ

- total runs: 216
- run_validity=ok: 216
- invalid runs: 0
- default SO_SNDBUF runs: 108
- explicit SO_SNDBUF runs: 108
- fixed: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none

## 結論・観察

- 送信buffer default 条件では、missing 最大は `rate_hz=1000000, rcvbuf=16000/32000` の `missing_avg=176153`。
- 送信buffer default 条件の p99 latency 最大は `rate_hz=200000, rcvbuf=100000/200000` の `p99=0.382719 ms`。
- TX/RX 明示条件では、missing 最大は `rate_hz=140000, rcvbuf=8000/16000, sndbuf=10000/20000` の `missing_avg=19202`。
- TX/RX 明示条件の p99 latency 最大は `rate_hz=180000, rcvbuf=12000/24000, sndbuf=12000/24000` の `p99=0.133118 ms`。
- missing と p99 latency は同じ条件で最大化していない。gap 発生量と通常受信時の tail latency は分けて見る必要がある。
- `SO_RCVBUF` を大きくすれば常に改善する、または小さくすれば常に悪化する、という単調な傾向はこの highrate 結果からは言えない。
- `rate_hz=500000` 以上では missing が大きく出る条件が増え、buffer size よりも処理飽和・スケジューリング・送受信処理の競合が支配的になっている可能性が高い。

## 主要な見方

- `missing_delta_total_avg` は3試行平均。値が大きいほど受信側で sequence gap が多い。
- `p99_latency_ms_avg` は各試行の p99 latency を平均した値。
- `max_latency_ms_avg` は外れ値を見るための補助指標。
- heatmap の buffer ラベルは `requested/actual`。`default` は送信側 buffer を明示指定していない条件。

## 送信buffer default: missing 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | runs | missing_avg | p99_ms_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 1000000 | 16000 | 32000 | 3 | 176153.00 | 0.010488 | 318.591505 |
| 1000000 | 4000 | 8000 | 3 | 99113.00 | 0.010352 | 175.116230 |
| 500000 | 4000 | 8000 | 3 | 72458.00 | 0.010414 | 122.740102 |
| 500000 | 100000 | 200000 | 3 | 57713.00 | 0.011518 | 208.062039 |
| 200000 | 2000 | 4000 | 3 | 44079.00 | 0.074896 | 101.490047 |
| 500000 | 2000 | 4000 | 3 | 37306.00 | 0.018370 | 56.700569 |
| 1000000 | 2000 | 4000 | 3 | 35527.00 | 0.010642 | 45.128117 |
| 1000000 | 32000 | 64000 | 3 | 28650.00 | 0.011074 | 192.838060 |
| 1000000 | 100000 | 200000 | 3 | 27093.00 | 0.026346 | 51.350403 |
| 200000 | 8000 | 16000 | 3 | 26169.00 | 0.240552 | 2.962479 |

## 送信buffer default: p99 latency 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | runs | p99_ms_avg | missing_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 200000 | 100000 | 200000 | 3 | 0.382719 | 5966.00 | 116.241782 |
| 200000 | 32000 | 64000 | 3 | 0.338607 | 1094.00 | 2.831338 |
| 200000 | 16000 | 32000 | 3 | 0.262909 | 17641.00 | 79.873847 |
| 200000 | 8000 | 16000 | 3 | 0.240552 | 26169.00 | 2.962479 |
| 200000 | 4000 | 8000 | 3 | 0.089630 | 24037.00 | 21.342164 |
| 200000 | 2000 | 4000 | 3 | 0.074896 | 44079.00 | 101.490047 |
| 180000 | 4000 | 8000 | 3 | 0.067981 | 1770.00 | 3.245913 |
| 180000 | 16000 | 32000 | 3 | 0.053587 | 1260.00 | 6.799683 |
| 180000 | 100000 | 200000 | 3 | 0.051741 | 4601.00 | 28.534190 |
| 180000 | 32000 | 64000 | 3 | 0.039920 | 16261.00 | 120.624300 |

## TX/RX明示: missing 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | sndbuf_req | sndbuf_actual | runs | missing_avg | p99_ms_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 140000 | 8000 | 16000 | 10000 | 20000 | 3 | 19202.00 | 0.009512 | 419.262430 |
| 180000 | 12000 | 24000 | 8000 | 16000 | 3 | 13956.00 | 0.055920 | 76.357018 |
| 180000 | 16000 | 32000 | 2000 | 4608 | 3 | 13829.00 | 0.034037 | 75.580208 |
| 180000 | 16000 | 32000 | 8000 | 16000 | 3 | 12264.00 | 0.015623 | 67.259259 |
| 140000 | 12000 | 24000 | 4000 | 8000 | 3 | 11860.00 | 0.010671 | 85.368322 |
| 140000 | 12000 | 24000 | 16000 | 32000 | 3 | 9836.00 | 0.009037 | 84.460033 |
| 140000 | 16000 | 32000 | 8000 | 16000 | 3 | 8793.00 | 0.032129 | 71.207085 |
| 140000 | 16000 | 32000 | 2000 | 4608 | 3 | 8483.00 | 0.011074 | 65.661138 |
| 140000 | 16000 | 32000 | 4000 | 8000 | 3 | 8279.00 | 0.026277 | 138.748540 |
| 140000 | 12000 | 24000 | 12000 | 24000 | 3 | 8069.00 | 0.015049 | 156.766345 |

## TX/RX明示: p99 latency 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | sndbuf_req | sndbuf_actual | runs | p99_ms_avg | missing_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 180000 | 12000 | 24000 | 12000 | 24000 | 3 | 0.133118 | 1986.00 | 8.277704 |
| 180000 | 12000 | 24000 | 4000 | 8000 | 3 | 0.073066 | 1701.00 | 7.434964 |
| 180000 | 8000 | 16000 | 16000 | 32000 | 3 | 0.065067 | 7178.00 | 38.664924 |
| 180000 | 12000 | 24000 | 10000 | 20000 | 3 | 0.063889 | 1586.00 | 6.663831 |
| 180000 | 12000 | 24000 | 8000 | 16000 | 3 | 0.055920 | 13956.00 | 76.357018 |
| 180000 | 16000 | 32000 | 16000 | 32000 | 3 | 0.053329 | 588.00 | 10.852612 |
| 180000 | 12000 | 24000 | 2000 | 4608 | 3 | 0.052019 | 2257.00 | 10.193853 |
| 180000 | 16000 | 32000 | 4000 | 8000 | 3 | 0.051895 | 297.00 | 2.650877 |
| 180000 | 8000 | 16000 | 8000 | 16000 | 3 | 0.049784 | 797.00 | 113.165105 |
| 180000 | 12000 | 24000 | 16000 | 32000 | 3 | 0.045630 | 2813.00 | 13.698420 |

## Heatmaps

![w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_missing_delta_total_avg](figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_missing_delta_total_avg.png)

![w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_p99_latency_ms_avg](figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_p99_latency_ms_avg.png)

![w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_max_latency_ms_avg](figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_max_latency_ms_avg.png)

![w08_socket_buffer_highrate_txrx_rate_140000_missing_delta_total_avg](figures/w08_socket_buffer_highrate_txrx_rate_140000_missing_delta_total_avg.png)

![w08_socket_buffer_highrate_txrx_rate_140000_p99_latency_ms_avg](figures/w08_socket_buffer_highrate_txrx_rate_140000_p99_latency_ms_avg.png)

![w08_socket_buffer_highrate_txrx_rate_140000_max_latency_ms_avg](figures/w08_socket_buffer_highrate_txrx_rate_140000_max_latency_ms_avg.png)

![w08_socket_buffer_highrate_txrx_rate_180000_missing_delta_total_avg](figures/w08_socket_buffer_highrate_txrx_rate_180000_missing_delta_total_avg.png)

![w08_socket_buffer_highrate_txrx_rate_180000_p99_latency_ms_avg](figures/w08_socket_buffer_highrate_txrx_rate_180000_p99_latency_ms_avg.png)

![w08_socket_buffer_highrate_txrx_rate_180000_max_latency_ms_avg](figures/w08_socket_buffer_highrate_txrx_rate_180000_max_latency_ms_avg.png)

## 追加: rate_hz x SO_RCVBUF matrix

送信bufferは default のまま、`rate_hz=50000 / 25000 / 10000 / 5000` と `SO_RCVBUF requested=1000 / 5000 / 10000 / 50000 / 100000` の matrix を追加した。詳細は `reports/w08_socket_buffer_rate_rcvbuf_summary.md` を参照。

- total runs: 60
- run_validity=ok: 60
- missing 最大: `rate_hz=50000, rcvbuf=5000/10000`, `missing_avg=1819`
- p99 latency 最大: `rate_hz=50000, rcvbuf=5000/10000`, `p99=0.029469 ms`
- この中低rate帯でも `SO_RCVBUF` と missing / latency は単調な関係ではない。

![w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg](figures/w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg.png)

![w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg](figures/w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg.png)

![w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg](figures/w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg.png)

## 成果物

- run summary: `reports/w08_socket_buffer_highrate_run_summary.csv`
- default SO_SNDBUF aggregate: `reports/w08_socket_buffer_highrate_default_sndbuf_aggregate.csv`
- explicit TX/RX aggregate: `reports/w08_socket_buffer_highrate_txrx_aggregate.csv`
- report: `reports/w08_socket_buffer_highrate_summary.md`
- rate/rcvbuf追加report: `reports/w08_socket_buffer_rate_rcvbuf_summary.md`
- rate/rcvbuf追加aggregate: `reports/w08_socket_buffer_rate_rcvbuf_aggregate.csv`
