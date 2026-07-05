# W10 random_drop + XOR FEC比較 summary

## 実験条件

- date: 2026-07-05T11:08:52+09:00
- host: Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
- branch: issue-162-w10-fec-comparison
- commit: 05c4bae86927f1dcf41398c5b1f2570d03fa8322
- rate_hz: 1200
- drop_rate: 0.10
- drop_seeds: 101 102 103 104 105 106 107 108 109 110
- tx_duration_sec: 30
- rx_duration_sec: 32
- data_port: 24001
- trials: 1 2 3 4 5 6 7 8 9 10
- rx_core: 2
- tx_core: 3
- data_dir: data/w10/fec_comparison
- log_dir: logs/w10/fec_comparison
- loopback: 127.0.0.1
- payload_len: 48
- FEC ON: tx/rx both --fec-mode xor
- FEC OFF: tx/rx both --fec-mode off
- random drop target: datagram
- 同じtrial番号ではFEC OFF/ONで同じdrop_seedを使う

## 結論

- FEC ON(xor) は effective_missing_total を OFF 36,312 から ON 9,756 に減らした。削減率は 73.1328%。
- 結果的に使えるdatagram数は OFF 107,904、ON 116,757。差分は ON-OFF = +8,853 datagrams。
- effective_missing_rate は OFF 10.0860%、ON 2.7098%。
- raw_missing_total は OFF 36,312、ON 36,315 でほぼ同じ。したがって、差はrandom_drop条件差ではなくFEC回復の効果として見てよい。
- FEC ONでは recovered_count=26,559 frames、fec_recovered_datagrams=8,853 datagrams を回復した。
- FEC ONでも unrecovered_count=9,756 frames が残った。XOR k=4,r=1 は1 block内で複数data datagramが欠ける、またはparity datagramが欠ける条件では回復できない。
- latency p99平均は OFF 0.012 ms、ON 7.521 ms。FEC回復フレームはparity到着後に復元されるため、latencyは増える。

## 集計比較

| fec_mode | trials | usable datagrams | usable datagram rate | raw missing | recovered frames | unrecovered frames | effective missing | raw missing rate | effective missing rate | avg p99 latency ms | max latency ms | avg cpu pct | dropped datagrams |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| off | 10 | 107,904 | 89.9140% | 36,312 | 0 | 36,312 | 36,312 | 10.0860% | 10.0860% | 0.012 | 5.000 | 0.451 | 12,106 |
| xor | 10 | 116,757 | 97.2902% | 36,315 | 26,559 | 9,756 | 9,756 | 9.3938% | 2.7098% | 7.521 | 7.000 | 0.506 | 12,106 |

## run別結果

| trial | seed | fec_mode | usable datagrams | raw missing | recovered | unrecovered | effective missing | effective missing rate | p99 latency ms | max latency ms | dropped datagrams |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 101 | off | 10,772 | 3,684 | 0 | 3,684 | 3,684 | 10.2333% | 0.012 | 0.000 | 1,229 |
| 1 | 101 | xor | 11,677 | 3,684 | 2,715 | 969 | 969 | 2.6917% | 7.520 | 7.000 | 1,229 |
| 2 | 102 | off | 10,757 | 3,729 | 0 | 3,729 | 3,729 | 10.3583% | 0.012 | 0.000 | 1,244 |
| 2 | 102 | xor | 11,685 | 3,732 | 2,784 | 948 | 948 | 2.6331% | 7.521 | 7.000 | 1,244 |
| 3 | 103 | off | 10,803 | 3,594 | 0 | 3,594 | 3,594 | 9.9825% | 0.012 | 1.000 | 1,198 |
| 3 | 103 | xor | 11,660 | 3,594 | 2,571 | 1,023 | 1,023 | 2.8414% | 7.521 | 7.000 | 1,198 |
| 4 | 104 | off | 10,842 | 3,477 | 0 | 3,477 | 3,477 | 9.6575% | 0.012 | 0.000 | 1,159 |
| 4 | 104 | xor | 11,694 | 3,477 | 2,556 | 921 | 921 | 2.5581% | 7.519 | 7.000 | 1,159 |
| 5 | 105 | off | 10,786 | 3,645 | 0 | 3,645 | 3,645 | 10.1242% | 0.012 | 0.000 | 1,215 |
| 5 | 105 | xor | 11,659 | 3,645 | 2,619 | 1,026 | 1,026 | 2.8498% | 7.521 | 7.000 | 1,215 |
| 6 | 106 | off | 10,783 | 3,654 | 0 | 3,654 | 3,654 | 10.1492% | 0.012 | 5.000 | 1,218 |
| 6 | 106 | xor | 11,667 | 3,654 | 2,652 | 1,002 | 1,002 | 2.7831% | 7.521 | 7.000 | 1,218 |
| 7 | 107 | off | 10,759 | 3,726 | 0 | 3,726 | 3,726 | 10.3491% | 0.012 | 0.000 | 1,242 |
| 7 | 107 | xor | 11,683 | 3,726 | 2,772 | 954 | 954 | 2.6498% | 7.521 | 7.000 | 1,242 |
| 8 | 108 | off | 10,814 | 3,561 | 0 | 3,561 | 3,561 | 9.8908% | 0.012 | 0.000 | 1,187 |
| 8 | 108 | xor | 11,709 | 3,561 | 2,685 | 876 | 876 | 2.4331% | 7.521 | 7.000 | 1,187 |
| 9 | 109 | off | 10,770 | 3,693 | 0 | 3,693 | 3,693 | 10.2575% | 0.012 | 0.000 | 1,231 |
| 9 | 109 | xor | 11,643 | 3,693 | 2,619 | 1,074 | 1,074 | 2.9831% | 7.520 | 7.000 | 1,231 |
| 10 | 110 | off | 10,818 | 3,549 | 0 | 3,549 | 3,549 | 9.8575% | 0.012 | 0.000 | 1,183 |
| 10 | 110 | xor | 11,680 | 3,549 | 2,586 | 963 | 963 | 2.6748% | 7.520 | 7.000 | 1,183 |

## 生成物

- summary CSV: `data/w10/fec_comparison/fec_comparison.csv`
- metadata: `data/w10/fec_comparison/run_metadata.md`
- Pi5 raw logs: `logs/w10/fec_comparison/*`（PRには容量を抑えるためsummary CSVとmetadataを収録）
