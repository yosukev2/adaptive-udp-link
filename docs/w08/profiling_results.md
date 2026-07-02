# W08 profiling results

## 目的

W08では Linux 側遅延の支配因子候補として、send interval / socket buffer size / CPU affinity の3つを比較した。
本ファイルでは、既存の #129〜#132 の計測・集計結果をもとに、W08で採用する1変数を決定する。

## baseline条件

共通baselineは W08 baseline 計測結果を使う。

- loopback: `127.0.0.1`
- port: `9000`
- payload_len: `48`
- tx duration: `10 sec`
- rx duration: `12 sec`
- recovery_mode: `fsm`
- socket buffer tuning: none
- CPU affinity: none

## 候補3つの比較

| factor | before | after | before_p95_ms | after_p95_ms | before_p99_ms | after_p99_ms | p99_change_pct | before_loss_rate | after_loss_rate | 判定 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| send interval | baseline rate_hz=100 | rate_hz=120000 | 0.019583 | 0.008185 | 0.036339 | 0.011852 | -67.39% | 0.00000000 | 0.00000000 | 120,000Hzまでmissingなし。高rateでも破綻しないことを確認したが、W08の改善変数としては「送信間隔を詰めてもまだ余裕がある」という確認に近い。 |
| socket buffer size | rate_hz=10000 socket default | rate_hz=10000 rcvbuf_requested=5000 actual=10000 | 0.014197 | 0.014229 | 0.014994 | 0.015025 | +0.21% | 0.00000000 | 0.00000000 | 10,000Hzではp99/lossにほぼ差がなく、支配因子とは言いにくい。 |
| CPU affinity | rate_hz=10000 rx_pin=off tx_pin=off | rate_hz=10000 rx_pin=on tx_pin=on | 0.014210 | 0.010550 | 0.014889 | 0.010821 | -27.32% | 0.00000000 | 0.00000000 | 同一rate条件でp99が改善し、loss副作用も0。通常時latencyの支配因子として扱いやすい。 |

## 採用する支配因子

採用する支配因子: `CPU affinity`

採用する変更値:

- before: `rate_hz=10000`, `rx_pin=off`, `tx_pin=off`
- after: `rate_hz=10000`, `rx_pin=on`, `tx_pin=on`
- default pin core: RX core 0, TX core 1

採用理由:

- `rate_hz=10000` の同一条件で、p99 latency が `0.014889 ms` から `0.010821 ms` に変化した。
- p99変化率は `-27.32%` で、socket buffer size より明確な改善がある。
- loss_rate は before/after ともに `0.00000000` で、副作用としてのmissing増加は確認されていない。
- CPU affinity は「受信/送信処理をどのcoreで実行するか」という1変数として扱いやすく、因果を説明しやすい。

## 採用しなかった候補

### send interval

`rate_hz=120000` でも loss_rate は `0.00000000` で、p99 latency も悪化していない。
これは Raspberry Pi 5 では少なくとも120,000Hz付近まで処理余裕があることを示す。
一方で、これは「send interval を変更すると改善する」というより、「10,000Hz近辺ではsend intervalが主要な悪化要因ではない」という結果であるため、W08の採用支配因子にはしない。

### socket buffer size

`rate_hz=10000` で `rcvbuf_requested=5000 actual=10000` にしても、p99 latency は `0.014994 ms` から `0.015025 ms` で、変化率は `+0.21%` だった。
loss_rate も before/after ともに `0.00000000` で、改善・悪化ともに実用上の差が小さい。
このrate帯では socket buffer size は主要な支配因子とは言いにくい。

## 注意点

CPU affinity は通常時 p99 latency には効いているが、先頭edge latency と末尾edge latency は残る。
先頭と末尾で大きい値が出る主因は、1秒ごとのstats/log処理を、送信timestamp取得後かつ `sendto()` 前に実行してしまっているためと考える。
この構造では、アプリ側の `send_time_ns` は先に記録される一方で、実際のUDP送信はstats/log処理の後になるため、受信側で計算する latency にログ処理時間が混入する。
したがって、W08で採用する支配因子は「通常時latencyの改善に効く1変数」としての CPU affinity であり、edge latency は timestamp取得位置とstats/log処理順序を修正して再評価する対象として扱う。

## 参照元

- `reports/w08_linux_latency_factor_summary.md`
- `reports/w08_send_interval_summary.md`
- `reports/w08_socket_buffer_highrate_summary.md`
- `reports/w08_cpu_affinity_matrix_summary.md`
- `data/w08/baseline/run1.csv`〜`run3.csv`
- `data/w08/send_interval/w08_send_interval_summary.csv`
- `reports/w08_socket_buffer_rate_rcvbuf_aggregate.csv`
- `reports/w08_cpu_affinity_matrix_aggregate.csv`
