# W08 #132 CPU affinity matrix summary

## 目的

- RX/TX の CPU affinity 有無と `rate_hz` の組み合わせで missing / latency がどう変わるかを見る。
- #130 で見えた先頭・末尾の latency 跳ねを確認するため、各runの先頭3行・末尾3行を別集計する。

## 実験条件

- rx_pin: `off / on`
- tx_pin: `off / on`
- rate_hz: `5000 / 10000 / 50000 / 100000 / 500000`
- trials: `1 / 2 / 3`
- default pin core: RX core 0, TX core 1
- socket buffer tuning: none

## 結論・観察

- missing 最大は `rate_hz=500000, rx_pin=off, tx_pin=on` の `missing_avg=552052`。
- 末尾 edge latency の平均との差が最大なのは `rate_hz=10000, rx_pin=on, tx_pin=on` で、末尾平均 `0.981002 ms`、中央平均 `0.010126 ms`、差分 `0.970876 ms`。
- 先頭 edge latency の平均との差が最大なのは `rate_hz=5000, rx_pin=on, tx_pin=on` で、先頭平均 `0.079352 ms`、中央平均 `0.010298 ms`、差分 `0.069054 ms`。
- 500,000 Hz では全pin条件で missing が大きく、CPU affinity の有無だけでは飽和を吸収できていない。
- 5,000〜50,000 Hz では missing は基本的に 0 だが、末尾 edge latency は条件によって中央部より大きく跳ねる。#130で見えた末尾だけ遅い現象は、このmatrixでも再現している。
- RX/TX の pinning は一部条件で改善するが、全指標で単調に良くなるわけではない。missing、p99、末尾edgeは分けて判断する。

## 集計値の意味

- `first_edge_*`: CSV先頭側の latency。
- `last_edge_*`: CSV末尾側の latency。
- `*_minus_middle_mean_ms`: 先頭/末尾 edge の平均 latency から、edgeを除いた中央部分の平均 latency を引いた値。正なら edge が中央より遅い。

## missing 上位

| rate_hz | rx_pin | tx_pin | runs | missing_avg | p99_ms_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 500000 | off | on | 3 | 552052 | 0.010661 | 1178.802144 |
| 500000 | on | on | 3 | 172274 | 0.010494 | 628.338372 |
| 500000 | on | off | 3 | 138754 | 0.012352 | 656.492359 |
| 500000 | off | off | 3 | 113695 | 0.022778 | 150.131954 |
| 100000 | off | on | 3 | 3823 | 0.012210 | 384.964847 |
| 100000 | on | on | 3 | 799 | 0.008765 | 13.102234 |
| 100000 | on | off | 3 | 458 | 0.009518 | 9.299489 |
| 5000 | off | off | 3 | 0 | 0.017394 | 2.942339 |
| 5000 | off | on | 3 | 0 | 0.015840 | 0.130006 |
| 5000 | on | off | 3 | 0 | 0.012562 | 0.073679 |

## p99 latency 上位

| rate_hz | rx_pin | tx_pin | runs | p99_ms_avg | missing_avg | max_ms_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 500000 | off | off | 3 | 0.022778 | 113695 | 150.131954 |
| 5000 | off | off | 3 | 0.017394 | 0 | 2.942339 |
| 10000 | off | on | 3 | 0.016364 | 0 | 0.564983 |
| 5000 | off | on | 3 | 0.015840 | 0 | 0.130006 |
| 10000 | off | off | 3 | 0.014889 | 0 | 1.632065 |
| 50000 | off | on | 3 | 0.012870 | 0 | 2.665757 |
| 5000 | on | off | 3 | 0.012562 | 0 | 0.073679 |
| 500000 | on | off | 3 | 0.012352 | 138754 | 656.492359 |
| 10000 | on | off | 3 | 0.012309 | 0 | 0.237420 |
| 100000 | off | on | 3 | 0.012210 | 3823 | 384.964847 |

## 末尾 edge latency 上位

| rate_hz | rx_pin | tx_pin | last_mean_ms | middle_mean_ms | last_minus_middle_ms | missing_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 10000 | on | on | 0.981002 | 0.010126 | 0.970876 | 0 |
| 100000 | on | off | 0.856168 | 0.012883 | 0.843285 | 458 |
| 5000 | off | off | 0.639347 | 0.015227 | 0.624119 | 0 |
| 50000 | on | on | 0.624217 | 0.008237 | 0.615980 | 0 |
| 10000 | off | off | 0.279149 | 0.012745 | 0.266404 | 0 |
| 10000 | off | on | 0.156902 | 0.013324 | 0.143578 | 0 |
| 50000 | off | on | 0.150118 | 0.011043 | 0.139074 | 0 |
| 5000 | off | on | 0.130006 | 0.014085 | 0.115921 | 0 |
| 50000 | off | off | 0.085593 | 0.009577 | 0.076015 | 0 |
| 5000 | on | off | 0.048092 | 0.010595 | 0.037497 | 0 |

## 先頭 edge latency 上位

| rate_hz | rx_pin | tx_pin | first_mean_ms | middle_mean_ms | first_minus_middle_ms | missing_avg |
| --- | --- | --- | --- | --- | --- | --- |
| 5000 | on | on | 0.079352 | 0.010298 | 0.069054 | 0 |
| 10000 | on | off | 0.075685 | 0.011283 | 0.064402 | 0 |
| 50000 | on | off | 0.069241 | 0.008550 | 0.060690 | 0 |
| 10000 | on | on | 0.065667 | 0.010126 | 0.055541 | 0 |
| 10000 | off | on | 0.067593 | 0.013324 | 0.054269 | 0 |
| 5000 | on | off | 0.060951 | 0.010595 | 0.050356 | 0 |
| 10000 | off | off | 0.063043 | 0.012745 | 0.050298 | 0 |
| 5000 | off | off | 0.062877 | 0.015227 | 0.047649 | 0 |
| 100000 | on | off | 0.059618 | 0.012883 | 0.046735 | 458 |
| 50000 | off | off | 0.054111 | 0.009577 | 0.044534 | 0 |

## Heatmaps

### TX非固定: RX固定/非固定 x rate_hz

![w08_cpu_affinity_tx_off_rxpin_x_rate_missing_delta_total_avg](figures/w08_cpu_affinity_tx_off_rxpin_x_rate_missing_delta_total_avg.png)

![w08_cpu_affinity_tx_off_rxpin_x_rate_p99_latency_ms_avg](figures/w08_cpu_affinity_tx_off_rxpin_x_rate_p99_latency_ms_avg.png)

![w08_cpu_affinity_tx_off_rxpin_x_rate_max_latency_ms_avg](figures/w08_cpu_affinity_tx_off_rxpin_x_rate_max_latency_ms_avg.png)

![w08_cpu_affinity_tx_off_rxpin_x_rate_last_edge_mean_latency_ms_avg](figures/w08_cpu_affinity_tx_off_rxpin_x_rate_last_edge_mean_latency_ms_avg.png)

![w08_cpu_affinity_tx_off_rxpin_x_rate_last_edge_minus_middle_mean_ms_avg](figures/w08_cpu_affinity_tx_off_rxpin_x_rate_last_edge_minus_middle_mean_ms_avg.png)

### RX非固定: TX固定/非固定 x rate_hz

![w08_cpu_affinity_rx_off_txpin_x_rate_missing_delta_total_avg](figures/w08_cpu_affinity_rx_off_txpin_x_rate_missing_delta_total_avg.png)

![w08_cpu_affinity_rx_off_txpin_x_rate_p99_latency_ms_avg](figures/w08_cpu_affinity_rx_off_txpin_x_rate_p99_latency_ms_avg.png)

![w08_cpu_affinity_rx_off_txpin_x_rate_max_latency_ms_avg](figures/w08_cpu_affinity_rx_off_txpin_x_rate_max_latency_ms_avg.png)

![w08_cpu_affinity_rx_off_txpin_x_rate_last_edge_mean_latency_ms_avg](figures/w08_cpu_affinity_rx_off_txpin_x_rate_last_edge_mean_latency_ms_avg.png)

![w08_cpu_affinity_rx_off_txpin_x_rate_last_edge_minus_middle_mean_ms_avg](figures/w08_cpu_affinity_rx_off_txpin_x_rate_last_edge_minus_middle_mean_ms_avg.png)

### rate_hz 最小・中間・最大: RX/TX 2軸

![w08_cpu_affinity_rate_5000_rxpin_x_txpin_missing_delta_total_avg](figures/w08_cpu_affinity_rate_5000_rxpin_x_txpin_missing_delta_total_avg.png)

![w08_cpu_affinity_rate_5000_rxpin_x_txpin_p99_latency_ms_avg](figures/w08_cpu_affinity_rate_5000_rxpin_x_txpin_p99_latency_ms_avg.png)

![w08_cpu_affinity_rate_5000_rxpin_x_txpin_max_latency_ms_avg](figures/w08_cpu_affinity_rate_5000_rxpin_x_txpin_max_latency_ms_avg.png)

![w08_cpu_affinity_rate_5000_rxpin_x_txpin_last_edge_mean_latency_ms_avg](figures/w08_cpu_affinity_rate_5000_rxpin_x_txpin_last_edge_mean_latency_ms_avg.png)

![w08_cpu_affinity_rate_5000_rxpin_x_txpin_last_edge_minus_middle_mean_ms_avg](figures/w08_cpu_affinity_rate_5000_rxpin_x_txpin_last_edge_minus_middle_mean_ms_avg.png)

![w08_cpu_affinity_rate_50000_rxpin_x_txpin_missing_delta_total_avg](figures/w08_cpu_affinity_rate_50000_rxpin_x_txpin_missing_delta_total_avg.png)

![w08_cpu_affinity_rate_50000_rxpin_x_txpin_p99_latency_ms_avg](figures/w08_cpu_affinity_rate_50000_rxpin_x_txpin_p99_latency_ms_avg.png)

![w08_cpu_affinity_rate_50000_rxpin_x_txpin_max_latency_ms_avg](figures/w08_cpu_affinity_rate_50000_rxpin_x_txpin_max_latency_ms_avg.png)

![w08_cpu_affinity_rate_50000_rxpin_x_txpin_last_edge_mean_latency_ms_avg](figures/w08_cpu_affinity_rate_50000_rxpin_x_txpin_last_edge_mean_latency_ms_avg.png)

![w08_cpu_affinity_rate_50000_rxpin_x_txpin_last_edge_minus_middle_mean_ms_avg](figures/w08_cpu_affinity_rate_50000_rxpin_x_txpin_last_edge_minus_middle_mean_ms_avg.png)

![w08_cpu_affinity_rate_500000_rxpin_x_txpin_missing_delta_total_avg](figures/w08_cpu_affinity_rate_500000_rxpin_x_txpin_missing_delta_total_avg.png)

![w08_cpu_affinity_rate_500000_rxpin_x_txpin_p99_latency_ms_avg](figures/w08_cpu_affinity_rate_500000_rxpin_x_txpin_p99_latency_ms_avg.png)

![w08_cpu_affinity_rate_500000_rxpin_x_txpin_max_latency_ms_avg](figures/w08_cpu_affinity_rate_500000_rxpin_x_txpin_max_latency_ms_avg.png)

![w08_cpu_affinity_rate_500000_rxpin_x_txpin_last_edge_mean_latency_ms_avg](figures/w08_cpu_affinity_rate_500000_rxpin_x_txpin_last_edge_mean_latency_ms_avg.png)

![w08_cpu_affinity_rate_500000_rxpin_x_txpin_last_edge_minus_middle_mean_ms_avg](figures/w08_cpu_affinity_rate_500000_rxpin_x_txpin_last_edge_minus_middle_mean_ms_avg.png)

## 成果物

- run summary: `reports/w08_cpu_affinity_matrix_run_summary.csv`
- aggregate summary: `reports/w08_cpu_affinity_matrix_aggregate.csv`
- edge summary: `reports/w08_cpu_affinity_matrix_edge_summary.csv`
- report: `reports/w08_cpu_affinity_matrix_summary.md`