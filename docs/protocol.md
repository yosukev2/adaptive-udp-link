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
| 5      | 1    | header_len  | payload を除くヘッダ全体の長さ（byte）。crc32 を含む。 |
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

## 5. CRC32 の計算対象と算法

### 計算対象フィールド（この順序で連結したバイト列に対して計算する）

| Field       | Size |
|-------------|-----:|
| version     | 1    |
| header_len  | 1    |
| payload_len | 2    |
| seq         | 4    |
| tx_ts       | 8    |
| flags       | 1    |
| payload     | N    |

計算対象外:
- preamble（再同期用であり CRC で保護しない）
- crc32 自体

固定部の合計 = 1+1+2+4+8+1 = **17 バイト**

### CRC32 算法

| 項目 | 値 |
|------|---|
| 規格 | CRC-32/ISO-HDLC（IEEE 802.3 互換） |
| 多項式（reflected） | 0xEDB88320 |
| 初期値 | 0xFFFFFFFF |
| 最終 XOR | 0xFFFFFFFF |
| ビット順 | LSB-first（reflected） |

テストベクタ（`src/frame_v1_wire.c` の `kFrameV1Crc32TestExpected`）:
- payload = `"crc32-test-payload"` (18 bytes)
- seq = 0x01020304, tx_ts = 0x1122334455667788, flags = 0
- 期待 CRC32 = **0x2D3B0C55**

## 6. 正しいフレームとみなす条件
受信側は、候補フレームについて以下をすべて満たしたときのみ「正しいフレーム」とみなす。
flags は判定に用いない。

1. preamble が一致する
2. version == 1
3. header_len == 25
4. payload_len <= 1024
5. wire 上のバイト数 = header_len + payload_len = **25 + payload_len**
6. CRC32 が一致する

## 7. 未対応事項（現時点）

以下は意図的に未実装。将来の Issue で対応する。

| 事項 | 状態 | 備考 |
|------|------|------|
| seq wrap-around | **未対応** | seq は uint32_t。2^32 周回時の連続性判定は行わない。欠損・重複カウントが誤る可能性がある。 |
| ACK / NACK / 再送 | 未実装 | UDP one-way 計測のみ |
| 複数ストリーム管理 | 未実装 | 単一ソケット前提 |

## 8. datagram と frame の関係

1 UDP datagram に **3 frame** を連結して送信する（W02 #40 実装済み）。

- 送信側（tx）: `TX_FRAMES_PER_DATAGRAM=3` frame を 1 回の `sendto` で送信する
- 受信側（rx）: datagram を byte 列としてストリームバッファに積み、preamble 探索で複数 frame を順次切り出す

受信側は datagram 内で preamble を再探索（resync）し、破損 frame の次の正常 frame から復帰できる。

## 9. trial_summary の固定列

Host と MCU/実リンクで同じ列順を使うため、受信側は `--link-name` と `--trial` の両方が与えられた trial 終了時に、以下の 1 行 summary を出す。

```text
trial_summary link_name=<token> trial=<n> duration_sec=<sec> sent=<n|na> recv_ok=<n> gap_est=<n> crc_fail=<n> len_invalid=<n> preamble_miss=<n> resync_count=<n> latency_p50_ms=<value> latency_p95_ms=<value> latency_max_ms=<value>
```

列順は固定で、順番を入れ替えない。どちらかの metadata が欠ける run では、誤った trial 識別子を出さないため `trial_summary` を出力しない。

| 列 | 意味 |
|----|------|
| link_name | 比較対象の link 識別子。Host loopback / MCU / 実リンク名などを token で入れる。rx 単体では `--link-name` を受け取り、token 以外の文字は `_` に正規化する。 |
| trial | 同一条件内の試行番号。rx 単体では `--trial` で受け取る。 |
| duration_sec | rx がその trial で観測する設定時間（`--duration-sec`）。 |
| sent | trial 全体で送信側が把握している frame 数。rx 単体では確定できないため、W03 #55 時点では `na` を出す。 |
| recv_ok | parse / validate / CRC がすべて成功した frame 数。 |
| gap_est | seq の不連続から推定した欠落 frame 数。従来の `gap_cnt` と同義。 |
| crc_fail | CRC32 不一致で棄却した frame 数。従来の `bad_crc` と同義。 |
| len_invalid | payload_len 超過で棄却した frame 数。 |
| preamble_miss | preamble が先頭にないと判定して再探索した回数。 |
| resync_count | 受信側が次の preamble を探し直した回数。 |
| latency_p50_ms | 正常受信 frame の latency p50。`recv_ok` に数えた frame のうち、`tx_ts <= recv_now` で latency を確定できたものだけを候補にする。sample 数が 0 の run、または `future_ts` が混じって `recv_ok` 全体を代表できない run では `na` を出す。 |
| latency_p95_ms | 正常受信 frame の latency p95。`recv_ok` に数えた frame のうち、`tx_ts <= recv_now` で latency を確定できたものだけを候補にする。sample 数が 0 の run、または `future_ts` が混じって `recv_ok` 全体を代表できない run では `na` を出す。 |
| latency_max_ms | 正常受信 frame の latency max。`recv_ok` に数えた frame のうち、`tx_ts <= recv_now` で latency を確定できたものだけを候補にする。sample 数が 0 の run、または `future_ts` が混じって `recv_ok` 全体を代表できない run では `na` を出す。 |

`trial_summary` は列順と意味を固定するための summary であり、既存の `rx summary` は補助ログとして残してよい。

percentile の算出は nearest-rank を使う。sample 数が 1 の場合は `p50 = p95 = max` になり、偶数個でも中央値補間はしない。percentile 用サンプルは `trial_summary` を出す run でだけ保持する。

## 10. 受信ループの統計カウンタ

| カウンタ | 意味 |
|---------|------|
| recv_any | recvfrom() が成功した回数（不正フレームを含む） |
| recv_ok | parse / validate / CRC がすべて成功したフレーム数 |
| bad_size | payload_len 超過または parse 失敗の回数 |
| bad_header | preamble / version / header_len 不正の回数 |
| bad_crc | CRC32 不一致の回数 |
| poll_timeout | poll() がタイムアウトした回数。1 秒周期の統計出力トリガーでもある。受信が途切れた秒数の目安になる。 |
| gap_cnt | seq の不連続から推定した欠落フレーム数（UDP 順序保証なしのため「推定値」） |
| dup_cnt | 同一 seq を持つフレームを受信した回数 |
| reord_cnt | seq が前回より小さいフレームを受信した回数（逆順到着の推定） |

## 11. 設計判断

### preamble 長（4 bytes）

2 bytes だと一致確率が高く、データ中に偶然同じ値が頻繁に現れて誤検出するため、4 bytes を選択した。

### preamble 値（0xA55AC33C）

0 と 1 が偏らず単純すぎないビット列にすることで、検出しやすく誤一致しにくくするため、この値を選択した。

### payload 長の上限（1024 bytes）

1500 bytes を超えると IP で分割され、一部欠損で全体ロストや遅延増加が起きて挙動が不安定になるため、Ethernet MTU（1500 bytes）に収まる上限として 1024 bytes を選択した。

### CRC の適用範囲（preamble を除外）

preamble は境界検出用、CRC は内容検証用であり、役割を分けるため preamble を CRC の計算対象に含めない。
