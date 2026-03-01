# Frame v1 Protocol

## 1. 目的
Frame v1 は、可変長 payload を持つ破損検知（CRC32）と再同期（Resync）が可能になるフレームのバイト列を作成する。


## 2. 基本方針
- 固定長ヘッダ + 可変長 payload
- preamble は再同期用の目印であり、CRC32 の計算対象には含めない。
- 整数値はすべて network byte order（big-endian）で格納する。

## 3. フレーム構造
Frame v1 は以下の順序で並ぶ。

| Offset | Size | Field       | Description |
|-------:|-----:|-------------|-------------|
| 0      | 4    | preamble    | フレーム開始識別子（固定値） |
| 4      | 1    | version     | プロトコルバージョン |
| 5      | 1    | header_len  | CRCを含む、payload以外のヘッダ長（byte）、|
| 6      | 2    | payload_len | このフレームに含まれる payload の実長（byte） |
| 8      | 4    | seq         | 送信順序番号 |
| 12     | 8    | tx_ts       | 送信時刻（ns, CLOCK_MONOTONIC 基準） |
| 20     | 1    | flags       | 将来拡張用フラグ |
| 21     | 4    | crc32       | CRC32 値 |
| 25     | N    | payload     | 可変長データ（N = payload_len） |

## 4. 固定値
- preamble = 0xA55AC33C
- version = 1
- header_len = 25
- payload_len の上限 = 1024
- flags の未使用ビットは 0 とする

## 5. CRC32 の計算対象
crc32 は、以下のバイト列を対象に計算した 32-bit CRC の値である。

計算対象:
- version
- header_len
- payload_len
- seq
- tx_ts
- flags
- payload

計算対象外:
- preamble
- crc32


## 6. 正しいフレームとみなす条件
受信側は、候補フレームについて以下をすべて満たしたときのみ「正しいフレーム」とみなす。
flagsは判定に用いない。

1. preamble が一致する
2. version == 1
3. header_len == 25
4. payload_len <= 1024
5. header_len + payload_len = 28 + payloadのバイト数
6. CRC32 が一致する


