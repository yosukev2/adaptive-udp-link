# m0_baseline_001

Pi 5 と Raspberry Pi Pico を UART で直結し、`docs/mcu_uart/protocol.md` の packet v1
で 10 パケットを送受信した実機 baseline。dry-run ではなく実機観測。

- `hardware_observed=true`
- `baseline_status=hardware_run`
- `summary.csv` の `pass_fail=PASS`
- `firmware_version=1321d35`

取得日: 2026-08-02

## 結果

| 指標 | 値 |
|------|---:|
| `sent_count` | 10 |
| `mcu_received_count` | 10 |
| `pc_received_count` | 10 |
| `exact_match_count` | 10 |
| `crc_error_count` | 0 |
| `seq_gap_count` | 0 |
| `duplicate_count` | 0 |
| `final_state` | `RUN` |

MCU telemetry の最終行では `rx_packet_count=10`、`ack_sent_count=10`、
`last_seq=9`、`expected_seq=10`。PC が送った 10 パケットを MCU が全数受理し、
ACK を返し、payload が完全一致で往復したことを示す。

`received_count` は PC 側の受信数ではなく **MCU telemetry の `rx_data_count`** を
採用している。PC 側の観測だけでなく、MCU 内部のカウンタで受理を確認している。

## 配線

この個体では既定ピンが使えないため、代替ピンで配線している。

| 信号 | Pi 5 物理 pin | 向き | Pico |
|------|-------------:|:----:|------|
| TX -> RX | 7 (GPIO4) | -> | `GP13` |
| RX <- TX | 29 (GPIO5) | <- | `GP12` |
| GND | 9 | -- | `GND` |

port は `/dev/ttyAMA2` (`dtoverlay=uart2-pi5`)。

`mcu_telemetry.csv` の先頭行に firmware が出力した構成が残る。

```text
# uart0 tx=GP12 rx=GP13 baudrate=115200 heartbeat_ms=0
```

既定の `/dev/ttyAMA0` (GPIO14/15) と Pico の `GP0`/`GP1` は、いずれもこの環境では
機能しなかった。経緯と切り分け手順は `docs/mcu_uart/link_bringup_triage.md`。

## 既知の観測

`last_error_code=1` (`BAD_PREAMBLE`)、`preamble_miss_count=1`、
`rx_byte_count=321`。

正味のデータは 10 パケット x 32 バイト = 320 バイトで、超過分の 1 バイトは電源投入
直後に RX ラインが浮いていた時間帯に拾ったノイズ。10 パケットの送受信そのものには
影響しておらず、`pass_fail` の判定条件にも含まれない。
