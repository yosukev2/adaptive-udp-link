# adaptive-udp-link

UDP ベースの自己回復リンク基盤を段階的に実装しながら、観測・耐障害化・適応制御まで積み上げる C プロジェクトです。W04 では「同一条件での計測結果を再現できること」を重視し、`trial_summary`、1 秒統計、再現性チェック、CI を固定しています。
## 目次

- [プロジェクト概要と主要成果](#プロジェクト概要と主要成果)
  - [再現可能な計測基盤](#1-再現可能な計測基盤)
  - [負荷限界とリアルタイム性の可視化](#2-負荷限界とリアルタイム性の可視化)
  - [欠落原因に合わせた自己回復](#3-欠落原因に合わせた自己回復)
- [実験成果の詳細](#実験成果の詳細)
  - [比較の土台を作る](#1-まず比較の土台を作る)
  - [限界を特定する](#2-次にどこから壊れるかを特定する)
  - [周期処理を守る方法を検証する](#3-組み込みで周期処理を守る方法を検証する)
  - [欠落の種類ごとに回復方式を選ぶ](#4-最後に欠落の種類ごとに回復方式を選ぶ)
- [成果物と再現方法](#成果物と再現方法)
- [Repository Layout](#repository-layout)
- [Prerequisites](#prerequisites)
- [Build And Test](#build-and-test)
- [Quick Loopback Run](#quick-loopback-run)
- [Reproducibility Check](#reproducibility-check)
- [W05 Recovery Matrix](#w05-recovery-matrix)
- [W05 FSM Vs Timeout Compare](#w05-fsm-vs-timeout-compare)
- [How To Read P95 And P99](#how-to-read-p95-and-p99)
- [Protocol Notes](#protocol-notes)
- [CI](#ci)

## プロジェクト概要と主要成果

このプロジェクトでは、**測る → 限界を特定する → 壊れても戻す**の順で UDP リンクを設計しました。数値は Raspberry Pi 5 loopback または Raspberry Pi Pico の独立試行です。

### 1. 再現可能な計測基盤

`trial_summary`、P50/P95/P99、seq gap、CRC、CPU 使用率を固定フォーマットで記録し、3 trial の P99 が平均の ±15% 以内かを自動判定するスクリプトと CI を整備しました。改善を単発の最良値ではなく分布として比較できます。

### 2. 負荷限界とリアルタイム性の可視化

送信レートを 50〜1,000,000 Hz で掃引し、**120,000 Hz までは欠落なし、140,000 Hz から gap、500,000 Hz では欠落率 2.37%・P99 0.410 ms** を確認しました。処理能力/socket queue の限界を超えると、latency より先に drop が現れます。

![送信レートと欠落の関係](reports/figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_missing_delta_total_avg.png)

Pico では bare-metal と FreeRTOS を同一 workload で比較。優先度付き task 分離により TX イベントの P95/P99 jitter は **1,839 µs → 0 µs（100%削減）**、queue hand-off P95 は 8 µs、deadline miss は 0 件でした。RTOS が常に速いのではなく、周期処理を RX workload から隔離できた結果です。

![bare-metal jitter](reports/figures/w07_baremetal_abs_jitter_distribution.svg)
![FreeRTOS jitter](reports/figures/w07_freertos_abs_jitter_distribution.svg)

### 3. 欠落原因に合わせた自己回復

feedback packet を軸に adaptive rate・retransmit・XOR FEC を実装し、同一 seed / 複数 trial で比較しました。

| 手段 | 実験結果 | 示唆 |
|---|---:|---|
| adaptive rate | missing 2.8919% → 2.7661% | 改善は小幅。受信総量は約54%に低下 |
| retransmit | effective missing **45.7%削減**、54,801 frame 回復 | 有効だが平均 latency 0.750 → 10.003 ms |
| XOR FEC (k=4,r=1) | random drop 10%で effective missing **約73%削減**、usable +875,299 (120 kHz) | 単発欠落に強いが parity 待ち・複数欠落は未回復 |

![adaptive rate の OFF/ON 比較](reports/figures/w09_adaptive_off_on_boxplot.png)

結論は単一の最適解ではなく、**輻輳には rate 制御、履歴に残る欠落には retransmit、ランダム単発欠落には FEC** と故障モードに応じて選択する設計です。

## 実験成果の詳細

実験は、機能を追加するたびに「観測できるか」「限界を説明できるか」「壊れた時に回復できるか」を順に検証する流れで進めました。

### 1. まず、比較の土台を作る

最初に loopback の送受信ログへ sequence gap、CRC、P50/P95/P99、CPU 使用率を記録する共通フォーマットを導入しました。3 trial の p99 が平均の ±15% 以内かを自動判定し、単発の良い値ではなく再現性のある分布で議論できるようにしました。短い停止と長い停止も別シナリオで測り、0.5/1 秒では誤検知せず、3 秒では `Normal → Degraded → Recover → Normal` を検出する 2-window FSM を確立しました。

### 2. 次に、どこから壊れるかを特定する

Linux のレート掃引では 120 kHz まで欠落なし、140 kHz から gap、500 kHz では missing 2.37%、P99 0.410 ms となりました。socket buffer と CPU affinity も振り、drop を減らす設定が queue backlog と tail latency を増やす場合や、core 分離が原因切り分けには効いても飽和そのものは解消しないことを確認しました。レート上限を平均 latency ではなく missing・p99/max・queue backlog の組み合わせで決められるようになりました。

![送信レートと欠落の関係](reports/figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_missing_delta_total_avg.png)

### 3. 組み込みで、周期処理を守る方法を検証する

同じ RX workload を Pico の bare-metal と FreeRTOS で実行しました。FreeRTOS の優先度 `TX=3, STATE=2, RX=1` と `xTaskDelayUntil()` により、TX イベントの P95/P99 jitter は 1,839 µs から 0 µs、queue hand-off の P95 は 8 µs、deadline miss は 0 件でした。これは RTOS が常に速いという主張ではなく、重要な周期処理を低優先度 workload から隔離できることの実証です。

![bare-metal jitter](reports/figures/w07_baremetal_abs_jitter_distribution.svg)
![FreeRTOS jitter](reports/figures/w07_freertos_abs_jitter_distribution.svg)

### 4. 最後に、欠落の種類ごとに回復方式を選ぶ

限界を把握した後、feedback packet を追加し、同じ missing でも原因に応じて3方式を比較しました。

- 輻輳への退避: adaptive rate は missing を 2.8919% から 2.7661% に下げましたが、受信総量は約54%に低下しました。
- 履歴に残る欠落の回収: retransmit は effective missing を 45.7%削減し 54,801 frame を回復しました。一方、平均 latency は 0.750 ms から 10.003 ms に増えました。
- ランダム単発 drop の回復: 同一 seed の drop 10% 条件で XOR FEC (k=4,r=1) は effective missing を約73%削減し、120 kHz で usable datagram を875,299件増やしました。parity 待ちと block 内複数欠落は残る制約です。

![adaptive rate の OFF/ON 比較](reports/figures/w09_adaptive_off_on_boxplot.png)

この流れから、rate down は輻輳、retransmit は完全性、FEC は単発欠落という役割分担を導きました。改善率だけでなく、latency・throughput・冗長量とのトレードオフまで測定した点が、この実験系列の結論です。
## 成果物と再現方法

- 実験レポート: [`reports/`](reports/)、生データ: [`data/`](data/)
- プロトコル仕様: [`docs/protocol.md`](docs/protocol.md)、FEC: [`docs/w09/xor_fec_design.md`](docs/w09/xor_fec_design.md)
- ビルド・テスト: `make all && make test`
- レート掃引: `scripts/w08/run_send_interval_sweep.sh`
- FEC 比較: `scripts/w09/run_fec_comparison.sh`

以下は開発者向けの詳細な実行手順です。


## Repository Layout

```text
adaptive-udp-link/
├── README.md
├── Makefile
├── .github/workflows/ci.yml
├── bin/
├── include/
├── src/
├── scripts/
├── logs/
└── docs/
```

## Prerequisites

- `gcc`
- `make`
- `bash`

## Build And Test

```bash
make all
make test
```

`make test` は以下を実行します。

- `bin/test_framer`
- `bash scripts/test_loopback_metrics.sh`

## Quick Loopback Run

10 秒だけローカル loopback で試す場合:

```bash
make run10
```

生成物:

- `logs/run_YYYYMMDD_HHMMSS_10s/rx.log`
- `logs/run_YYYYMMDD_HHMMSS_10s/rx_in_1sec.csv`
- `logs/run_YYYYMMDD_HHMMSS_10s/rx_by_1recv.csv`
- `logs/run_YYYYMMDD_HHMMSS_10s/tx.log`

`rx_in_1sec.csv` では 1 秒ごとに `pps` と `cpu_pct` を確認できます。`pps` は UDP datagram/s、`cpu_pct` はその 1 秒窓での process CPU usage です。

## Reproducibility Check

W04 の標準手順はこのスクリプトです。

```bash
make all
RESULT_DIR=logs/reproducibility/w04_baseline_20260429 bash scripts/run_reproducibility_check.sh
```

主な生成物:

- `logs/reproducibility/w04_baseline_20260429/reproducibility_check.csv`
- `logs/reproducibility/w04_baseline_20260429/interpretation.md`
- `logs/reproducibility/w04_baseline_20260429/trial_1/`
- `logs/reproducibility/w04_baseline_20260429/trial_2/`
- `logs/reproducibility/w04_baseline_20260429/trial_3/`

環境変数で条件を上書きできます。

```bash
RATE_HZ=120 DURATION_SEC=5 PAYLOAD_LEN=64 LINK_NAME=host_loopback \
RESULT_DIR=logs/reproducibility/custom_run bash scripts/run_reproducibility_check.sh
```

## W05 Recovery Matrix

W05 の標準手順はこのスクリプトです。

```bash
make all
RESULT_DIR=logs/fsm_recovery/w05_matrix_baseline bash scripts/run_fsm_recovery_check.sh
```

主な生成物:

- `logs/fsm_recovery/w05_matrix_baseline/fsm_recovery_check.csv`
- `logs/fsm_recovery/w05_matrix_baseline/summary.txt`
- `logs/fsm_recovery/w05_matrix_baseline/scenario_500ms/trial_1/rx.log`
- `logs/fsm_recovery/w05_matrix_baseline/scenario_500ms/trial_1/tx.log`
- `logs/fsm_recovery/w05_matrix_baseline/scenario_500ms/trial_1/state.csv`
- `logs/fsm_recovery/w05_matrix_baseline/scenario_1000ms/trial_1/state.csv`
- `logs/fsm_recovery/w05_matrix_baseline/scenario_3000ms/trial_1/state.csv`

環境変数で条件を上書きできます。

```bash
TRIALS=3 LINK_NAME=host_loopback RESULT_DIR=logs/fsm_recovery/custom_run \
bash scripts/run_fsm_recovery_check.sh
```

`fsm_recovery_check.csv` には少なくとも次の列が入ります。

- `scenario`
- `trial`
- `outage_ms`
- `degraded_detect_ms`
- `recover_complete_ms`

各 run は `scenario_<duration>/trial_<n>/` にまとまり、`rx.log`、`tx.log`、`state.csv` を残します。現行の 2-window FSM では `0.5s` と `1s` の outage は `Degraded` 閾値を跨がないため、`degraded_detect_ms` と `recover_complete_ms` は `na` になります。`3s` シナリオでは `Normal -> Degraded -> Recover -> Normal` の 3 遷移を必須とし、期待した遷移パターンから外れた run はスクリプトが非 0 で終了します。

## W05 FSM Vs Timeout Compare

最終比較はこのスクリプトで行います。

```bash
make all
RESULT_DIR=logs/fsm_recovery/w05_compare_baseline bash scripts/run_fsm_vs_timeout_compare.sh
```

主な生成物:

- `logs/fsm_recovery/w05_compare_baseline/compare_runs.csv`
- `logs/fsm_recovery/w05_compare_baseline/compare_summary.csv`
- `logs/fsm_recovery/w05_compare_baseline/interpretation.md`
- `logs/fsm_recovery/w05_compare_baseline/mode_fsm/scenario_3000ms/trial_1/state.csv`
- `logs/fsm_recovery/w05_compare_baseline/mode_timeout_only/scenario_3000ms/trial_1/state.csv`

`compare_summary.csv` には少なくとも次の列が入ります。

- `outage_ms`
- `mode`
- `degraded_detect_ms`
- `recover_complete_ms`

比較 run も `mode_<name>/scenario_<duration>/trial_<n>/` にまとまり、`rx.log`、`tx.log`、`state.csv` を残します。`interpretation.md` には比較表と、短い outage が `na` になる理由、`fsm` と `timeout-only` の挙動差をまとめます。

## How To Read P95 And P99

各 trial の `rx.log` 末尾に `trial_summary` が出ます。

```text
trial_summary link_name=host_loopback trial=1 duration_sec=7 sent=na recv_ok=... gap_est=... crc_fail=... len_invalid=... preamble_miss=... resync_count=... latency_p50_ms=... latency_p95_ms=... latency_p99_ms=... latency_max_ms=...
```

3 回分をまとめて見るには:

```bash
column -s, -t < logs/reproducibility/w04_baseline_20260429/reproducibility_check.csv
```

重要列:

- `latency_p95_ms`
- `latency_p99_ms`
- `latency_max_ms`
- `p99_deviation_pct_from_mean`
- `reproducible`

## Reproducibility Criterion

W04 では、3 trial の `latency_p99_ms` それぞれについて `abs(trial_p99 - mean_p99) / mean_p99 * 100` を計算し、すべてが `+/-15%` 以内なら `reproducible=yes` と判定します。`interpretation.md` に結果と簡単な解釈を残します。

変動がしきい値を超えた場合は、まず `avg_pps` と `avg_cpu_pct` のばらつきを確認してください。そこが大きい場合、フレーム処理より先にローカルのスケジューリングやバックグラウンド負荷を疑うべきです。

## Protocol Notes

固定列の意味は [docs/protocol.md](docs/protocol.md) を参照してください。W04 では以下を固定しています。

- `trial_summary` の `latency_p50_ms / latency_p95_ms / latency_p99_ms / latency_max_ms`
- 1 秒統計の `pps / cpu_pct`
- percentile の算出規則は nearest-rank

## CI

GitHub Actions は [.github/workflows/ci.yml](.github/workflows/ci.yml) で `make all` と `make test` を `push` / `pull_request` ごとに実行します。
