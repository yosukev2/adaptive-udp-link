# repo
$repo = "yosukev2/adaptive-udp-link"

# milestones
$milestones = @(
  @{
    title = "M0 - MCU UART: 計測基盤・検証基準"
    description = @'
## 目的

実装の効果をデータで判定できるように、packet仕様、ログ仕様、実験手順、判定基準を固定する。

## Issue steps

- [ ] M0-01: リポジトリ構成と build / flash / run 手順を整備する
- [ ] M0-02: packet format v1 を定義する
- [ ] M0-03: telemetry counter 定義を作る
- [ ] M0-04: PC側 Python test harness を作る
- [ ] M0-05: CSV log schema を定義する
- [ ] M0-06: summary 生成スクリプトを作る
- [ ] M0-07: 正常通信 baseline を実機で取得し、判定基準を決める

## 出すべきデータ

- protocol.md
- telemetry_schema.md
- run_metadata.md
- pc_tx_log.csv
- pc_rx_log.csv
- mcu_telemetry.csv
- summary.csv

## 成功判定

- sent_count / received_count / exact_match_count / crc_error_count / seq_gap_count / recovered_count / unrecovered_count が summary で確認できる
- baudrate、payload長、packet数、異常注入条件、firmware version が metadata に残る
- 同じ条件で再実行できる

## 実験方法

- PCから10 packetだけ送信し、MCUがtelemetryを返す
- 異常注入はまだ行わない
- summary.csvに必要な列がすべて出るか確認する
'@
  },
  @{
    title = "M1 - MCU UART: 正常系 packet 通信"
    description = @'
## 目的

PC↔MCUで、意味ある文字列payloadをpacketとして送り、壊れず完全一致で受信できることを確認する。

## Issue steps

- [ ] M1-01: PC Python ↔ MCU UART の疎通確認
- [ ] M1-02: preamble / length / seq / payload / CRC 付き packet 生成を実装する
- [ ] M1-03: MCU側 packet parser を実装する
- [ ] M1-04: CRC検証を実装する
- [ ] M1-05: 意味ある文字列payloadの exact match 確認を追加する
- [ ] M1-06: 正常系1000 packet実機検証を行う
- [ ] M1-07: 正常系ログから packet loss、CRC error、exact match率を確認する

## 出すべきデータ

- sent_count
- parsed_packets
- crc_ok_count
- crc_error_count
- exact_match_count
- exact_match_rate
- seq_gap_count
- parser_resync_count

## 成功判定

- 正常系1000 packet × 3 trialで exact_match_rate = 100%
- crc_error_count = 0
- seq_gap_count = 0
- MCUが途中停止しない

## 実験方法

- PCから HELLO_LINK_TEST_SEQ_000001 のようなpayloadを1000件送る
- 異常注入なし
- baudrateは最初115200bpsに固定
- 3 trial実行して完全一致を確認する
'@
  },
  @{
    title = "M2 - MCU UART: 異常検出"
    description = @'
## 目的

壊れたpacket、欠落packet、重複packet、順序ずれをMCU側で検出できることを確認する。

## Issue steps

- [ ] M2-01: sequence number と seq gap 検出を追加する
- [ ] M2-02: duplicate packet 検出を追加する
- [ ] M2-03: out-of-order 検出を追加する
- [ ] M2-04: PC側に drop 注入を追加する
- [ ] M2-05: PC側に duplicate 注入を追加する
- [ ] M2-06: PC側に out-of-order 注入を追加する
- [ ] M2-07: PC側に CRC破壊注入を追加する
- [ ] M2-08: CRC破壊packetをMCU側で破棄する処理を確認する
- [ ] M2-09: drop / duplicate / out-of-order / CRC破壊を実機で注入し、検出率を確認する
- [ ] M2-10: 異常検出ログから誤検出・未検出がないか確認する

## 出すべきデータ

- crc_error_count
- seq_gap_count
- duplicate_count
- out_of_order_count
- accepted_packet_count
- rejected_packet_count
- false_accept_count
- injected_fault_count
- detected_fault_count

## 成功判定

- CRC破壊packetを受理しない
- false_accept_count = 0
- drop注入数とseq_gap_countが概ね一致する
- duplicate packetを二重計上しない
- out-of-orderを検出できる

## 実験方法

- CRC corrupt 10%: payloadまたはCRCをPC側で破壊する
- drop 5%: PC側でpacketを送らない
- duplicate 5%: 同じseqを再送する
- out-of-order: 一部packetの送信順を入れ替える
- 各条件1000 packet × 3 trialで実行する
- 注入ログとMCU telemetryを突き合わせる
'@
  },
  @{
    title = "M3 - MCU UART: heartbeat・timeout・状態遷移"
    description = @'
## 目的

通信が途切れたとき、MCUがACTIVEのまま固まらず、DEGRADED / LINK_LOST / RECOVERINGへ遷移できることを確認する。

## Issue steps

- [ ] M3-01: heartbeat packet形式を定義する
- [ ] M3-02: PC側heartbeat送信を実装する
- [ ] M3-03: MCU側heartbeat受信処理を実装する
- [ ] M3-04: heartbeat timeout検出を実装する
- [ ] M3-05: IDLE / ACQUIRING / ACTIVE / DEGRADED / RECOVERING の state machine v1 を実装する
- [ ] M3-06: 異常条件ごとの状態遷移ルールを定義する
- [ ] M3-07: state_transition_log.csv を出力する
- [ ] M3-08: heartbeat停止を実機で注入し、ACTIVE→DEGRADED/LINK_LOST遷移を確認する
- [ ] M3-09: heartbeat再開後にACTIVEへ復帰できるか確認する
- [ ] M3-10: 状態遷移ログから想定外遷移がないか確認する

## 出すべきデータ

- state_transition_log.csv
- current_state
- heartbeat_rx_count
- heartbeat_timeout_count
- time_to_degraded_ms
- time_to_recovering_ms
- time_to_active_ms
- recovery_success_count
- unexpected_transition_count

## 成功判定

- 正常heartbeat中はACTIVEを維持する
- heartbeat停止後、指定timeout以内にDEGRADEDまたはLINK_LOSTへ遷移する
- heartbeat再開後、RECOVERINGを経てACTIVEへ戻る
- 想定外の直接遷移がない

## 実験方法

- PC側からheartbeatを100ms周期で送る
- 5秒正常通信してACTIVE確認
- 2秒heartbeat停止
- MCUがDEGRADED/LINK_LOSTへ遷移するか確認
- heartbeat再開後にACTIVEへ復帰するか確認
- 3 trial実行して遷移時刻をsummary化する
'@
  },
  @{
    title = "M4 - MCU UART: 固定buffer・メモリ制約"
    description = @'
## 目的

mallocなしの固定長bufferで受信・履歴・再送候補を管理し、overflowやbuffer missをデータで確認できるようにする。

## Issue steps

- [ ] M4-01: mallocなし方針とメモリ使用方針を定義する
- [ ] M4-02: 固定長RX ring bufferを実装する
- [ ] M4-03: packet history bufferを実装する
- [ ] M4-04: rx_buffer_max_usedを計測する
- [ ] M4-05: history_buffer_max_usedを計測する
- [ ] M4-06: overflow_countを追加する
- [ ] M4-07: buffer_miss_countを追加する
- [ ] M4-08: burst送信でoverflowを実機発生させる
- [ ] M4-09: bufferサイズ別にdrop / overflow / recovery率を比較する
- [ ] M4-10: 固定buffer設計が効いているか、メモリ上限と欠落率の関係を確認する

## 出すべきデータ

- rx_buffer_capacity
- rx_buffer_max_used
- history_buffer_capacity
- history_buffer_max_used
- overflow_count
- buffer_miss_count
- dropped_due_to_overflow_count
- recovered_count
- unrecovered_count

## 成功判定

- 通常rateでは overflow_count = 0
- burst条件では overflow_count が増える
- bufferサイズを増やすと overflow_count が下がる
- bufferに残っているpacketは再送可能
- bufferから消えたpacketは buffer_miss として記録される
- mallocなしで動作する

## 実験方法

- 通常送信: 1000 packetを一定間隔で送る
- burst送信: 短時間に100 packetを連続送信する
- buffer sizeを小・中・大で切り替える
- overflow_count、max_used、recovered_countを比較する
'@
  },
  @{
    title = "M5 - MCU UART: 再送による完全復元"
    description = @'
## 目的

packet dropが起きても、ACK/NACKまたは再送要求で意味ある文字列payloadを完全復元できることを確認する。

## Issue steps

- [ ] M5-01: ACK / NACK packet形式を定義する
- [ ] M5-02: MCU側でseq gap時にNACKまたは再送要求を出す
- [ ] M5-03: PC側で再送要求を受け取り、該当packetを再送する
- [ ] M5-04: TX history bufferから再送する処理を実装する
- [ ] M5-05: retransmit_countを記録する
- [ ] M5-06: recovered_count / unrecovered_countを記録する
- [ ] M5-07: exact_match_after_recoveryを確認する
- [ ] M5-08: 1 packet dropの再送復元を実機で確認する
- [ ] M5-09: 複数dropやbuffer不足時の復元限界を確認する
- [ ] M5-10: 再送によるlatency増加を記録する

## 出すべきデータ

- dropped_by_injection_count
- retransmit_request_count
- retransmit_sent_count
- recovered_count
- unrecovered_count
- exact_match_after_recovery_count
- recovery_rate
- recovery_latency_ms
- buffer_miss_count

## 成功判定

- single packet drop条件でrecovery_rateが高い、理想は100%
- recovered payloadが元の文字列と完全一致する
- buffer内に残るpacketは再送で復元できる
- buffer外のpacketはbuffer_missとして復元不可扱いになる
- 再送によりlatencyが増えることも記録できる

## 実験方法

- 1000 packet中、単発dropを10回注入する
- MCUがseq gapを検出してNACKまたは再送要求を出す
- PCが該当seqを再送する
- MCU側でpayload完全一致を確認する
- drop間隔を短くした条件、bufferサイズを小さくした条件も実行する
- recovery_rateとrecovery_latencyを比較する
'@
  },
  @{
    title = "M6 - MCU UART: 復旧失敗・SAFE遷移"
    description = @'
## 目的

復旧できない異常を無理に継続せず、SAFEへ落とす設計ができていることを確認する。

## Issue steps

- [ ] M6-01: retry上限を定義する
- [ ] M6-02: SAFE状態を追加する
- [ ] M6-03: SAFE遷移条件を定義する
- [ ] M6-04: last_error_codeを定義する
- [ ] M6-05: RECOVERING失敗時にSAFEへ遷移する処理を実装する
- [ ] M6-06: CRC error多発時のSAFE遷移を実装する
- [ ] M6-07: heartbeat長時間停止時のSAFE遷移を実装する
- [ ] M6-08: retry上限超過時のSAFE遷移を実装する
- [ ] M6-09: MCU reset後の再同期処理を実装する
- [ ] M6-10: 復旧成功条件と復旧失敗条件を実機で検証する
- [ ] M6-11: SAFE遷移が過剰でも不足でもないかログから確認する

## 出すべきデータ

- retry_count
- retry_limit_exceeded_count
- safe_count
- last_error_code
- time_to_safe_ms
- recovery_success_count
- recovery_fail_count
- reset_count
- resync_success_count
- false_safe_count

## 成功判定

- 一時的なdropではACTIVEへ復帰する
- 連続dropやheartbeat長時間停止ではSAFEへ遷移する
- retry上限超過時に無限ループしない
- SAFE遷移理由がlast_error_codeで分かる
- MCU reset後にIDLE/ACQUIRINGから再同期できる
- 正常系でSAFEが過剰発火しない

## 実験方法

- 一時異常: drop 5%を短時間だけ入れる → ACTIVE復帰を確認
- 継続異常: drop 100%またはheartbeat停止を長時間入れる → SAFE遷移を確認
- CRC corrupt 50%を継続注入 → retry上限後SAFEを確認
- MCU resetボタンまたはsoftware reset後、PCと再同期できるか確認
- state_transition_logから遷移順と遷移時間を確認する
'@
  },
  @{
    title = "M7 - MCU UART: 最終実機評価・レポート"
    description = @'
## 目的

正常系、異常検出、復旧成功、復旧失敗、buffer限界、SAFE遷移を横断比較し、実装の効果と限界を説明できる最終レポートにする。

## Issue steps

- [ ] M7-01: 最終test matrixを定義する
- [ ] M7-02: 正常系testを3 trial以上実行する
- [ ] M7-03: CRC破壊testを3 trial以上実行する
- [ ] M7-04: drop / duplicate / out-of-order testを3 trial以上実行する
- [ ] M7-05: heartbeat停止testを3 trial以上実行する
- [ ] M7-06: retransmit recovery testを3 trial以上実行する
- [ ] M7-07: burst / buffer overflow testを3 trial以上実行する
- [ ] M7-08: SAFE遷移testを3 trial以上実行する
- [ ] M7-09: reset / resync testを3 trial以上実行する
- [ ] M7-10: final_test_matrix.csvを作成する
- [ ] M7-11: normal_summary.csv / fault_detection_summary.csv / recovery_summary.csv / buffer_limit_summary.csv / safe_transition_summary.csvを作成する
- [ ] M7-12: final_summary.mdに効果・限界・次の課題をまとめる

## 出すべきデータ

- final_test_matrix.csv
- final_summary.md
- normal_summary.csv
- fault_detection_summary.csv
- recovery_summary.csv
- buffer_limit_summary.csv
- safe_transition_summary.csv
- state_transition_log.csv

## 成功判定

- どの異常を検出できるかが表で分かる
- どの異常を復旧できるかが表で分かる
- どの条件で復旧できないかが表で分かる
- bufferサイズや再送の効果がデータで分かる
- SAFE遷移条件が過剰でも不足でもないことを説明できる
- 実装の限界を明記できている

## 実験方法

- 各testを3 trial以上実行する
- packet数、payload形式、baudrateを固定する
- 正常系、CRC破壊、drop、duplicate、heartbeat停止、burst、buffer不足、recovery失敗、resetを横断比較する
- 効果あり、効果なし、限界をfinal_summaryに書く
'@
  }
)

# existing milestones
$existing = gh api "repos/$repo/milestones?state=all&per_page=100" | ConvertFrom-Json
$existingTitles = @($existing | ForEach-Object { $_.title })

foreach ($m in $milestones) {
  if ($existingTitles -contains $m.title) {
    Write-Host "SKIP existing milestone: $($m.title)"
    continue
  }

  $payload = @{
    title = $m.title
    description = $m.description
    state = "open"
  } | ConvertTo-Json -Depth 10

  Write-Host "CREATE milestone: $($m.title)"
  $payload | gh api -X POST "repos/$repo/milestones" --input -
}