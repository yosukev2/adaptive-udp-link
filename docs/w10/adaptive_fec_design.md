# W10 adaptive FEC policy

対象Issue: #161
親Issue: #149

## 目的

RX feedbackのmissing情報を使い、TX側でFEC modeを `off` と `xor` の間で切り替える。
rate_hz制御とは分離し、このpolicyでは送信rateは変更しない。

## CLI

TX:

- `--adaptive-fec off|on`
- `--adaptive-fec-high-missing-rate <rate>`: FECをONにするmissing_rate閾値。default `0.001`。
- `--adaptive-fec-low-missing-rate <rate>`: FECをOFFへ戻すための低missing_rate閾値。default `0.0`。
- `--adaptive-fec-stable-windows <n>`: low missing windowがn回続いたらFECをOFFにする。default `3`。

`--adaptive-fec on` は `--feedback-bind-ip`, `--feedback-bind-port`, `--adaptive-log-path` を必須とする。

## policy

- FEC off中に `missing_rate > high_missing_rate` なら `xor` へ切り替える。
- FEC on中に `missing_rate <= low_missing_rate` が `stable_windows` 回続いたら `off` へ戻す。
- FEC on中にmissingが残る場合はFEC onを維持する。
- rate_hzは変更しない。

## feedbackで使うmissing

FEC有効時、RXはfeedbackの `missing_delta` に `raw gap - FEC recovered` を入れる。
これにより、FECで復元できたmissingはTXのadaptive FEC判定ではeffective missingとして扱われる。

## adaptive log

`adaptive_log_path` には以下のFEC decision列を出す。

- `effective_missing_rate`
- `old_fec_mode`
- `new_fec_mode`
- `fec_action`
- `fec_reason`
- `fec_stable_windows`

## 非対象

- 可変k/r。
- Reed-Solomon。
- retransmitとの同時利用。
- 同一policy内でのrate_hz変更。