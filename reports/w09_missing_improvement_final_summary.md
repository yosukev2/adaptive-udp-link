# W09 missing改善 最終サマリー

## 目的

W09では、受信側の観測値に基づいて missing を改善する手段として、以下の3系統を実装・検証した。

- adaptive rate制御: feedbackに基づいて `rate_hz` を下げる。
- retransmit: feedbackに基づいて欠落範囲を再送する。
- XOR FEC: datagram random_drop条件で冗長datagramにより欠落を復元する。

P99 latencyは補助指標として扱い、主成功指標は missing reduction と final delivered / unique received frames の改善とする。

## 成果物

| 分類 | 成果物 |
|---|---|
| feedback packet仕様 | `docs/w09/feedback_packet_format.md` |
| adaptive rate summary | `reports/w09_adaptive_rate_summary.md` |
| retransmit仕様 | `docs/w09/retransmit_design.md` |
| retransmit summary | `reports/w09_retransmit_summary.md` |
| XOR FEC仕様 | `docs/w09/xor_fec_design.md` |
| adaptive FEC仕様 | `docs/w09/adaptive_fec_design.md` |
| FEC ON/OFF比較summary | `reports/w09_fec_comparison_summary.md` |

## 方式別の結論

| 方式 | 条件 | 改善結果 | final delivered / usable dataへの影響 | 主な限界 |
|---|---|---:|---:|---|
| adaptive rate | rate_hz 120000 start、OFF/ON各10 trial | missing rate平均 2.8919% → 2.7661% | 受信frame総数 34,958,871 → 18,827,169 | rate downで送信総量も減るため、受信総量最大化には向きにくい |
| retransmit | rate_hz 120000、OFF/ON各3 trial | effective_missing_total 517,431 → 280,728、45.7458%削減 | unique delivered 10,282,560 → 10,519,263 | ON/OFFでraw missing条件差があり、改善の全てを再送効果とは断定しない。再送分のlatencyは大きい |
| XOR FEC | random_drop 10%、rate_hz 1200、OFF/ON各10 trial | effective_missing_total 36,312 → 9,756、73.1328%削減 | usable datagrams +8,853 | parity到着後に復元するためlatencyは増える。1 block内複数欠損は復元不可 |
| XOR FEC | random_drop 10%、rate_hz 120000、OFF/ON各10 trial | effective_missing_total 3,602,061 → 976,164、72.8998%削減 | usable datagrams +875,299 | parity overheadがある。1 block内複数欠損またはparity欠損は復元不可 |

## missing種別ごとの整理

| missing種別 | 観測・再現方法 | 改善できた手段 | 解釈 |
|---|---|---|---|
| rate過大・受信処理詰まり由来 | rate_hz 120000 loopbackで試行ごとのmissingばらつきとして観測 | adaptive rateで小幅改善、retransmitで一部回復 | 平均rateだけでは説明しにくく、一時的な受信詰まり・スケジューリング・socket queueの影響を受ける。rate downは緊急退避にはなるが、final deliveredを大きく減らす |
| feedbackで後から補える欠落 | retransmit requestにより欠落範囲をTXへ通知 | retransmit | bounded retransmit buffer内に残っているdatagramは後着で回復できる。ただし古いtimestampを持つためlatencyは増える。buffer外や要求範囲制限を超えたものは回復不可 |
| random_drop由来の単発datagram欠落 | `--drop-rate 0.10 --drop-target datagram` | XOR FEC k=4,r=1 | OFF/ONで同じdrop_seedを使うことでraw missingを揃えた比較が可能。1 FEC block内でdata datagramが1個だけ欠ける場合は高い確率で復元できる |
| FECで回復できない欠落 | FEC ONでも残る `unrecovered_count` / `effective_missing_total` | 今回のk=4,r=1では不可 | 1 block内で複数data datagramが欠ける、またはparity datagramが欠ける条件ではXOR 1 parityでは復元できない |

## 効かなかった・逆効果になった条件

- adaptive rateは、missing rateを小幅に下げた一方で、受信できたframe総数をOFFの約54%まで減らした。missing率だけを見れば改善だが、final delivered最大化の観点では逆効果になりうる。
- retransmitはeffective_missingを下げたが、今回のrunではON側のraw missingもOFFより小さかったため、改善の全てを再送だけの効果とは断定しない。また再送frameは元のTX timestampを持つため、latencyは大きく悪化する。
- XOR FECはrandom_drop条件では安定してeffective_missingを下げたが、FEC ONでもunrecoveredは残る。k=4,r=1の範囲では、複数欠損やparity欠損は回復できない。

## W09の結論

- rate_hzを下げる制御だけでは、missingを安定的に下げつつfinal deliveredを最大化するには不十分だった。
- 欠落を後から補う方針では、retransmitとFECのどちらもeffective_missingを下げられる。
- retransmitはfeedbackとbufferに依存し、後着latencyが大きくなる。
- XOR FECはrandom_dropのような単発datagram欠落に強く、今回の同一seed比較ではeffective_missingを約73%削減した。
- 今回の範囲で最も明確に効果を確認できたのは、random_drop条件に対するXOR FECだった。

## 関連Issue

- adaptive rate: #150, #151, #152, #153, #154, #155
- retransmit: #173
- random_drop / XOR FEC: #156, #157, #158, #159, #160, #161, #162

Closes #149