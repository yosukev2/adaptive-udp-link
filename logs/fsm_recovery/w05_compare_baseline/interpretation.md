# FSM vs Timeout Comparison

- Run date: 2026-05-09T20:02:15+09:00
- Link name: host_loopback
- Trials per mode/scenario: 3
- Result directory: logs/fsm_recovery/w05_compare_baseline
- Per-run CSV: logs/fsm_recovery/w05_compare_baseline/compare_runs.csv
- Summary CSV: logs/fsm_recovery/w05_compare_baseline/compare_summary.csv

| Outage | Mode | Degraded Detect (ms) | Recover Complete (ms) | Observed Pattern |
|--------|------|----------------------|------------------------|------------------|
| 500 | fsm | na | na | none |
| 1000 | fsm | na | na | none |
| 3000 | fsm | 5000 | 7667 | Normal->Degraded->Recover->Normal |
| 500 | timeout-only | na | na | none |
| 1000 | timeout-only | na | na | none |
| 3000 | timeout-only | 5000 | 8000 | Normal->Degraded->Normal |

0.5s と 1s の outage は、現行の recv_ok == 0 が 2 つの 1 秒窓連続で必要という Degraded 条件を跨がないため、fsm と timeout-only のどちらでも state transition は発生しませんでした。したがって両 mode とも degraded_detect_ms / recover_complete_ms は na です。

3s の outage では両 mode とも Degraded 検知は 5000ms で揃いました。fsm は Normal->Degraded->Recover->Normal と明示的な復旧フェーズを残し、timeout-only は Normal->Degraded->Normal へ直接戻ります。今回の baseline では fsm の Recover 完了は 7667ms、timeout-only の Normal 復帰は 8000ms でした。

一部の mode / outage で trial 間のばらつきがあるため、CPU scheduling や tx 開始オフセットの揺れを候補として再確認してください。
