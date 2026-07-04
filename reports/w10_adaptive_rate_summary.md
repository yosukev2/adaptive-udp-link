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
- trials: off/on 各10回

## 結論

- OFF は rate_hz=120000 固定。10試行平均の missing rate は 2.8919%、中央値は 2.3979%。同一rateでも run2〜4 は約0.6%、run8〜10 は約5.5〜6.0% で、試行間のばらつきが大きい。
- ON は missing 検出で rate_hz を下げた。10試行平均の最終 rate_hz は 57232、中央値は 60172。
- ON 全10試行平均の missing rate は 2.7661%、中央値は 2.3070%。OFF よりわずかに低いが、差は小さい。
- 一方で、受信できたframe総数は OFF 34,958,871、ON 18,827,169。ON は受信率を小幅に改善したが、送信rateを大きく下げたため、受信総量は OFF の約54% まで減った。
- latency は全10試行の中央値ベースでは ON が悪い。avg latency median は OFF 0.292 ms、ON 1.052 ms。
- CPU 使用率は ON が低い。avg cpu pct は OFF 31.00%、ON 18.18%。これは主に送信rateが下がったためと考える。
- したがって今回の条件では、rate_hz を下げる adaptive 制御だけで missing を安定的に制御する効果は限定的。missing は平均rateだけでなく、一時的な受信詰まり・スケジューリング・socket queue などの影響を強く受けている可能性が高い。
- rate down は緊急退避としては有効だが、総受信データ数を最大化する主手段には向きにくい。次の方向性は feedback による再送、FEC、または receive loop / buffer 側の改善が妥当。

## 受信できたframe数の比較

| mode | trials | received frames total | missing frames total | expected frames total | received rate | received frames avg/trial |
|---|---:|---:|---:|---:|---:|---:|
| off | 10 | 34,958,871 | 1,041,099 | 35,999,970 | 97.1081% | 3,495,887 |
| on | 10 | 18,827,169 | 489,057 | 19,316,226 | 97.4682% | 1,882,717 |

ON は received rate だけ見ると少し良いが、rate_hz を大きく下げるため、受信できたframe総数は OFF より大幅に少ない。

## ON/OFF 集計比較

| mode | 対象 | trials | missing rate avg | missing rate median | avg latency ms avg | avg latency ms median | p99 latency ms avg | max latency ms avg | avg cpu pct | final rate avg |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| off | run1-10 | 10 | 2.8919% | 2.3979% | 0.610 | 0.292 | 0.012 | 2362.021 | 31.00 | 120000 |
| on | run1-10 | 10 | 2.7661% | 2.3070% | 1.276 | 1.052 | 0.072 | 2975.857 | 18.18 | 57232 |
| on | missing<1%のみ | 3 | 0.2497% | 0.0615% | 0.069 | 0.040 | 0.014 | 105.940 | 22.01 | 59516 |

## run別詳細

| mode | trial | ok frames | missing frames | missing rate | avg latency ms | p99 latency ms | max latency ms | avg cpu pct | start rate | final rate | min rate | max rate | dec/inc/hold |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| off | 1 | 3517962 | 82035 | 2.2788% | 0.155 | 0.011 | 147.718 | 33.37 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 2 | 3577896 | 22101 | 0.6139% | 0.060 | 0.010 | 12.249 | 34.80 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 3 | 3577863 | 22134 | 0.6148% | 0.060 | 0.011 | 11.672 | 34.98 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 4 | 3579003 | 20994 | 0.5832% | 0.058 | 0.011 | 12.024 | 33.80 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 5 | 3509385 | 90612 | 2.5170% | 0.170 | 0.009 | 168.943 | 32.04 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 6 | 3472455 | 127542 | 3.5428% | 1.280 | 0.013 | 6376.202 | 27.91 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 7 | 3543564 | 56433 | 1.5676% | 0.414 | 0.013 | 1919.482 | 30.34 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 8 | 3393978 | 206019 | 5.7228% | 1.319 | 0.014 | 4667.421 | 27.66 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 9 | 3402447 | 197550 | 5.4875% | 1.096 | 0.014 | 4788.481 | 28.22 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| off | 10 | 3384318 | 215679 | 5.9911% | 1.486 | 0.013 | 5516.020 | 26.90 | 120000 | 120000 | 120000 | 120000 | 0/0/30 |
| on | 1 | 1500414 | 133920 | 8.1942% | 3.368 | 0.390 | 6651.496 | 13.35 | 120000 | 26979 | 26979 | 120000 | 8/6/16 |
| on | 2 | 2116620 | 13452 | 0.6315% | 0.128 | 0.017 | 296.904 | 21.19 | 120000 | 68674 | 54190 | 120000 | 6/16/8 |
| on | 3 | 2144061 | 1320 | 0.0615% | 0.040 | 0.013 | 11.599 | 22.67 | 120000 | 54937 | 54937 | 120000 | 7/16/7 |
| on | 4 | 1847313 | 40458 | 2.1432% | 2.423 | 0.012 | 6611.555 | 17.11 | 120000 | 68675 | 39321 | 120000 | 6/16/8 |
| on | 5 | 2208477 | 1236 | 0.0559% | 0.039 | 0.012 | 9.317 | 22.18 | 120000 | 54937 | 54937 | 120000 | 7/16/7 |
| on | 6 | 1692693 | 42885 | 2.4709% | 1.851 | 0.013 | 4405.169 | 15.42 | 120000 | 65405 | 36416 | 120000 | 6/15/9 |
| on | 7 | 2019408 | 72132 | 3.4488% | 1.160 | 0.017 | 3398.599 | 19.78 | 120000 | 68675 | 49152 | 120000 | 6/16/8 |
| on | 8 | 1426710 | 84207 | 5.5732% | 0.945 | 0.225 | 788.037 | 13.50 | 120000 | 31233 | 29745 | 120000 | 8/9/13 |
| on | 9 | 1838802 | 65439 | 3.4365% | 2.626 | 0.011 | 7149.171 | 16.15 | 120000 | 77862 | 39321 | 120000 | 5/14/11 |
| on | 10 | 2032671 | 34008 | 1.6455% | 0.177 | 0.012 | 436.721 | 20.49 | 120000 | 54939 | 49152 | 120000 | 7/16/7 |

## adaptive ON 時系列グラフ

missing rate は adaptive feedback window ごとの値。rate_hz は tx が次に使う送信 rate。

![ON all trials](figures/w10_adaptive_on_all_trials_rate_missing.png)

![OFF all trials missing rate](figures/w10_adaptive_off_all_trials_missing_rate.png)

![OFF/ON boxplot](figures/w10_adaptive_off_on_boxplot.png)

![Missing rate histogram by feedback window](figures/w10_adaptive_missing_rate_histogram.png)

missing rate histogram は trial単位ではなく、OFF/ON 各10試行の約1秒 feedback window をすべて含めた分布。

![ON run1](figures/w10_adaptive_on_run1_missing_rate_rate_hz.png)

![ON run2](figures/w10_adaptive_on_run2_missing_rate_rate_hz.png)

![ON run3](figures/w10_adaptive_on_run3_missing_rate_rate_hz.png)

![ON run4](figures/w10_adaptive_on_run4_missing_rate_rate_hz.png)

![ON run5](figures/w10_adaptive_on_run5_missing_rate_rate_hz.png)

![ON run6](figures/w10_adaptive_on_run6_missing_rate_rate_hz.png)

![ON run7](figures/w10_adaptive_on_run7_missing_rate_rate_hz.png)

![ON run8](figures/w10_adaptive_on_run8_missing_rate_rate_hz.png)

![ON run9](figures/w10_adaptive_on_run9_missing_rate_rate_hz.png)

![ON run10](figures/w10_adaptive_on_run10_missing_rate_rate_hz.png)

## 生成物

- run summary CSV: `reports/w10_adaptive_rate_run_summary.csv`
- report: `reports/w10_adaptive_rate_summary.md`
- figures: `reports/figures/w10_adaptive_on_*.png`, `reports/figures/w10_adaptive_off_on_boxplot.png`, `reports/figures/w10_adaptive_missing_rate_histogram.png`, `reports/figures/w10_adaptive_off_all_trials_missing_rate.png`
