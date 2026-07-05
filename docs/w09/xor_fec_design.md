# W09 XOR FEC design

親Issue: #149
対象Issue: #157 / #158 / #159 / #160

## 目的

実験2用の最小FECとして XOR FEC `k=4,r=1` を実装する。
4個のdata UDP datagramを1つのFEC blockとし、その直後に1個のparity UDP datagramを送る。

## datagram形式

FEC有効時は、既存のFrame v1 wire formatは変更しない。
UDP datagramの先頭にFEC datagram headerを付け、その後ろに既存の「3 frames/datagram」のpayloadを置く。

### FEC v1 header

| offset | size | field | type | meaning |
|---:|---:|---|---|---|
| 0 | 4 | magic | uint32 | `0x46454331` (`FEC1`) |
| 4 | 1 | version | uint8 | `1` |
| 5 | 1 | header_len | uint8 | `24` |
| 6 | 1 | packet_type | uint8 | `1=data`, `2=parity` |
| 7 | 1 | k | uint8 | `4` |
| 8 | 1 | r | uint8 | `1` |
| 9 | 1 | index_in_block | uint8 | dataは`0..3`、parityは`4` |
| 10 | 2 | payload_len | uint16 | header後続payloadのbyte数 |
| 12 | 4 | block_id | uint32 | FEC block番号 |
| 16 | 4 | first_seq | uint32 | block内index 0 data datagramの先頭frame seq |
| 20 | 4 | flags | uint32 | 現状0 |

## block割り当て

- TXは送信順にdata datagram 4個を1 blockにまとめる。
- `block_id` はblockごとに+1する。
- `index_in_block` はdata datagram順に `0,1,2,3`。
- parity datagramは同じblockのdata datagram 4個をbyte単位XORしたpayloadを持つ。
- parityはdata datagram内には入れず、別UDP datagramとして送る。

## 復元条件

RXはblockごとにdata/parity datagramを収集する。

復元できる条件:

- completed block内でdata datagramがちょうど1個欠けている。
- parity datagramが届いている。
- block内data/parityのpayload_lenが一致している。

復元しない条件:

- data datagramが2個以上欠けた。
- parity datagramが欠落した。
- block metadataが不整合。
- block timeout/incomplete。

この実装では最小実験用として、parity到着時点で判定できるblockを処理する。

## metrics

RX summaryに以下を出す。

- `fec_raw_missing_frames`: FEC block内で復元前に欠けていたframe数。
- `recovered_by_fec_count`: FECで復元できたframe数。
- `unrecovered_by_fec_count`: FECで復元できず残ったframe数。
- `fec_recovered_datagrams`: FECで復元できたdatagram数。
- `fec_unrecovered_datagrams`: FECで復元できなかったdatagram数。
- `fec_effective_missing_total`: `fec_raw_missing_frames - recovered_by_fec_count`。
- `fec_effective_missing_rate`: `fec_effective_missing_total / (unique_received_frames_total + fec_effective_missing_total)`。

CSVではFEC復元frameを `parse_status=FEC_RECOVERED` として通常受信 `OK` と区別する。

## CLI

TX:

- `--fec-mode off|xor`
- `--fec-k 4`
- `--fec-r 1`
- `--drop-datagram-every <n>`: deterministic検証用。n個に1個のdata datagram送信をskipする。

RX:

- `--fec-mode off|xor`

## 今回の非対象

- Reed-Solomon。
- `r>=2`。
- 可変k/r。
- adaptive FEC ON/OFF policy。
- 再送との同時利用。