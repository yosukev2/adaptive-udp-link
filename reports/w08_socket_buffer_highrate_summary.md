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

- 結果：
低rateの 5,000/10,000Hz では、missingなし条件の p99 latency はおおむね 0.015〜0.017 ms に収まり、SO_RCVBUF の大小による差は小さい。
示唆：
今回の payload_len=48 かつ受信処理が軽い条件では、受信キュー滞留が latency を支配しているとは言いにくく、p99 の差はスケジューリング揺らぎ・測定ノイズの影響が大きい可能性が高い。

- 結果：
TX/RX明示条件では、送信バッファが大きく受信バッファが小さい条件で missing が増える例がある。例として rate=180,000Hz、rcvbuf=8,000/16,000、sndbuf=16,000/32,000 では missing_avg=7,178。
示唆：
送信側が一時的に多く吐ける一方で受信側の受け皿が小さいと、RXが瞬間的に遅れたときにsocket queueを吸収しきれず、sequence gap が発生しやすい。

- 結果：
追加の rate×SO_RCVBUF 実験では、50,000Hzで rcvbuf=5,000/10,000 の missing_avg=1,819 に対し、rcvbuf=50,000/100,000 では missing_avg=0 まで低下した。
示唆：
受信バッファを十分大きくすると、短時間のRX遅れをdropではなくqueueで吸収できるため、missingは抑制される。ただし全条件で単調減少ではないため、buffer sizeだけを支配要因とは見なさない。

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

### 実験データ

- total runs: 60
- run_validity=ok: 60
- invalid runs: 0
- rate_hz: `50000 / 25000 / 10000 / 5000`
- SO_RCVBUF requested: `1000 / 5000 / 10000 / 50000 / 100000`
- SO_SNDBUF: default
- fixed: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none

### 結論・観察

- missing 最大は `rate_hz=50000, rcvbuf=5000/10000` の `missing_avg=1819`。
- p99 latency 最大は `rate_hz=50000, rcvbuf=5000/10000` の `p99=0.029469 ms`。
- この中低rate帯でも `SO_RCVBUF` と missing / latency は単調な関係ではない。
- `requested=1000` は actual `2304` に丸められる。requested値そのものではなく actual も併記して比較する。

### missing 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | runs | missing_avg | p99_ms_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 50000 | 5000 | 10000 | 3 | 1819.00 | 0.029469 | 109.666652 |
| 25000 | 10000 | 20000 | 3 | 288.00 | 0.016445 | 13.978613 |
| 50000 | 10000 | 20000 | 3 | 196.00 | 0.012420 | 4.286901 |
| 50000 | 1000 | 2304 | 3 | 118.00 | 0.013290 | 1.127418 |
| 25000 | 1000 | 2304 | 3 | 103.00 | 0.014666 | 3.142859 |
| 25000 | 5000 | 10000 | 3 | 65.00 | 0.015228 | 2.768866 |
| 10000 | 1000 | 2304 | 3 | 50.00 | 0.015136 | 3.686290 |
| 50000 | 100000 | 200000 | 3 | 47.00 | 0.013747 | 7.732463 |
| 5000 | 1000 | 2304 | 3 | 3.00 | 0.018537 | 1.510794 |
| 5000 | 5000 | 10000 | 3 | 0.00 | 0.016197 | 0.167370 |

### p99 latency 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | runs | p99_ms_avg | missing_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 50000 | 5000 | 10000 | 3 | 0.029469 | 1819.00 | 109.666652 |
| 5000 | 1000 | 2304 | 3 | 0.018537 | 3.00 | 1.510794 |
| 10000 | 50000 | 100000 | 3 | 0.016882 | 0.00 | 0.794474 |
| 10000 | 100000 | 200000 | 3 | 0.016654 | 0.00 | 1.336393 |
| 25000 | 10000 | 20000 | 3 | 0.016445 | 288.00 | 13.978613 |
| 10000 | 10000 | 20000 | 3 | 0.016408 | 0.00 | 1.140980 |
| 5000 | 5000 | 10000 | 3 | 0.016197 | 0.00 | 0.167370 |
| 5000 | 100000 | 200000 | 3 | 0.016099 | 0.00 | 1.605101 |
| 5000 | 50000 | 100000 | 3 | 0.015932 | 0.00 | 0.166500 |
| 5000 | 10000 | 20000 | 3 | 0.015913 | 0.00 | 1.437775 |

### max latency 上位

| rate_hz | rcvbuf_req | rcvbuf_actual | runs | max_ms_avg | p99_ms_avg | missing_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 50000 | 5000 | 10000 | 3 | 109.666652 | 0.029469 | 1819.00 |
| 25000 | 10000 | 20000 | 3 | 13.978613 | 0.016445 | 288.00 |
| 50000 | 100000 | 200000 | 3 | 7.732463 | 0.013747 | 47.00 |
| 50000 | 10000 | 20000 | 3 | 4.286901 | 0.012420 | 196.00 |
| 10000 | 1000 | 2304 | 3 | 3.686290 | 0.015136 | 50.00 |
| 50000 | 50000 | 100000 | 3 | 3.640297 | 0.013963 | 0.00 |
| 25000 | 1000 | 2304 | 3 | 3.142859 | 0.014666 | 103.00 |
| 25000 | 5000 | 10000 | 3 | 2.768866 | 0.015228 | 65.00 |
| 5000 | 100000 | 200000 | 3 | 1.605101 | 0.016099 | 0.00 |
| 5000 | 1000 | 2304 | 3 | 1.510794 | 0.018537 | 3.00 |

### Heatmaps

![w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg](figures/w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg.png)

![w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg](figures/w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg.png)

![w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg](figures/w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg.png)

## 成果物

- run summary: `reports/w08_socket_buffer_highrate_run_summary.csv`
- default SO_SNDBUF aggregate: `reports/w08_socket_buffer_highrate_default_sndbuf_aggregate.csv`
- explicit TX/RX aggregate: `reports/w08_socket_buffer_highrate_txrx_aggregate.csv`
- report: `reports/w08_socket_buffer_highrate_summary.md`
- rate/rcvbuf追加run summary: `reports/w08_socket_buffer_rate_rcvbuf_run_summary.csv`
- rate/rcvbuf追加aggregate: `reports/w08_socket_buffer_rate_rcvbuf_aggregate.csv`
