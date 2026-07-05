# W09 retransmit feedback design

## 目的

#155 の adaptive rate down 実験では、missing rate は小幅に改善した一方で、受信できた frame 総数が大きく減った。

#173 では rate を下げる代わりに、RX feedback で欠落 range をTXへ伝え、TX が保持している送信済み datagram を再送する。

## 最小方式

- RX は 1秒 feedback window 内で最初に観測した missing range を feedback packet に載せる。
- TX は通常送信 datagram を bounded ring buffer に保存する。
- TX は feedback の range と重なる datagram が buffer に残っている場合だけ再送する。
- 再送は通常送信 rate_hz とは独立して、feedback受信時に即時実行する。
- 1 feedback あたりの再送 datagram 数には上限を設ける。

## feedback packet extension

既存の feedback v1 packet を 48 bytes に拡張した。

追加field:

| field | type | unit | description |
|---|---|---|---|
| flags bit0 | uint16 | bit | retransmit request がある場合に 1 |
| retransmit_start_seq | uint32 | frame seq | 再送要求rangeの先頭seq |
| retransmit_count | uint32 | frames | 再送要求frame数 |

## TX option

- `--retransmit-mode off|on`
- `--retransmit-buffer-datagrams <n>`
- `--retransmit-max-datagrams-per-feedback <n>`

## RX option

- `--retransmit-request off|on`

## metrics

RX summary:

- `unique_received_frames_total`
- `duplicate_frames_total`
- `recovered_by_retransmit_count`
- `effective_missing_total`
- `effective_missing_rate`

TX summary:

- `retransmit_requested_frames`
- `retransmit_sent_datagrams`
- `retransmit_sent_frames`
- `retransmit_buffer_miss_count`

## 制限

- 1 feedback window 内の最初の missing range のみを要求する。
- 複数gapを完全には要求しない。
- 再送bufferから消えた seq は回復できない。
- FECとは併用しない。
- TCP型の本格ARQではない。
