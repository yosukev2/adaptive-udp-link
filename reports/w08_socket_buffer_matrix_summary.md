# W08 #131 socket buffer matrix report

## 目的

- `SO_RCVBUF` の requested 値を変えたとき、UDP loopback の `missing_delta_total` と latency がどう変わるかを確認する。
- #130 の `rate_hz=14000` 付近で見えた missing 増大が、受信 socket buffer の小ささで説明できるかを切り分ける。

## 結論

- #131 全体では 192 runs を確認し、すべて `run_validity=ok`。
- `SO_RCVBUF` の actual は requested と一致しない。最小側では `100 / 512 / 1024` がすべて `actual=2304` に丸められ、大きい側では `262144` 以上が `actual=425984` の天井に丸められた。
- missing は socket buffer size と単調には対応しなかった。`actual=2304` まで小さくしても #130 の大きな missing は再現していない。
- #131 内で最も missing が大きい集計条件は `rate_hz=10000, requested=65536, actual=131072` の `missing_avg=40.0`。ただしこれは重複条件6 trialsの平均で、同じ buffer size だから必ず悪い、とは言えない。
- p99 latency は全体として狭い範囲に収まった。最小は `0.013271 ms`、最大は `0.019710 ms` 程度で、buffer size による大きな改善・悪化は確認できない。
- max latency は外れ値の影響を受ける。最大の集計条件は `rate_hz=10000, requested=65536, actual=131072` の `max_latency_ms_avg=12.709301 ms`。平均・p99と分けて扱う必要がある。
- 実用上の安定候補は、missing が概ね出ず actual も天井に張り付かない `requested=16384(actual=32768)` 以上。ただし #131 の結果だけでは最適値を一意には決めない。

## 実験セット

| set | runs | invalid |
| --- | ---: | ---: |
| large matrix | 108 | 0 |
| lowbuf matrix | 54 | 0 |
| tiny sweep | 30 | 0 |

- 共通条件: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none, SO_SNDBUF default
- rate_hz: `10000 / 12000 / 14000 / 16000 / 18000 / 20000`
- heatmap / 差分表では、actual が `425984` に丸められた列を代表 `262144/425984` の1列に圧縮した。

## requested と actual の事実

`SO_RCVBUF` は requested 値がそのまま使われない。今回観測した対応は以下。

| requested | actual |
| ---: | ---: |
| 100 | 2304 |
| 512 | 2304 |
| 1024 | 2304 |
| 4096 | 8192 |
| 8000 | 16000 |
| 8192 | 16384 |
| 16384 | 32768 |
| 32768 | 65536 |
| 49152 | 98304 |
| 65536 | 131072 |
| 98304 | 196608 |
| 262144 | 425984 |
| 1048576 | 425984 |
| 4194304 | 425984 |
| 8388608 | 425984 |
| 16777216 | 425984 |

差分として重要なのは以下。

- `100 / 512 / 1024` はすべて `actual=2304`。これより細かい requested の違いは、今回の環境では actual buffer 差になっていない。
- `4096` 以上は概ね2倍の actual になった。
- `262144` 以上は `actual=425984` に丸められたため、巨大な requested 値同士の比較は実質同じ buffer size の比較になる。

## missing に関する事実と差

- heatmap集計後の条件数は 37。このうち `missing_avg=0` は 27 条件、非ゼロは 10 条件。
- `missing_avg` は同一条件の trial における `missing_delta_total` の平均。packet数ではなく、seq の飛びから見た frame 欠落数。
- 非ゼロ条件の上位は以下。

| rate_hz | requested/actual | trials | missing_avg | p99_ms | max_ms |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10000 | 65536/131072 | 6 | 40.0 | 0.016904 | 12.709300 |
| 14000 | 8192/16384 | 3 | 35.0 | 0.016944 | 4.247707 |
| 14000 | 1024/2304 | 3 | 28.0 | 0.013271 | 1.936266 |
| 10000 | 8192/16384 | 3 | 22.0 | 0.014975 | 4.047403 |
| 14000 | 100/2304 | 3 | 21.0 | 0.016234 | 1.777476 |
| 10000 | 1024/2304 | 3 | 11.0 | 0.015531 | 1.525907 |
| 14000 | 8000/16000 | 3 | 7.0 | 0.014759 | 2.033836 |
| 18000 | 8192/16384 | 3 | 6.0 | 0.014549 | 2.059567 |
| 10000 | 100/2304 | 3 | 3.0 | 0.015086 | 0.660421 |
| 14000 | 512/2304 | 3 | 3.0 | 0.016339 | 0.556144 |

missing の差分として言えること:

- 最小 actual `2304` でも missing は小さい。`rate_hz=14000` では `requested=100/512/1024` の missing_avg は `21.0 / 3.0 / 28.0`。#130 の大きな missing を説明する規模ではない。
- `requested=4096(actual=8192)` は `rate_hz=10000/14000` ともに `missing_avg=0.0`。
- `requested=8192(actual=16384)` は `rate_hz=10000/14000/18000` で `22.0 / 35.0 / 6.0` と少量の missing が出た。
- `requested=16384(actual=32768)` 以上では、今回の lowbuf matrix 範囲では missing は基本的に 0。ただし重複して実施した `requested=65536(actual=131072)` の `rate_hz=10000` では外れ値を含み、統合平均で `40.0` になった。
- よって missing は buffer size だけで単調に説明できず、run の揺らぎやスケジューリングの影響を含む。

## latency に関する事実と差

p99 latency の下位・上位は以下。

### p99 latency が小さい条件

| rate_hz | requested/actual | p99_ms | missing_avg |
| ---: | ---: | ---: | ---: |
| 14000 | 1024/2304 | 0.013271 | 28.0 |
| 14000 | 98304/196608 | 0.014241 | 0.0 |
| 18000 | 262144/425984 | 0.014454 | 0.0 |
| 18000 | 8192/16384 | 0.014549 | 6.0 |
| 18000 | 16384/32768 | 0.014691 | 0.0 |
| 20000 | 65536/131072 | 0.014759 | 0.0 |
| 14000 | 8000/16000 | 0.014759 | 7.0 |
| 10000 | 512/2304 | 0.014907 | 0.0 |

### p99 latency が大きい条件

| rate_hz | requested/actual | p99_ms | missing_avg |
| ---: | ---: | ---: | ---: |
| 18000 | 49152/98304 | 0.019710 | 0.0 |
| 14000 | 49152/98304 | 0.019056 | 0.0 |
| 10000 | 16384/32768 | 0.018574 | 0.0 |
| 18000 | 65536/131072 | 0.018340 | 0.0 |
| 10000 | 49152/98304 | 0.017969 | 0.0 |
| 10000 | 98304/196608 | 0.017839 | 0.0 |
| 18000 | 98304/196608 | 0.017679 | 0.0 |
| 10000 | 262144/425984 | 0.017398 | 0.0 |

latency の差分として言えること:

- p99 latency はおおむね `0.013〜0.020 ms` の範囲で、buffer size による大きな差は出ていない。
- p99 が最大の条件は `rate_hz=18000, requested=49152(actual=98304)` の `0.019710 ms` だが、missing は `0.0`。latency と missing は同じ方向に動いていない。
- p99 が小さい条件にも `requested=1024(actual=2304)` が含まれる。小さい buffer が必ず latency を悪化させるとは言えない。
- mean latency は一部 outlier 条件を除くと概ね `0.011〜0.016 ms` 程度。`rate_hz=10000, requested=65536(actual=131072)` は `mean=0.045243 ms` まで上がっており、外れ値の影響が強い。

## max latency / outlier

max latency は外れ値の影響を受けるため、p99とは分けて評価する。上位は以下。

| rate_hz | requested/actual | max_ms | mean_ms | p99_ms | missing_avg |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10000 | 65536/131072 | 12.709300 | 0.045243 | 0.016904 | 40.0 |
| 14000 | 8192/16384 | 4.247707 | 0.014108 | 0.016944 | 35.0 |
| 10000 | 8192/16384 | 4.047403 | 0.012975 | 0.014975 | 22.0 |
| 18000 | 32768/65536 | 3.913160 | 0.014085 | 0.015352 | 0.0 |
| 14000 | 16384/32768 | 3.217655 | 0.012354 | 0.015531 | 0.0 |
| 10000 | 32768/65536 | 2.775619 | 0.015212 | 0.017327 | 0.0 |
| 16000 | 65536/131072 | 2.718029 | 0.011672 | 0.016704 | 0.0 |
| 18000 | 262144/425984 | 2.654632 | 0.013649 | 0.014454 | 0.0 |

- `rate_hz=10000, requested=65536(actual=131072)` は missing と max latency の両方が大きく、今回の外れ値条件。
- ただし他の max latency 上位には missing 0 の条件も多い。tail latency と missing は別指標として扱う。

## heatmaps

actual が kernel 上限 `425984` に丸められた列は、代表として `262144/425984` の1列に圧縮した。

- missing average heatmap: `reports/figures/w08_socket_buffer_heatmap_missing_avg.png`
- p99 latency heatmap: `reports/figures/w08_socket_buffer_heatmap_p99_latency_ms.png`
- mean latency heatmap: `reports/figures/w08_socket_buffer_heatmap_mean_latency_ms.png`
- heatmap source summary: `reports/w08_socket_buffer_heatmap_summary.csv`

![W08 socket buffer missing avg heatmap](figures/w08_socket_buffer_heatmap_missing_avg.png)

![W08 socket buffer p99 latency heatmap](figures/w08_socket_buffer_heatmap_p99_latency_ms.png)

![W08 socket buffer mean latency heatmap](figures/w08_socket_buffer_heatmap_mean_latency_ms.png)

## #131 の判断

- #130 の missing 増大は、#131 の socket buffer sweep では再現しなかった。buffer size 単独原因とは判断しない。
- `SO_RCVBUF` を極端に大きくしても actual が天井に張り付くため、巨大値を細かく比較する意味は薄い。
- `requested=16384(actual=32768)` 以上を安定候補とし、それ以上の調整は performance 本命Issueで CPU affinity / rate / OS scheduling と合わせて評価する。

## 成果物

- 実行スクリプト: `scripts/w08/run_socket_buffer_matrix.sh`
- 追加実行スクリプト: `scripts/w08/run_socket_buffer_tiny_sweep.sh`
- 集計スクリプト: `scripts/analyze_w08_socket_buffer_matrix.py`
- heatmap生成スクリプト: `scripts/analyze_w08_socket_buffer_heatmaps.py`
- 単一レポート: `reports/w08_socket_buffer_matrix_summary.md`
- heatmap集計CSV: `reports/w08_socket_buffer_heatmap_summary.csv`
- raw/summary data: `data/w08/socket_buffer_matrix/`, `data/w08/socket_buffer_matrix_lowbuf/`, `data/w08/socket_buffer_tiny/`
