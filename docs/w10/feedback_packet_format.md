# W10 feedback UDP packet format

## 目的

RXが1秒windowで観測した missing と latency を、TXへ返すための最小feedback UDP packet形式を定義する。
このfeedbackはdata pathとは別の RX→TX UDP packet として送る。

## 転送方向

- sender: RX
- receiver: TX
- transport: UDP
- data packetとは別portを使う
- feedback packetが欠落した場合、TXは現在のrateを維持する

## byte order

multi-byte integer fieldは network byte order、つまり big-endian とする。
floatは使わず、rateやlatencyは整数スケール値で送る。

## packet layout: version 1

| offset | size | field | type | unit | description |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | feedback_version | uint8 | - | format version。初期値は1 |
| 1 | 1 | header_len | uint8 | bytes | v1では40 |
| 2 | 2 | flags | uint16 | bitfield | v1では0 |
| 4 | 4 | feedback_seq | uint32 | packets | RXがfeedback送信ごとに+1 |
| 8 | 8 | window_start_ns | uint64 | ns | RX側1秒window開始時刻、CLOCK_MONOTONIC |
| 16 | 8 | window_end_ns | uint64 | ns | RX側1秒window終了時刻、CLOCK_MONOTONIC |
| 24 | 4 | recv_ok | uint32 | frames | window内で正常受信したframe数 |
| 28 | 4 | missing_delta | uint32 | frames | window内で新たに観測したmissing増分 |
| 32 | 4 | missing_rate_ppm | uint32 | ppm | `missing_delta / (recv_ok + missing_delta) * 1,000,000` |
| 36 | 4 | p99_latency_us | uint32 | us | RX側1秒window内のP99 latency |

v1 payload sizeは40 bytesとする。

## field semantics

### feedback_seq

RX process起動後、最初に送るfeedbackを0とし、送信ごとに1ずつ増やす。
TXはfeedback_seqの欠番を検出できるが、欠番があってもrateを即変更しない。

### window_start_ns / window_end_ns

RX側の統計window境界を表す。
時刻源はRX processの `CLOCK_MONOTONIC` であり、TX時刻との絶対比較には使わない。
TXではwindow長やfeedback順序の確認に使う。

### recv_ok

window内でparse成功し、正常受信として扱ったframe数。
既存の `parse_status=OK` と整合させる。

### missing_delta

累積値ではない。
window内で新たに観測したmissingの増分である。
例えば前windowまでのmissing累積が100、今回window終了時点で112なら、このfieldは12になる。

### missing_rate_ppm

TX側でfloat binary互換を考えなくてよいように ppm 整数で送る。

```text
missing_rate_ppm = missing_delta * 1,000,000 / max(1, recv_ok + missing_delta)
```

### p99_latency_us

RX側1秒window内で計算したP99 latencyをmicrosecond整数で送る。
既存CSVの latency_ns から算出する場合は `latency_ns / 1000` を使う。

## TX側の欠落時挙動

feedback packetが届かないwindowがあっても、TXは現在のrate_hzを維持する。
欠落したfeedbackを補完するための再送要求は行わない。

## 非対象

- adaptive rate更新policy
- FEC制御policy
- 長期binary互換性
- data frame format変更

## 参照Issue

- #150
- parent: #149
