# W08-6 送信間隔 sweep の要約

- baseline は `--rate-hz 100`
- `rate_hz=100` は 1 frame あたり 10 ms を意味する
- `TX_FRAMES_PER_DATAGRAM=3` なので、1 datagram は 30 ms ごとに送信される
- baseline では latency と CPU 使用率にまだかなり余裕がある
- そのため、`--rate-hz` だけを変えたときに latency、特に末尾の tail latency が悪化するか改善するかを見る
- 実験候補は `50 / 200 / 500 / 1000 / 10000 Hz`
- 実測では、`rate_hz` を上げるほど latency の mean / p95 / p99 が下がる傾向が出た
- したがって、当初の「`rate_hz` が高いほど負荷が増えて latency が悪化する」という仮説は、この loopback 条件では支持されなかった
- 現時点の仮説は、Pi 5 にまだ余裕があり、`rate_hz` 上昇による CPU 飽和ではなく、`poll()` / wakeup / scheduling の見え方の変化が latency に効いている可能性がある、というもの
- Raspberry Pi 5 は 1 core 2.4 GHz とみなせるので、`rate_hz=10000 frame/s` では 1 frame あたり約 `2.4e9 / 10000 = 240,000` cycle の時間予算がある
- `cpu_pct` は `process CPU time / wall time` なので、単一スレッドならこの cycle 予算の使用率に近い指標として読める
- 例として `cpu_pct=5%` なら、実使用は約 `12,000 cycle/frame` 相当
- 飽和目安は `上限 rate_hz ≒ 測定 rate_hz × 目標 CPU% / 実測 cpu_pct` で概算できる
- そのため、`rate_hz=10000` で `cpu_pct=5%` なら、70% 目安で約 `140000 frame/s`、100% 目安で約 `200000 frame/s` 程度まで余地がある
- それ以外の条件は固定する
  - loopback
  - `127.0.0.1`
  - port `9000`
  - payload `48`
  - tx 10 秒
  - rx 12 秒
  - `recovery_mode=fsm`
  - CPU affinity なし
  - socket buffer 調整なし
- 実行後は `scripts/analyze_w08_send_interval.py` で CSV を集計し、比較結果を
  - `data/w08/send_interval/w08_send_interval_summary.csv`
  - `reports/w08_send_interval_summary.md`
  に出力する
