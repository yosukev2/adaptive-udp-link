# W10 retransmit comparison summary

## 実験条件

- date: 2026-07-04T20:15:52+09:00
- host: Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
- branch: issue-173-w10-retransmit
- commit: 3b8ac7dfc662212a436d96088a4d89441ce4f289
- rate_hz: 120000
- tx_duration_sec: 30
- rx_duration_sec: 32
- data_port: 22001
- feedback_port: 22000
- trials: 1 2 3
- rx_core: 2
- tx_core: 3
- retransmit_buffer_datagrams: 131072
- retransmit_max_datagrams_per_feedback: 4096
- time: 2026-07-04T20:15:52+09:00

## 結論

- retransmit ON は effective_missing_total を OFF 517,431 から ON 280,728 に減らした。削減率は 45.7458%。
- raw missing rate は OFF 4.7910%、ON 3.0911%。今回のrunではON側の再送前missingも小さいため、effective_missing改善の全てを再送だけの効果とは断定しない。
- effective missing rate は OFF 4.7910%、ON 2.5993%。
- ONでは 98,583 frames を再送し、54,801 frames が後着受信として回復した。
- buffer miss は ON 2。今回のbuffer設定では再送buffer不足はほぼ観測されていない。
- latencyは再送ONで大きく悪化した。平均latencyは OFF 0.750 ms、ON 10.003 ms。再送フレームは元のtx timestampを持つため、回復できた分だけ古いデータのlatencyが大きく出る。

## 集計比較

| mode | trials | received | unique delivered | raw missing | recovered | effective missing | raw missing rate | effective missing rate | retransmit sent frames | buffer miss | avg latency ms | max latency ms | avg cpu pct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| off | 3 | 10,282,560 | 10,282,560 | 517,431 | 0 | 517,431 | 4.7910% | 4.7910% | 0 | 0 | 0.750 | 8094.658 | 29.54 |
| on | 3 | 10,519,263 | 10,519,263 | 335,529 | 54,801 | 280,728 | 3.0911% | 2.5993% | 98,583 | 2 | 10.003 | 7546.766 | 28.48 |

## run別詳細

| mode | trial | received | unique | raw missing | recovered | effective missing | raw missing rate | effective missing rate | rtx sent frames | buffer miss | avg latency ms | max latency ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| off | 1 | 3,486,525 | 3,486,525 | 113,472 | 0 | 113,472 | 3.1520% | 3.1520% | 0 | 0 | 0.207 | 518.562 |
| off | 2 | 3,490,470 | 3,490,470 | 109,527 | 0 | 109,527 | 3.0424% | 3.0424% | 0 | 0 | 0.205 | 137.700 |
| off | 3 | 3,305,565 | 3,305,565 | 294,432 | 0 | 294,432 | 8.1787% | 8.1787% | 0 | 0 | 1.837 | 8094.658 |
| on | 1 | 3,521,646 | 3,521,646 | 97,422 | 19,071 | 78,351 | 2.6919% | 2.1764% | 34,101 | 0 | 9.925 | 3818.633 |
| on | 2 | 3,473,877 | 3,473,877 | 142,296 | 16,176 | 126,120 | 3.9350% | 3.5033% | 30,117 | 2 | 11.151 | 7546.766 |
| on | 3 | 3,523,740 | 3,523,740 | 95,811 | 19,554 | 76,257 | 2.6470% | 2.1183% | 34,365 | 0 | 8.933 | 3444.864 |

## 生成物

- summary CSV: `reports/w10_retransmit_comparison.csv`
- report: `reports/w10_retransmit_summary.md`
