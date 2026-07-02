# W08 #131 rate_hz x SO_RCVBUF matrix summary

## 目的

- 送信bufferは default のまま、`rate_hz` と受信 `SO_RCVBUF` の組み合わせで missing / latency がどう変わるかを見る。
- highrate sweep で大きな missing が出たため、`50,000` 以下の中低rate帯を細かく確認する。

## 実験データ

- total runs: 60
- run_validity=ok: 60
- invalid runs: 0
- rate_hz: `50000 / 25000 / 10000 / 5000`
- SO_RCVBUF requested: `1000 / 5000 / 10000 / 50000 / 100000`
- SO_SNDBUF: default
- fixed: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none

## 結論・観察

- missing 最大は `rate_hz=50000, rcvbuf=5000/10000` の `missing_avg=1819`。
- p99 latency 最大は `rate_hz=50000, rcvbuf=5000/10000` の `p99=0.029469 ms`。
- この中低rate帯でも `SO_RCVBUF` と missing / latency は単調な関係ではない。
- `requested=1000` は actual `2304` に丸められる。requested値そのものではなく actual も併記して比較する。

## missing 上位

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

## p99 latency 上位

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

## max latency 上位

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

## Heatmaps

![w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg](figures/w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg.png)

![w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg](figures/w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg.png)

![w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg](figures/w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg.png)

## 成果物

- run summary: `reports/w08_socket_buffer_rate_rcvbuf_run_summary.csv`
- aggregate summary: `reports/w08_socket_buffer_rate_rcvbuf_aggregate.csv`
- report: `reports/w08_socket_buffer_rate_rcvbuf_summary.md`