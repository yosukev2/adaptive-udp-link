# W06 Run Log

## Linux jitter logger

Issue #85 では、Linux 側ロガーの build/run 手順と Raspberry Pi 5 実機での計測結果を記録する。

### Environment

- Date: 2026-06-01
- Host: `pi5@192.168.40.18`
- Target: Raspberry Pi 5 Linux
- Source: `experiments/w06_jitter/linux_jitter.c`

### Build

```bash
cd ~/adaptive-udp-link
gcc -O2 -Wall -Wextra -o experiments/w06_jitter/linux_jitter experiments/w06_jitter/linux_jitter.c
```

Result: pass

### Run

```bash
mkdir -p data/w06
./experiments/w06_jitter/linux_jitter > data/w06/linux_jitter_raw.csv
```

Result: pass

### Output path

- `data/w06/linux_jitter_raw.csv`

### CSV contract

- header は `env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us`
- data 行は 1000 行
- `env=linux_rpi5`
- `board=raspberry_pi_5`
- `period_target_us=10000`

### Verification

```bash
wc -l data/w06/linux_jitter_raw.csv
head -n 2 data/w06/linux_jitter_raw.csv
tail -n 1 data/w06/linux_jitter_raw.csv
awk -F, 'NR > 1 && NF != 7 { bad++ } END { print bad + 0 }' data/w06/linux_jitter_raw.csv
```

Result:

- total lines: 1001
- data rows: 1000
- first sample_index: 1
- last sample_index: 1000
- column count errors: 0
- observed jitter_us range: -7 to 55

### Notes

- `clock_gettime(CLOCK_MONOTONIC)` で timestamp を取る
- `clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, ...)` で 10ms の絶対時刻スケジュールを作る
- Raspberry Pi 5 実機で `data/w06/linux_jitter_raw.csv` を取得済み
