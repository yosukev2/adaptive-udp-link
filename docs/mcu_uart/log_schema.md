# MCU UART CSV Log Schema

## 目的

MCU UART 実験では、PC 送信ログ、PC 受信ログ、MCU telemetry、summary を同じ列構成で保存する。これにより、正常系、CRC error、seq gap、buffer overflow、復旧、SAFE 遷移を CSV だけで比較できる。

## 共通ルール

- 文字コードは UTF-8。
- 1 行目は header。
- 時刻は `*_ns` が nanosecond、`*_ms` が millisecond。
- `trial_id` は 1 回の実験ディレクトリ名と一致させる。
- 実機未接続 dry-run は `hardware_observed=false`、`baseline_status=template_only` とする。
- 実測 baseline は `hardware_observed=true`、`baseline_status=hardware_run` とする。

## run_metadata.csv

| 列 | 意味 | 単位/例 |
|----|------|---------|
| `trial_id` | 試行 ID | `m0_baseline_001` |
| `test_name` | 試験名 | `m0_baseline_10pkt` |
| `firmware_version` | MCU firmware version または commit | `unknown` |
| `baudrate` | UART baudrate | bit/s |
| `packet_count` | 送信予定 packet 数 | count |
| `payload_len` | DATA payload 長 | bytes |
| `port` | PC 側 serial port | `/dev/ttyUSB0`, `COM5` |
| `dry_run` | dry-run か | `true`/`false` |
| `hardware_observed` | MCU 実機応答を観測したか | `true`/`false` |
| `baseline_status` | baseline 状態 | `template_only`, `hardware_run` |
| `created_wall_ns` | metadata 生成時刻 | ns |

## pc_tx_log.csv

| 列 | 意味 | 単位/例 |
|----|------|---------|
| `trial_id` | 試行 ID | string |
| `seq` | DATA sequence number | count |
| `packet_type` | packet type 名 | `DATA` |
| `payload_len` | payload 長 | bytes |
| `tx_wall_ns` | PC wall clock 送信時刻 | ns |
| `tx_mono_ns` | PC monotonic 送信時刻 | ns |
| `payload_text` | printable payload 表現 | string |
| `packet_hex` | wire bytes の hex dump | lowercase hex |
| `crc32` | packet CRC | `0x12345678` |
| `dry_run` | dry-run か | `true`/`false` |
| `port` | serial port | string |
| `baudrate` | UART baudrate | bit/s |

## pc_rx_log.csv

| 列 | 意味 | 単位/例 |
|----|------|---------|
| `trial_id` | 試行 ID | string |
| `seq` | 受信 packet sequence number | count |
| `packet_type` | packet type 名 | `ACK`, `TELEMETRY` |
| `payload_len` | payload 長 | bytes |
| `rx_wall_ns` | PC wall clock 受信時刻 | ns |
| `rx_mono_ns` | PC monotonic 受信時刻 | ns |
| `payload_text` | printable payload 表現 | string |
| `packet_hex` | wire bytes の hex dump | lowercase hex |
| `crc32` | packet CRC | `0x12345678` |
| `crc_ok` | CRC 検証結果 | `true`/`false` |
| `parse_error` | parse error 内容 | empty if valid |
| `port` | serial port | string |
| `baudrate` | UART baudrate | bit/s |

## mcu_telemetry.csv

MCU firmware は最低限、以下の列を snapshot として出す。

| 列 | 意味 | 単位/例 |
|----|------|---------|
| `trial_id` | 試行 ID | string |
| `mono_ms` | MCU monotonic time | ms |
| `state` | Link state | `IDLE`, `RUN`, `DEGRADED`, `RECOVER`, `SAFE` |
| `last_error_code` | 最新 error code | integer |
| `last_seq` | 最後に受理した seq | count |
| `expected_seq` | 次に期待する seq | count |
| `rx_byte_count` | UART 受信 byte 数 | bytes |
| `rx_packet_count` | 正常 packet 受理数 | count |
| `rx_data_count` | 正常 DATA packet 受理数 | count |
| `tx_packet_count` | MCU 送信 packet 数 | count |
| `ack_sent_count` | ACK 送信数 | count |
| `nack_sent_count` | NACK 送信数 | count |
| `telemetry_sent_count` | telemetry 送信数 | count |
| `heartbeat_sent_count` | heartbeat 送信数 | count |
| `crc_error_count` | CRC error 数 | count |
| `seq_gap_count` | sequence gap 推定数 | count |
| `duplicate_count` | duplicate 数 | count |
| `timeout_count` | receive/parser timeout 数 | count |
| `preamble_miss_count` | preamble 探索で捨てた byte/event 数 | count |
| `invalid_version_count` | version 不正数 | count |
| `invalid_type_count` | type 不正数 | count |
| `length_error_count` | length 不正数 | count |
| `rx_buffer_overflow_count` | RX buffer overflow 数 | count |
| `rx_buffer_miss_count` | RX buffer miss 数 | count |
| `recover_enter_count` | RECOVER 進入数 | count |
| `recovered_count` | 復旧成功数 | count |
| `unrecovered_count` | 復旧失敗数 | count |
| `safe_enter_count` | SAFE 進入数 | count |
| `reset_count` | reset 観測数 | count |
| `rx_buffer_used` | 現在の RX buffer 使用量 | bytes |
| `rx_buffer_capacity` | RX buffer 容量 | bytes |

## summary.csv

| 列 | 意味 | 判定での使い方 |
|----|------|----------------|
| `trial_id` | 試行 ID | run 識別 |
| `test_name` | 試験名 | 条件比較 |
| `firmware_version` | firmware version | 実装比較 |
| `baudrate` | UART baudrate | 条件比較 |
| `packet_count_configured` | 送信予定数 | `sent_count` と比較 |
| `payload_len_configured` | payload 長 | 条件比較 |
| `sent_count` | PC 送信 packet 数 | baseline では 10 |
| `pc_received_count` | PC が MCU から受信した有効 packet 数 | ACK/telemetry 確認 |
| `mcu_received_count` | MCU telemetry 上の DATA 受理数 | 実機 baseline の主指標 |
| `received_count` | summary が採用する受信数 | telemetry があれば MCU 値、なければ PC RX 値 |
| `exact_match_count` | PC TX と PC RX payload 完全一致数 | loopback/echo 時の確認 |
| `crc_error_count` | CRC error 数 | baseline では 0 |
| `seq_gap_count` | seq gap 数 | baseline では 0 |
| `duplicate_count` | duplicate 数 | baseline では 0 |
| `overflow_count` | RX buffer overflow 数 | baseline では 0 |
| `buffer_miss_count` | RX buffer miss 数 | baseline では 0 |
| `recovered_count` | 復旧成功数 | 異常注入時の確認 |
| `unrecovered_count` | 復旧失敗数 | baseline では 0 |
| `safe_enter_count` | SAFE 進入数 | baseline では 0 |
| `reset_count` | reset 観測数 | 予期しない reset 検出 |
| `final_state` | 最終 MCU state | baseline では `RUN` または `IDLE` |
| `last_error_code` | 最新 error code | baseline では `0` |
| `hardware_observed` | 実機を観測したか | `false` は実測合格にしない |
| `baseline_status` | baseline 状態 | `template_only` は手順確認のみ |
| `pass_fail` | 判定 | `PASS`, `FAIL`, `TEMPLATE_ONLY` |
| `note` | 補足 | 手動メモ |

## baseline 判定基準

実機 baseline の `PASS` 条件:

- `hardware_observed=true`
- `sent_count=10`
- `received_count=10`
- `crc_error_count=0`
- `seq_gap_count=0`
- `duplicate_count=0`
- `overflow_count=0`
- `buffer_miss_count=0`
- `unrecovered_count=0`
- `safe_enter_count=0`
- `final_state` が `RUN` または `IDLE`

dry-run は packet 生成と CSV 形式確認のための `TEMPLATE_ONLY` とし、実機 baseline の代替にはしない。
