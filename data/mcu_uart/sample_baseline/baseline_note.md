# sample_baseline

このディレクトリは dry-run で生成したサンプル baseline であり、実機 MCU の正常通信結果ではない。

- `hardware_observed=false`
- `baseline_status=template_only`
- `summary.csv` の `pass_fail=TEMPLATE_ONLY`

packet 生成と CSV 形式を実機なしで確認するための雛形として残している。
実機 baseline の代替にはならない。

実機での取得は `data/mcu_uart/m0_baseline_001/` で完了済み
(`hardware_observed=true`, `pass_fail=PASS`, 2026-08-02)。
実測値を参照する場合はそちらを使う。
