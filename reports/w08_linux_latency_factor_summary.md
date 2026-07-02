# W08 Linux latency factor summary

## 目的

send interval / socket buffer size / CPU affinity の3候補について、既存サマリ結果を使って P95 / P99 / loss_rate を同じ表で比較する。

## 比較方針

- send interval は W08 baseline `rate_hz=100` と、10,000Hzより大きくmissingが出ていない代表点 `rate_hz=120000` を比較する。
- socket buffer と CPU affinity は `rate_hz=10000` を基準に、同じrate内で before/after を比較する。
- loss_rate は 1recv CSV の `missing_delta_total / (observed + missing)` または各aggregate CSVの `missing_rate_avg` を使う。
- 本表は既存の #129〜#132 サマリを横断した比較であり、新規実機計測は追加しない。

## 3候補比較

| factor | before | after | before_p95_ms | after_p95_ms | before_p99_ms | after_p99_ms | p99_change_pct | before_loss_rate | after_loss_rate | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| send interval | baseline rate_hz=100 | rate_hz=120000 | 0.019583 | 0.008185 | 0.036339 | 0.011852 | -67.39% | 0.00000000 | 0.00000000 | 10,000Hzより大きく、missing=0の代表点として120,000Hzを採用。p99は大きく悪化せず、Pi5ではこのrate帯まで処理余裕がある。 |
| socket buffer | rate_hz=10000 socket default | rate_hz=10000 rcvbuf_requested=5000 actual=10000 | 0.014197 | 0.014229 | 0.014994 | 0.015025 | 0.21% | 0.00000000 | 0.00000000 | 10,000Hzではbuffer変更によるp99改善は小さく、有意な支配因子とは言いにくい。 |
| CPU affinity | rate_hz=10000 rx_pin=off tx_pin=off | rate_hz=10000 rx_pin=on tx_pin=on | 0.014210 | 0.010550 | 0.014889 | 0.010821 | -27.32% | 0.00000000 | 0.00000000 | 10,000HzではRX/TX固定でp99が改善。ただし末尾edgeは残るため、通常時latencyとedge要因は分けて扱う。 |

## 判定

- 120,000Hzまでは missing/loss が出ておらず、Raspberry Pi 5 ではこのrate帯に処理余裕がある。
- socket buffer size は 10,000Hz では p99/loss に大きな差が出ず、支配因子とは言いにくい。
- CPU affinity は 10,000Hz の通常時 p99 を改善するが、末尾edge latencyは残る。
- send interval は少なくとも120,000Hzまでは破綻していないため、10,000Hz近辺では主要な悪化要因ではない。

## 参照元

- `data/w08/baseline/run1.csv`〜`run3.csv`
- `data/w08/send_interval/w08_send_interval_summary.csv`
- `reports/w08_socket_buffer_rate_rcvbuf_aggregate.csv`
- `reports/w08_cpu_affinity_matrix_aggregate.csv`
- `reports/w08_send_interval_summary.md`
- `reports/w08_socket_buffer_highrate_summary.md`
- `reports/w08_cpu_affinity_matrix_summary.md`
