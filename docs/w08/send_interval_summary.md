# W08-6 送信間隔 sweep の要約

- baseline は `--rate-hz 100`
- `rate_hz=100` は 1 frame あたり 10 ms を意味する
- `TX_FRAMES_PER_DATAGRAM=3` なので、1 datagram は 30 ms ごとに送信される
- baseline では latency と CPU 使用率にまだかなり余裕がある
- そのため、`--rate-hz` だけを変えたときに latency、特に末尾の tail latency が悪化するか改善するかを見る
- 実験候補は `50 / 200 / 500 / 1000 / 10000 Hz`
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
