# sample_baseline

このディレクトリは dry-run で生成したサンプル baseline であり、実機 MCU の正常通信結果ではない。

- `hardware_observed=false`
- `baseline_status=template_only`
- `summary.csv` の `pass_fail=TEMPLATE_ONLY`

Issue #194 の完了には、実機 UART 接続で `hardware_observed=true` のログを取得する必要がある。
