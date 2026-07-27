# adaptive-udp-link

UDP ベースの自己回復リンク基盤を段階的に実装しながら、観測・耐障害化・適応制御まで積み上げる C プロジェクトです。W04 では「同一条件での計測結果を再現できること」を重視し、`trial_summary`、1 秒統計、再現性チェック、CI を固定しています。
## 目次

- [3つの主要成果](#3つの主要成果)
  - [Pi 5–Pico UART通信・telemetry評価](#1-pi-5pico-uart通信telemetry評価)
  - [Pi 5 loopbackでのUDP性能評価・障害検知・自己回復](#2-pi-5-loopbackでのudp性能評価障害検知自己回復)
  - [PicoでのBare-metal / FreeRTOSリアルタイム性評価](#3-picoでのbare-metal--freertosリアルタイム性評価)
- [現時点の課題と次にやりたいこと](#現時点の課題と次にやりたいこと)
- [成果物と再現方法](#成果物と再現方法)
- [開発・実験コマンド](#開発実験コマンド)
- [Repository Layout](#repository-layout)
- [Prerequisites](#prerequisites)
## 3つの主要成果

### 1. Pi 5–Pico UART通信・telemetry評価

**目的**：Pi 5とPico間のpacket通信を実機構成で確認し、ACK/NACK、CRC、sequence、telemetryを観測可能にする。

**実験方法**：Pi 5側のPC harnessからUARTでDATA packetを送信し、PicoからACK/NACKとtelemetryを受信。送受信ログをCSVに保存し、summaryを生成する。

**結果のまとめ**：UART packet format、PC harness、Pico firmware、telemetry schema、summary生成の一連の評価系を整備した。sample baselineではCRC error 0、sequence gap 0を確認できる構成になっている。

#### 1-1. UART packet通信

- **やったこと**：DATA packetをPi 5からPicoへ送信し、Pico側のACK/NACKを記録。
- **現象**：PC TX/RXログとMCU telemetryをtrial単位で保存できる。
- **示唆**：UDP loopbackとは別に、実機MCUを含む通信経路を同じCSVベースで評価できる。

#### 1-2. MCU telemetryとsummary

- **やったこと**：CRC error、sequence gap、送受信数、MCU stateをtelemetryとして収集し、summary.csvに集計。
- **現象**：sample baselineではCRC error 0、sequence gap 0、正常状態を確認。
- **示唆**：通信結果だけでなく、MCU内部状態と通信品質を対応付けて分析できる。

関連資料: [UART demo](docs/mcu_uart_link_demo.md)、[PC harness](scripts/mcu_uart/pc_harness.py)、[sample baseline](data/mcu_uart/sample_baseline/)。

### 2. Pi 5 loopbackでのUDP性能評価・障害検知・自己回復

**目的**：1章で実機間通信の観測系を整えた後、物理ネットワークやMCU処理の影響を分離するため、Pi 5 loopbackでUDP処理・socket queue・スケジューリングの限界を切り分け、再現可能な計測基盤と障害検知を確立する。loopbackの結果は実ネットワークの品質そのものではなく、ホスト内の処理能力を評価するbaselineとして扱う。UART経路とloopbackを接続したend-to-end評価は次の課題とする。

**実験方法**：Pi 5 loopbackで複数trialを実行し、再現性、outage、送信レート、socket buffer、CPU affinityを比較する。

**結果のまとめ**：120,000 Hzまでは欠落なし。3秒outageではFSMが復旧状態まで検出。bufferやaffinityはdrop・tail latency・再現性に影響した。

#### 2-1. 再現性評価

- **やったこと**：Pi 5 loopbackで送信レート120 frame/s、payload 64 bytes、送信5秒・受信7秒の条件を固定し、3 trialを実行。送受信数、sequence gap、CRC error、parse error、P50/P95/P99、pps、CPU使用率を比較。
- **現象**：3 trialとも期待送信数600 frameに対するsequence gap、CRC error、parse errorは0件。P99平均は0.360 ms、最大偏差6.94%、再現性判定は `yes`。
- **示唆**：この実験は負荷限界ではなく、エラーが発生しないbaseline条件で計測系の再現性を確認したもの。負荷限界とgap発生条件は2-3のrate sweepで別途検証した。

関連データ: [W04再現性CSV](logs/reproducibility/w04_baseline_20260429/reproducibility_check.csv)

#### 2-2. 障害検知FSMとtimeout-only比較

- **やったこと**：0.5秒、1秒、3秒の通信停止を再現し、FSMとtimeout-onlyを比較。
- **現象**：0.5/1秒停止は誤検知なし。3秒停止では `Normal → Degraded → Recover → Normal` を検出。FSM復旧完了7,667 ms、timeout-only 8,000 ms。
- **示唆**：短時間の揺らぎと長時間障害を区別し、復旧状態を明示できる。

![FSM状態遷移](reports/figures/readme_fsm_recovery.png)

#### 2-3. 送信レート sweep

- **やったこと**：50〜1,000,000 Hzで送信し、missing、CPU、P95/P99/max latencyを測定。
- **現象**：120,000 Hzまでは欠落なし。140,000 Hzからgap。500,000 Hzではmissing率2.37%、P99 latency 0.410 ms。
- **示唆**：限界はlatency悪化より先にdropとして現れるため、missingとtail latencyを同時に見る必要がある。

![送信レートと欠落](reports/figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_missing_delta_total_avg.png)

#### 2-4. socket buffer比較

- **やったこと**：socket bufferサイズを変え、dropとlatencyを比較。
- **現象**：buffer増加でdropは減る一方、queue滞留によりP95/P99/max latencyが増える条件を確認。
- **示唆**：drop最小化とtail latency最小化はトレードオフ。

![socket bufferとlatency](reports/figures/w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_p99_latency_ms_avg.png)

#### 2-5. CPU affinity比較

- **やったこと**：TX/RXを同一core、別coreに固定して比較。
- **現象**：低〜中レートでは末尾latency outlierの切り分けに有効。高レートではcore分離後も飽和dropが残った。
- **示唆**：affinityは高速化の万能策ではなく、再現性向上と原因分離の手段。

![CPU affinity比較](reports/figures/w08_cpu_affinity_rate_500000_rxpin_x_txpin_max_latency_ms_avg.png)


#### 2-6. UDP自己回復機構

**目的**：欠落原因ごとに回復方式を選び、missing削減とlatency・throughputのトレードオフを評価する。

**実験方法**：feedback packetを追加し、Adaptive Rate、Retransmit、XOR FECを実装。ON/OFF、同一drop seed、複数trialで比較する。

**結果のまとめ**：Adaptive Rateは小幅改善、Retransmitは欠落回復と引き換えにlatency増加、XOR FECはrandom dropに対して約73%のeffective missing削減を確認した。

##### 2-6-1. Adaptive Rate

- **やったこと**：feedbackでmissingを検出し、送信rateを動的に下げる制御を実装。
- **現象**：missingは2.8919%から2.7661%へ改善。一方、受信総量は約54%に低下。
- **示唆**：最大throughputではなく、輻輳時の退避機構として適する。

![Adaptive Rate ON/OFF](reports/figures/w09_adaptive_off_on_boxplot.png)

##### 2-6-2. Retransmit

- **やったこと**：feedbackで欠落範囲を通知し、bounded bufferから再送。
- **現象**：effective missingを45.7%削減し、54,801 frameを回復。平均latencyは0.750 msから10.003 msへ増加。
- **示唆**：完全性を高められるが、古いframeの後着によるlatency増加を許容する必要がある。

関連データ: [Retransmitレポート](reports/w09_retransmit_summary.md)

##### 2-6-3. XOR FEC

- **やったこと**：k=4、r=1のXOR parityを追加し、random drop 10%条件でFEC ON/OFFを同一seedで比較。
- **現象**：effective missingを約73%削減。120 kHzではusable datagramが875,299件増加。
- **示唆**：単発datagram欠落には強いが、同一block内の複数欠落やparity欠落は回復できない。

![XOR FEC回復効果](reports/figures/readme_fec_effect.png)

##### 2-6-4. 3方式の比較

- **やったこと**：raw missing、recovered、effective missing、usable datagram、latencyを方式間で比較。
- **現象**：3方式すべてで欠落改善を確認したが、Adaptive Rateは受信量低下、Retransmitはlatency増加、FECはparity待ちと未回復欠落が残った。
- **示唆**：輻輳にはAdaptive Rate、履歴欠落にはRetransmit、ランダム単発欠落にはFECという役割分担が妥当。

比較データ: [W09総合サマリー](reports/w09_missing_improvement_final_summary.md)

### 3. PicoでのBare-metal / FreeRTOSリアルタイム性評価

**目的**：1章でPi 5–Pico間の通信観測系を作り、2章でPi 5側のUDP欠落・queue飽和・自己回復を確認した。3章では、その通信相手となるPico側が周期送信を安定して実行できるかを、Bare-metalとFreeRTOSで検証する。特に、RX処理やtask間通信がTX周期性へ与える影響を明らかにする。

**実験方法**：Picoで同一RX workloadをBare-metalとFreeRTOSで各3回実行し、TX jitter、queue hand-off、deadline missを測定。Pi 5 Linux user-space loopとも比較する。

**結果のまとめ**：FreeRTOSではTX jitter P95/P99が0 µs、queue hand-off P95が8 µs、deadline missが0件。周期処理の分離効果を確認した。

#### 3-1. Bare-metal周期処理

- **やったこと**：単一loop内でRX相当処理と周期TXイベントを実行。
- **現象**：TX jitterのP95/P99は1,839 µs。
- **示唆**：RX workloadの実行時間が周期TXのタイミングに影響した。

![Bare-metal jitter](reports/figures/w07_baremetal_abs_jitter_distribution.svg)

#### 3-2. FreeRTOS task分離

- **やったこと**：TX、STATE、RXをtaskに分離し、優先度をTX=3、STATE=2、RX=1に設定。
- **現象**：TX jitterのP95/P99は0 µs、deadline missは0件。
- **示唆**：高優先度TX taskにより周期処理をRX負荷から保護できた。

![FreeRTOS jitter](reports/figures/w07_freertos_abs_jitter_distribution.svg)

#### 3-3. FreeRTOS queue hand-off

- **やったこと**：TX taskからSTATE taskへqueueでイベントを渡し、送受信遅延を測定。
- **現象**：queue hand-off P95/P99は8 µs、最大80 µs。3,000イベントを全件受信し、send failureとmissing receiveは0件。
- **示唆**：task分割によるqueue通信は、今回の条件では許容可能なオーバーヘッドだった。

![FreeRTOS queue latency](reports/figures/w07_freertos_queue_latency_distribution.svg)

#### 3-4. Linuxを比較基準にしたPico周期jitter評価

- **やったこと**：Pi 5 Linux user-space loopを比較基準として、Pico hardware-timer loopの周期jitterを比較。
- **現象**：LinuxのP99 jitterは5 µs、Picoは0 µs。最大値はLinux 55 µs、Pico 2 µs。
- **示唆**：hardware timerは送信側のスケジューリングノイズを抑える基準として有効。

![Linux / Pico jitter比較](reports/figures/readme_rtos_jitter.png)

## 現時点の課題と次にやりたいこと

3つの実験で、ホスト内UDPの限界、欠落回復方式、Pico側の周期処理、Pi 5–Pico UART通信を個別に評価しました。一方で、以下はまだ検証範囲が限定されています。

### 現時点の課題

- **実ネットワークのend-to-end評価が未実施**：Pi 5 loopbackは物理NIC、スイッチ、無線、伝送路の揺らぎを含まないため、実ネットワークで同じ欠落率・tail latencyになるとは限らない。
- **Pi 5–Pico間の統合評価が未完了**：UART通信とPico RTOSの評価系はあるが、Pi 5のUDP自己回復処理とPicoの実通信処理を一つのend-to-end経路として接続していない。
- **FECの回復範囲**：`k=4, r=1`では同一block内の複数欠落やparity欠落を復元できない。
- **再送の鮮度問題**：retransmitは欠落を回復できる一方、古いframeの後着でlatencyが増える。
- **長時間・多環境の再現性**：今回の比較は主に3〜10 trialであり、長時間運転、異なる負荷、複数ボードでの評価はこれからである。

### 次にやりたいこと

1. **Pi 5–Pico end-to-end接続**：UARTまたは実ネットワーク経路で、Pi 5の送信・feedback・自己回復とPicoの受信・telemetryを接続し、通信全体のP99、missing、復旧時間を測る。
2. **実ネットワークでの再検証**：有線・無線、遅延・loss・burst lossを注入し、loopbackで得た限界値との差分を測定する。
3. **適応制御の統合**：missing率、queue backlog、latencyをfeedbackに集約し、rate制御・再送・FECを状況に応じて切り替える。
4. **FECと再送の拡張**：複数parity、blockサイズ変更、burst lossへの対応を比較し、回復率と冗長量の最適点を探る。
5. **リアルタイム経路の実測**：PicoのFreeRTOS task jitterだけでなく、実際のUDP/UART送受信、driver、buffer、queueを含むend-to-end latencyを測る。
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
