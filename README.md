# adaptive-udp-link

UDP ベースの自己回復リンク基盤を段階的に実装しながら、観測・耐障害化・適応制御まで積み上げる C プロジェクトです。W04 では「同一条件での計測結果を再現できること」を重視し、`trial_summary`、1 秒統計、再現性チェック、CI を固定しています。
## 目次

- [3つの主要成果](#3つの主要成果)
  - [再現可能な計測基盤と障害検知FSM](#1-再現可能な計測基盤と障害検知fsm)
  - [Bare-metal/FreeRTOSのリアルタイム性とUDP負荷限界](#2-bare-metalfreertosのリアルタイム性とudp負荷限界)
  - [Feedbackベース自己回復](#3-feedbackベース自己回復-adaptive-rate再送xor-fec)
- [成果物と再現方法](#成果物と再現方法)
- [開発・実験コマンド](#開発実験コマンド)
  - [Build And Test](#build-and-test)
  - [Quick Loopback Run](#quick-loopback-run)
  - [Reproducibility Check](#reproducibility-check)
  - [W05 Recovery Matrix](#w05-recovery-matrix)
  - [W05 FSM Vs Timeout Compare](#w05-fsm-vs-timeout-compare)
  - [How To Read P95 And P99](#how-to-read-p95-and-p99)
  - [Protocol Notes](#protocol-notes)
  - [CI](#ci)
- [Repository Layout](#repository-layout)
- [Prerequisites](#prerequisites)
## 3つの主要成果

このプロジェクトでは、**測る → 限界を特定する → 壊れても戻す**の順で UDP リンクを設計しました。数値は Raspberry Pi 5 loopback または Raspberry Pi Pico の独立試行です。

### 1. 再現可能な計測基盤と障害検知FSM
**目的**：UDP性能と障害復旧を、同じ指標・同じ条件で再現可能に比較する。

**実験方法**：Pi 5 loopbackで複数trialを実行し、P50/P95/P99、seq gap、CRC、CPU使用率を固定形式で記録。0.5/1/3秒のoutageを注入し、FSMとtimeout-onlyを比較。

**結果のまとめ**：P99の再現性を確認し、3秒outageではFSMの状態遷移を検出。


UDPリンクの改善を評価するには、まず「何が起きたか」を同じ尺度で記録する必要があります。そこで `trial_summary` に P50/P95/P99、seq gap、CRC、CPU 使用率を固定し、3 trial の P99 が平均の ±15% 以内かを自動判定するスクリプトと CI を整備しました。さらに outage を 0.5/1/3 秒で再現し、短い揺らぎは無視し、3 秒停止だけを `Normal → Degraded → Recover → Normal` と検出する2-window FSMを実装しました。結果として、性能改善と障害検知を同じログから再現可能に比較できる基盤を作りました。

関連データ: [W04 reproducibility](logs/reproducibility/w04_baseline_20260429/reproducibility_check.csv)、[W05 FSM compare](logs/fsm_recovery/w05_compare_baseline/compare_summary.csv)。

![FSMの障害検知と復旧](reports/figures/readme_fsm_recovery.png)

さらにLinuxとPicoのjitterを同じpercentile規則で比較するため、[W06 report](reports/w06_jitter_summary.md) と [W06 raw data](data/w06/jitter_comparison.csv) を整備しました。

### 2. Bare-metal/FreeRTOSのリアルタイム性とUDP負荷限界
**目的**：UDP処理がどのレートで飽和するか、また周期TX処理をRX負荷から守れるかを明らかにする。

**実験方法**：Pi 5では送信レート・socket buffer・CPU affinityを掃引。Picoでは同一RX workloadをBare-metalとFreeRTOSで各3回実行し、TX jitterとqueue hand-offを測定。

**結果のまとめ**：Pi 5では120 kHzまで欠落なし、PicoではFreeRTOSのTX jitter P95/P99を0 µsに抑制。


Linux loopbackで送信レートを 50〜1,000,000 Hz、socket buffer、CPU affinity の組み合わせで掃引しました。**120,000 Hz までは欠落なし、140,000 Hz から gap、500,000 Hz では欠落率 2.37%・P99 0.410 ms** となり、処理能力/socket queue の限界を超えると latency の連続的な悪化より先に drop が現れることを確認しました。これにより、レート上限を平均値だけで決めず、missing・p99/max・queue backlog の境界として設計できるようにしました。

![送信レートと欠落の関係](reports/figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_missing_delta_total_avg.png)

関連データ: [W08 rate sweep summary](reports/w08_send_interval_summary.md)、[summary CSV](data/w08/send_interval/w08_send_interval_summary.csv)。50〜1,000,000 Hzを各3 trialで測定し、sample数、実効受信rate、missing、CPU、mean/p95/p99/max latencyを集計しました。socket buffer/CPU affinityの比較結果は [W08 socket buffer](reports/w08_socket_buffer_highrate_summary.md) と [W08 CPU affinity](reports/w08_cpu_affinity_matrix_summary.md) にまとめています。

Pico では bare-metal と FreeRTOS を同一 workload で比較。優先度付き task 分離により TX イベントの P95/P99 jitter は **1,839 µs → 0 µs（100%削減）**、queue hand-off P95 は 8 µs、deadline miss は 0 件でした。RTOS が常に速いのではなく、周期処理を RX workload から隔離できた結果です。

![bare-metal jitter](reports/figures/w07_baremetal_abs_jitter_distribution.svg)

![Bare-metal / FreeRTOS比較](reports/figures/readme_rtos_jitter.png)
![FreeRTOS jitter](reports/figures/w07_freertos_abs_jitter_distribution.svg)

![bare-metal / FreeRTOS jitter比較](reports/figures/readme_rtos_jitter.png)

関連データ: [W07 report](reports/w07_rtos_jitter_summary.md)、[summary CSV](data/w07/w07_jitter_summary.csv)。Picoで各モード3 run、各999 intervalを取得し、jitter分布、queue latency、deadline miss、queue send failureまで集計しました。実装は [FreeRTOS firmware](firmware/w07_rtos_jitter/) と [task architecture](docs/w07_task_architecture.md) に記録しています。

### 3. Feedbackベース自己回復（Adaptive Rate・再送・XOR FEC）
**目的**：欠落の原因に応じて回復方式を選べるようにし、missing削減とlatency・throughputのトレードオフを測定する。

**実験方法**：feedback packetを追加し、Adaptive Rate、Retransmit、XOR FECを実装。ON/OFF、同一drop seed、複数trialでraw missing、recovered、effective missing、usable datagramを比較。

**結果のまとめ**：Adaptive Rate、Retransmit、XOR FECのいずれも欠落を改善したが、各方式でthroughputまたはlatencyのコストを確認。


欠落を検出するだけでなく回復させるため、feedback packet、bounded retransmit buffer、XOR parity を実装しました。同一 seed / 複数 trial で ON/OFF を比較し、missing rateだけでなく effective missing、usable datagram、latencyまで評価しました。

| 手段 | 実験結果 | 示唆 |
|---|---:|---|
| adaptive rate | missing 2.8919% → 2.7661% | 改善は小幅。受信総量は約54%に低下 |
| retransmit | effective missing **45.7%削減**、54,801 frame 回復 | 有効だが平均 latency 0.750 → 10.003 ms |
| XOR FEC (k=4,r=1) | random drop 10%で effective missing **約73%削減**、usable +875,299 (120 kHz) | 単発欠落に強いが parity 待ち・複数欠落は未回復 |

![adaptive rate の OFF/ON 比較](reports/figures/w09_adaptive_off_on_boxplot.png)

![XOR FECによる欠落回復](reports/figures/readme_fec_effect.png)

![FSMによる障害検知](reports/figures/readme_fsm_recovery.png)
![XOR FECの欠落回復効果](reports/figures/readme_fec_effect.png)

関連データ: [W05 FSM比較](logs/fsm_recovery/w05_compare_baseline/interpretation.md)、[adaptive rate](reports/w09_adaptive_rate_summary.md)、[retransmit](reports/w09_retransmit_summary.md)、[FEC比較](reports/w09_fec_comparison_summary.md)。W09では各方式を単なる実装確認で終わらせず、ON/OFF、同一drop seed、複数trialで raw missing / recovered / effective missing / usable datagram / latency を比較しました。raw CSVは [FEC 1200 Hz](data/w09/fec_comparison/fec_comparison.csv) と [FEC 120 kHz](data/w09/fec_comparison_rate_120000/fec_comparison.csv) で確認できます。

結論は単一の最適解ではなく、**輻輳には rate 制御、履歴に残る欠落には retransmit、ランダム単発欠落には FEC** と故障モードに応じて選択する設計です。

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

## 開発・実験コマンド

### Build And Test

```bash
make all
make test
```

`make test` は以下を実行します。

- `bin/test_framer`
- `bash scripts/test_loopback_metrics.sh`

### Quick Loopback Run

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

### Reproducibility Check

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

### W05 Recovery Matrix

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

### W05 FSM Vs Timeout Compare

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

### How To Read P95 And P99

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

### Reproducibility Criterion

W04 では、3 trial の `latency_p99_ms` それぞれについて `abs(trial_p99 - mean_p99) / mean_p99 * 100` を計算し、すべてが `+/-15%` 以内なら `reproducible=yes` と判定します。`interpretation.md` に結果と簡単な解釈を残します。

変動がしきい値を超えた場合は、まず `avg_pps` と `avg_cpu_pct` のばらつきを確認してください。そこが大きい場合、フレーム処理より先にローカルのスケジューリングやバックグラウンド負荷を疑うべきです。

### Protocol Notes

固定列の意味は [docs/protocol.md](docs/protocol.md) を参照してください。W04 では以下を固定しています。

- `trial_summary` の `latency_p50_ms / latency_p95_ms / latency_p99_ms / latency_max_ms`
- 1 秒統計の `pps / cpu_pct`
- percentile の算出規則は nearest-rank

### CI

GitHub Actions は [.github/workflows/ci.yml](.github/workflows/ci.yml) で `make all` と `make test` を `push` / `pull_request` ごとに実行します。
