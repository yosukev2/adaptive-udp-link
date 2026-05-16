# W06 Run Log

## Linux jitter logger

Issue #85 では、Linux 側ロガーの build/run 手順を先に固定する。実機の Raspberry Pi 5 で計測した結果はまだ記録していない。

### Build

```bash
gcc -O2 -Wall -Wextra -o experiments/w06_jitter/linux_jitter experiments/w06_jitter/linux_jitter.c
```

### Run

```bash
mkdir -p data/w06
./experiments/w06_jitter/linux_jitter > data/w06/linux_jitter_raw.csv
```

### Expected output path

- `data/w06/linux_jitter_raw.csv`

### CSV contract

- header は `env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us`
- data 行は 1000 行
- `env=linux_rpi5`
- `board=raspberry_pi_5`
- `period_target_us=10000`

### Notes

- `clock_gettime(CLOCK_MONOTONIC)` で timestamp を取る
- `clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, ...)` で 10ms の絶対時刻スケジュールを作る
- 本書は手順の記録であり、未実施の Raspberry Pi 5 実測結果は書かない
