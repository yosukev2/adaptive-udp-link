# adaptive-udp-link

UDP ベースの自己回復リンクを C で実装し、性能限界・障害検知・欠落回復・リアルタイム性を実測で評価したプロジェクトです。Raspberry Pi 5 上の UDP loopback、Pi 5–Pico 間の UART 実機通信、Pico 上の FreeRTOS の3つの経路で、**同一条件で再現できる形**に計測基盤を固定しています。

| 検証領域 | 主要な実測結果 |
|----------|----------------|
| Pi 5–Pico UART 実機通信 | 10 packet 全数受理、CRC error 0、payload 完全一致 10/10 |
| Pi 5 loopback の UDP 性能 | 120,000 Hz まで欠落 0。500,000 Hz で missing 2.37%、P99 0.410 ms |
| 障害検知と自己回復 | 3秒停止を FSM が検出・復旧。XOR FEC で effective missing を約73%削減 |
| Pico のリアルタイム性 | FreeRTOS で TX jitter P95/P99 = 0 µs、deadline miss 0 件 |

## 目次

- [使った技術](#使った技術)
- [実装したもの](#実装したもの)
- [検証したことと結果](#検証したことと結果)
  - [1. Pi 5–Pico UART通信・telemetry評価](#1-pi-5pico-uart通信telemetry評価)
  - [2. Pi 5 loopbackでのUDP性能評価・障害検知・自己回復](#2-pi-5-loopbackでのudp性能評価障害検知自己回復)
  - [3. PicoでのBare-metal / FreeRTOSリアルタイム性評価](#3-picoでのbare-metal--freertosリアルタイム性評価)
  - [4. 故障注入とframe integrity](#4-故障注入とframe-integrity)
- [現時点の課題と次にやりたいこと](#現時点の課題と次にやりたいこと)
- [詳細ドキュメント](#詳細ドキュメント)
- [開発の進め方](#開発の進め方)
## 使った技術

| 領域 | 内容 |
|------|------|
| 言語 | C11（実装本体）、Python 3（解析・MCU harness）、Bash（実験自動化） |
| 通信 | UDP / POSIX socket、`SO_RCVBUF`・`SO_SNDBUF` 制御、UART (115200 8N1) |
| プロトコル | 自作frame形式（preamble、seq、length、CRC-32/ISO-HDLC）、feedback packet、XOR FEC |
| 組込み | Raspberry Pi Pico (RP2040)、Pico SDK、FreeRTOS、CMake、USB CDC |
| 計測 | `clock_gettime(CLOCK_MONOTONIC)`、nearest-rank percentile、CPU affinity (`sched_setaffinity`) |
| 環境 | Raspberry Pi 5 / Linux 6.12.75-rpi / gcc 14.2.0、GitHub Actions、Git LFS |

## 実装したもの

外部ライブラリに頼らず、frame処理から適応制御まで C で実装している。

| ファイル | 行数 | 主な内容 |
|----------|-----:|----------|
| `src/rx.c` | 1,923 | 受信ループ、stream buffer と resync、障害検知FSM、latency percentile、feedback送出、重複・回復判定 |
| `src/tx.c` | 1,687 | 周期送信スケジューラ、rate適応制御、再送バッファ、FEC parity生成 |
| `src/frame_v1_wire.c` | 340 | frame v1 の encode / decode、CRC-32 |
| `src/fec_v1_wire.c` | 93 | XOR FEC parity のwire形式 |
| `src/feedback_v1_wire.c` | 86 | feedback packet のwire形式 |
| `src/test_framer.c` | 248 | frame処理の単体テスト |
| `firmware/mcu_uart_link/` | 358 | MCU UART parser（Pico SDK非依存でホストテスト可能）+ Pico応用層 |

主要な実装要素:

- **stream parser**：UARTもUDPもバイト境界が保証されないため、preamble探索・部分受信の保持・不正header検出後のresyncを自前で実装
- **障害検知FSM**：`Normal → Degraded → Recover → Normal` の状態遷移をCSVに記録し、timeout単独方式と比較可能にした
- **percentile算出**：nearest-rank規則を固定し、trial間で比較できる形に統一
- **適応制御**：feedbackで観測したmissing率をもとに、rate制御・再送・XOR FECを実装して個別に効果測定

## 検証したことと結果

### 1. Pi 5–Pico UART通信・telemetry評価

**目的**：Pi 5とPico間のpacket通信を実機で成立させ、ACK、CRC、sequence、MCU内部stateを観測可能にする。loopbackやシミュレーションではなく、実際のMCUを含む経路で計測する。

**実験方法**：packet formatを仕様として先に固定し、PC harness（Python）とMCU parser（C）を独立に実装。Pi 5からUART経由でDATA packetを送信し、PicoはACKを返しつつtelemetryをUSB CDCへ出力する。PC側の送受信ログとMCU内部カウンタを同一trialのCSVとして保存し、突き合わせて判定する。

**結果のまとめ**：10 packetを送信し、**MCU側で全数受理、ACK 10件、payload完全一致10件、CRC error 0、sequence gap 0**を実測。`final_state=RUN`、`pass_fail=PASS`。判定はPC側の受信数ではなくMCU内部の`rx_data_count`を採用している。

#### 1-1. UART packet通信の実機成立

- **やったこと**：packet v1（preamble、version、type、seq、length、CRC-32/ISO-HDLC）を仕様化し、Pi 5–Pico間で10 packetを送受信。
- **現象**：`sent_count=10`に対し`mcu_received_count=10`、`ack_sent_count=10`、`exact_match_count=10`。CRC error、sequence gap、duplicate、buffer overflowはいずれも0。
- **示唆**：UDP loopbackとは別に、実機MCUを含む通信経路を同じCSVベースで評価できる基盤が成立した。

#### 1-2. MCU内部状態とのつき合わせ

- **やったこと**：MCU側で31項目のカウンタ（受信byte数、packet種別ごとの受理数、error種別、buffer使用量、state）を収集し、`summary.csv`へ集計。
- **現象**：`rx_byte_count=321`に対し正味データは320 byte。超過1 byteは電源投入直後にRXラインが浮いていた区間のノイズで、`preamble_miss_count=1`として分離できている。
- **示唆**：「PC側では10件受信」で終わらせず、MCUが実際に何 byte受けて何をどう捨てたかまで追える。ノイズと正常受信を切り分けられる粒度で観測できている。

#### 1-3. 実機bring-upでの故障切り分け

- **やったこと**：初回接続時に通信が成立せず、PC側UART・ジャンパ線・firmware動作・MCUピンを1要素ずつ検証。最終的にPico単体で`GP0`と`GP1`を直結する自己ループバック試験を実施。
- **現象**：PicoはHEARTBEATを11,000 byte以上送出しているのに自身では1 byteも受信せず、**PCも配線も経路に存在しない条件で失敗**したため、故障をPico側ピンに限定できた。`GP12`/`GP13`では同一試験が成立。
- **示唆**：切り分けは「変数を1つずつ消す」ことに尽きる。実機では想定どおりに動かない前提で、前提自体を検証する手段を先に用意しておく必要がある。

この経験から、ビルド時のピン設定をfirmware自身がtelemetry先頭行へ出力するようにした。設定が反映されていないビルドで測定し、誤った結論を出しかけたため。

```text
# uart0 tx=GP12 rx=GP13 baudrate=115200 heartbeat_ms=0
```

**実測条件**：Pi 5 `/dev/ttyAMA2`（`dtoverlay=uart2-pi5`, GPIO4/5）、Pico `GP12`/`GP13`、115200 8N1、payload 16 byte。既定の`/dev/ttyAMA0`とPico `GP0`/`GP1`はこの個体では機能せず、代替ピンを実測で選定した。

関連資料: [実機baseline](data/mcu_uart/m0_baseline_001/)、[bring-up切り分け手順](docs/mcu_uart/link_bringup_triage.md)、[packet仕様](docs/mcu_uart/protocol.md)、[PC harness](scripts/mcu_uart/pc_harness.py)、[MCU parser](firmware/mcu_uart_link/mcu_uart_protocol.c)。

### 2. Pi 5 loopbackでのUDP性能評価・障害検知・自己回復

**目的**：1章で実機間通信の観測系を整えた後、物理ネットワークやMCU処理の影響を分離するため、Pi 5 loopbackでUDP処理・socket queue・スケジューリングの限界を切り分け、再現可能な計測基盤と障害検知を確立する。loopbackの結果は実ネットワークの品質そのものではなく、ホスト内の処理能力を評価するbaselineとして扱う。UART経路とloopbackを接続したend-to-end評価は次の課題とする。

**実験方法**：Pi 5 loopbackで複数trialを実行し、再現性、outage、送信レート、socket buffer、CPU affinityを比較する。

まず正常時の再現性を確認し、次に障害・負荷・処理資源の影響を順に切り分け、最後に欠落への回復策を評価する。

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

### 4. 故障注入とframe integrity

**目的**：正常系の計測が信用できるかを、意図的に壊して確かめる。どの故障がどのカウンタに現れるかを対応づけ、観測系が故障の種類を区別できるかを検証する。

**実験方法**：preamble、length、header、CRC、payload の5箇所に故障を注入し、カウンタの反応パターンを比較。あわせて故障率を 0 / 1 / 5 / 10% と変えて `parse_ok_rate` の推移を測る。

**結果のまとめ**：CRC故障とlength故障は単独カウンタで識別できたが、**preamble故障とheader故障は `trial_summary` だけでは区別できない**ことが判明した。観測系の限界を実測で確認できた点が成果。

#### 4-1. 故障種別ごとのシグネチャ

| 注入対象 | crc_fail | len_invalid | preamble_miss | bad_header | 識別可否 |
|----------|---------:|------------:|--------------:|-----------:|----------|
| preamble | 0 | 0 | 21 | 0 | header と**曖昧** |
| payload_len | 0 | 48 | 48 | 0 | `len_invalid` で識別可 |
| header | 0 | 0 | 48 | 48 | Host補助の `bad_header` が必要 |
| crc | 51 | 0 | 0 | 0 | `crc_fail` で識別可 |
| payload | 46 | 0 | 0 | 0 | `crc_fail` で識別可 |

- **示唆**：preamble破壊とheader破壊はどちらも「preambleを探し直す」挙動になるため、受信側の標準カウンタでは同じに見える。切り分けにはHost側の補助カウンタ `bad_header` が要る。**観測系の設計限界を、想像ではなく実測で特定できた。**

#### 4-2. 故障率とparse成功率

| 条件 | 故障率 | parse_ok_rate | crc_fail |
|------|-------:|--------------:|---------:|
| A_none | 0% | 1.000 | 0 |
| B_low | 1% | 0.991 | 27 |
| C_mid | 5% | 0.949 | 154 |
| D_high | 10% | 0.898 | 305 |

- **示唆**：注入率と `parse_ok_rate` の低下がほぼ線形に対応し、故障が検出漏れなくカウントされていることを確認できた。正常系0件の測定が「本当に0件」だと言える根拠になる。

関連データ: [故障シグネチャ](logs/fault_signatures/fault_signatures.csv)、[frame integrity](logs/frame_integrity/frame_integrity.csv)、[判定の読み方](docs/fault_target_signatures.md)

## 現時点の課題と次にやりたいこと

3つの実験で、ホスト内UDPの限界、欠落回復方式、Pico側の周期処理、Pi 5–Pico UART通信を個別に評価しました。一方で、以下はまだ検証範囲が限定されています。

### 現時点の課題

- **実ネットワークのend-to-end評価が未実施**：Pi 5 loopbackは物理NIC、スイッチ、無線、伝送路の揺らぎを含まないため、実ネットワークで同じ欠落率・tail latencyになるとは限らない。
- **Pi 5–Pico間の統合評価が未完了**：UART通信は実機で成立し、Pico RTOSの評価系も揃っているが、Pi 5のUDP自己回復処理とPicoの実通信処理を一つのend-to-end経路として接続していない。1章のUART linkは10 packetの正常系baselineまでで、故障注入や長時間運転はこれから。
- **FECの回復範囲**：`k=4, r=1`では同一block内の複数欠落やparity欠落を復元できない。
- **再送の鮮度問題**：retransmitは欠落を回復できる一方、古いframeの後着でlatencyが増える。
- **長時間・多環境の再現性**：今回の比較は主に3〜10 trialであり、長時間運転、異なる負荷、複数ボードでの評価はこれからである。

### 次にやりたいこと

1. **Pi 5–Pico end-to-end接続**：UARTまたは実ネットワーク経路で、Pi 5の送信・feedback・自己回復とPicoの受信・telemetryを接続し、通信全体のP99、missing、復旧時間を測る。
2. **実ネットワークでの再検証**：有線・無線、遅延・loss・burst lossを注入し、loopbackで得た限界値との差分を測定する。
3. **適応制御の統合**：missing率、queue backlog、latencyをfeedbackに集約し、rate制御・再送・FECを状況に応じて切り替える。
4. **FECと再送の拡張**：複数parity、blockサイズ変更、burst lossへの対応を比較し、回復率と冗長量の最適点を探る。
5. **リアルタイム経路の実測**：PicoのFreeRTOS task jitterだけでなく、実際のUDP/UART送受信、driver、buffer、queueを含むend-to-end latencyを測る。
## 詳細ドキュメント

| 内容 | 場所 |
|------|------|
| 実験レポート・グラフ | [`reports/`](reports/) |
| 生データ・実機baseline | [`data/`](data/) |
| UDP frame仕様 | [`docs/protocol.md`](docs/protocol.md) |
| MCU UART packet仕様 | [`docs/mcu_uart/protocol.md`](docs/mcu_uart/protocol.md) |
| XOR FEC設計 | [`docs/w09/xor_fec_design.md`](docs/w09/xor_fec_design.md) |
| 再送設計 | [`docs/w09/retransmit_design.md`](docs/w09/retransmit_design.md) |
| RTOS task構成 | [`docs/w07_task_architecture.md`](docs/w07_task_architecture.md) |
| 故障シグネチャ判定 | [`docs/fault_target_signatures.md`](docs/fault_target_signatures.md) |
| **ビルド・実験手順** | [`docs/runbook.md`](docs/runbook.md) |

## 開発の進め方

個人開発だが、再現性を保つため以下を固定している。

- **CI**：[GitHub Actions](.github/workflows/ci.yml) で `make all` と `make test` を push / PR ごとに実行
- **issue駆動**：設計判断と受け入れ条件を [`docs/issues/`](docs/issues/) に残してから着手
- **PR運用**：[`docs/pr_operation.md`](docs/pr_operation.md) に手順を固定
- **コーディング規約**：整数printf formatの方針を [`docs/c_integer_printf_format_policy.md`](docs/c_integer_printf_format_policy.md) に明文化（`PRI*` macroを使わず明示cast + 明示format）
- **大容量データ**：計測CSVは Git LFS で管理し、リポジトリ本体を軽く保つ
- **ボード選定**：比較検討の経緯を [`docs/board_selection.md`](docs/board_selection.md) に記録
