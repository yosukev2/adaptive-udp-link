# W10 adaptive rate comparison summary

## 実験条件

- host: Raspberry Pi 5 loopback
- rx core: 2
- tx core: 3
- initial rate_hz: 120000
- tx duration: 30 sec
- rx duration: 32 sec
- adaptive_min_rate_hz: 1000
- adaptive_max_rate_hz: 500000
- adaptive_high_latency_ms: 0
- trials: off/on 各3回

## 結論

- OFF は rate_hz=120000 固定。3試行平均の missing rate は 0.6150%、平均 latency は 0.087 ms。
- ON は missing 検出で rate_hz を下げた。3試行平均の最終 rate_hz は 57857。
- ON の3試行平均 missing rate は 1.1550% で、OFF 平均より悪い。ただしこれは run1 の大きな崩れの影響が強い。
- ON run2/run3 に限ると missing rate は 0.0691% で、OFF 平均 0.6150% より明確に低い。
- latency は ON run2/run3 では平均 0.038 ms で OFF 平均 0.087 ms より低い。一方 ON run1 は平均 0.482 ms、max 347.932 ms まで跳ねた。
- したがって今回の結果は「adaptive ON が常に優位」とは言えない。run2/run3 では missing と latency が改善したが、run1 のように制御初期に大きく崩れるケースがある。
- 次の確認ポイントは、ON run1 の 5秒付近の missing spike と rate 低下が再現性のある現象か、初期制御パラメータの問題かを切り分けること。

## ON/OFF 平均比較

| mode | 対象 | missing rate | avg latency ms | p99 latency ms | max latency ms | avg cpu pct | final rate avg |
|---|---|---:|---:|---:|---:|---:|---:|
| off | run1-3 | 0.6150% | 0.087 | 0.010 | 122.431 | 33.60 | 120000 |
| on | run1-3 | 1.1550% | 0.186 | 0.012 | 123.430 | 18.22 | 57857 |
| on | run2-3のみ | 0.0691% | 0.038 | 0.012 | 11.179 | 19.81 | 70388 |

## run別詳細

| mode | trial | ok frames | missing frames | missing rate | avg latency ms | p99 latency ms | max latency ms | avg cpu pct | start rate | final rate | min rate | max rate | dec/inc/hold |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| off | 1 | 3579348 | 20649 | 0.5736% | 0.058 | 0.008 | 12.108 | 33.26 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 2 | 3572994 | 24897 | 0.6920% | 0.146 | 0.011 | 343.575 | 33.76 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 3 | 3579141 | 20856 | 0.5793% | 0.058 | 0.010 | 11.608 | 33.78 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| on | 1 | 1470717 | 50613 | 3.3269% | 0.482 | 0.013 | 347.932 | 15.04 | 120000 | 32795 | 29745 | 120000 | 8/10/12 |
| on | 2 | 2208525 | 1221 | 0.0553% | 0.038 | 0.013 | 9.345 | 22.13 | 120000 | 54937 | 54937 | 120000 | 7/16/7 |
| on | 3 | 1765446 | 1464 | 0.0829% | 0.037 | 0.011 | 13.013 | 17.49 | 120000 | 85839 | 55330 | 132300 | 5/16/11 |

## adaptive ON 時系列グラフ

missing rate は adaptive feedback window ごとの値。rate_hz は tx が次に使う送信 rate。

![ON all trials](figures/w10_adaptive_on_all_trials_rate_missing.png)

![ON run1](figures/w10_adaptive_on_run1_missing_rate_rate_hz.png)

![ON run2](figures/w10_adaptive_on_run2_missing_rate_rate_hz.png)

![ON run3](figures/w10_adaptive_on_run3_missing_rate_rate_hz.png)

## 生成物

- run summary CSV: `reports/w10_adaptive_rate_run_summary.csv`
- report: `reports/w10_adaptive_rate_summary.md`
- figures: `reports/figures/w10_adaptive_on_*.png`
