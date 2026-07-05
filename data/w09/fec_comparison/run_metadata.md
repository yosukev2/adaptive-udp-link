# W09 random_drop + XOR FEC comparison metadata

- date: 2026-07-05T11:08:52+09:00
- host: Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
- branch: issue-162-w09-fec-comparison
- commit: 05c4bae86927f1dcf41398c5b1f2570d03fa8322
- rate_hz: 1200
- drop_rate: 0.10
- drop_seeds: 101 102 103 104 105 106 107 108 109 110
- tx_duration_sec: 30
- rx_duration_sec: 32
- data_port: 24001
- trials: 1 2 3 4 5 6 7 8 9 10
- rx_core: 2
- tx_core: 3
- data_dir: data/w09/fec_comparison
- log_dir: logs/w09/fec_comparison

## 固定条件

- loopback: 127.0.0.1
- payload_len: 48
- FEC ON: tx/rx both --fec-mode xor
- FEC OFF: tx/rx both --fec-mode off
- random drop target: datagram
- 同じtrial番号ではFEC OFF/ONで同じdrop_seedを使う

## fec_mode=off trial=1

- time: 2026-07-05T11:08:52+09:00
- seed: 101
- run_dir: logs/w09/fec_comparison/fec_off_trial1
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial1/rx.log --link-name w09_fec_comparison --trial 1 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial1/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial1/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 101 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=2

- time: 2026-07-05T11:09:24+09:00
- seed: 102
- run_dir: logs/w09/fec_comparison/fec_off_trial2
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial2/rx.log --link-name w09_fec_comparison --trial 2 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial2/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial2/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 102 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=3

- time: 2026-07-05T11:09:56+09:00
- seed: 103
- run_dir: logs/w09/fec_comparison/fec_off_trial3
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial3/rx.log --link-name w09_fec_comparison --trial 3 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial3/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial3/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 103 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=4

- time: 2026-07-05T11:10:28+09:00
- seed: 104
- run_dir: logs/w09/fec_comparison/fec_off_trial4
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial4/rx.log --link-name w09_fec_comparison --trial 4 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial4/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial4/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial4/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 104 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=5

- time: 2026-07-05T11:11:00+09:00
- seed: 105
- run_dir: logs/w09/fec_comparison/fec_off_trial5
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial5/rx.log --link-name w09_fec_comparison --trial 5 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial5/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial5/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial5/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 105 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=6

- time: 2026-07-05T11:11:32+09:00
- seed: 106
- run_dir: logs/w09/fec_comparison/fec_off_trial6
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial6/rx.log --link-name w09_fec_comparison --trial 6 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial6/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial6/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial6/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 106 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=7

- time: 2026-07-05T11:12:04+09:00
- seed: 107
- run_dir: logs/w09/fec_comparison/fec_off_trial7
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial7/rx.log --link-name w09_fec_comparison --trial 7 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial7/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial7/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial7/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 107 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=8

- time: 2026-07-05T11:12:36+09:00
- seed: 108
- run_dir: logs/w09/fec_comparison/fec_off_trial8
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial8/rx.log --link-name w09_fec_comparison --trial 8 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial8/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial8/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial8/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 108 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=9

- time: 2026-07-05T11:13:08+09:00
- seed: 109
- run_dir: logs/w09/fec_comparison/fec_off_trial9
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial9/rx.log --link-name w09_fec_comparison --trial 9 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial9/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial9/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial9/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 109 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=off trial=10

- time: 2026-07-05T11:13:40+09:00
- seed: 110
- run_dir: logs/w09/fec_comparison/fec_off_trial10
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_off_trial10/rx.log --link-name w09_fec_comparison --trial 10 --fec-mode off --csv-in-1sec-log-path logs/w09/fec_comparison/fec_off_trial10/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_off_trial10/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_off_trial10/tx.log --payload-len 48 --version 1 --fec-mode off --drop-rate 0.10 --drop-seed 110 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=1

- time: 2026-07-05T11:14:12+09:00
- seed: 101
- run_dir: logs/w09/fec_comparison/fec_xor_trial1
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial1/rx.log --link-name w09_fec_comparison --trial 1 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial1/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial1/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 101 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=2

- time: 2026-07-05T11:14:44+09:00
- seed: 102
- run_dir: logs/w09/fec_comparison/fec_xor_trial2
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial2/rx.log --link-name w09_fec_comparison --trial 2 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial2/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial2/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 102 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=3

- time: 2026-07-05T11:15:16+09:00
- seed: 103
- run_dir: logs/w09/fec_comparison/fec_xor_trial3
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial3/rx.log --link-name w09_fec_comparison --trial 3 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial3/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial3/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 103 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=4

- time: 2026-07-05T11:15:48+09:00
- seed: 104
- run_dir: logs/w09/fec_comparison/fec_xor_trial4
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial4/rx.log --link-name w09_fec_comparison --trial 4 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial4/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial4/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial4/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 104 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=5

- time: 2026-07-05T11:16:20+09:00
- seed: 105
- run_dir: logs/w09/fec_comparison/fec_xor_trial5
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial5/rx.log --link-name w09_fec_comparison --trial 5 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial5/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial5/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial5/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 105 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=6

- time: 2026-07-05T11:16:52+09:00
- seed: 106
- run_dir: logs/w09/fec_comparison/fec_xor_trial6
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial6/rx.log --link-name w09_fec_comparison --trial 6 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial6/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial6/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial6/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 106 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=7

- time: 2026-07-05T11:17:24+09:00
- seed: 107
- run_dir: logs/w09/fec_comparison/fec_xor_trial7
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial7/rx.log --link-name w09_fec_comparison --trial 7 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial7/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial7/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial7/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 107 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=8

- time: 2026-07-05T11:17:56+09:00
- seed: 108
- run_dir: logs/w09/fec_comparison/fec_xor_trial8
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial8/rx.log --link-name w09_fec_comparison --trial 8 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial8/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial8/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial8/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 108 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=9

- time: 2026-07-05T11:18:28+09:00
- seed: 109
- run_dir: logs/w09/fec_comparison/fec_xor_trial9
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial9/rx.log --link-name w09_fec_comparison --trial 9 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial9/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial9/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial9/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 109 --drop-target datagram

- tx_status: 0
- rx_status: 0

## fec_mode=xor trial=10

- time: 2026-07-05T11:19:00+09:00
- seed: 110
- run_dir: logs/w09/fec_comparison/fec_xor_trial10
- rx_cmd: taskset -c 2 ./bin/rx --bind-ip 127.0.0.1 --port 24001 --duration-sec 32 --log-path logs/w09/fec_comparison/fec_xor_trial10/rx.log --link-name w09_fec_comparison --trial 10 --fec-mode xor --csv-in-1sec-log-path logs/w09/fec_comparison/fec_xor_trial10/rx_1sec.csv --csv-by-1recv-log-path logs/w09/fec_comparison/fec_xor_trial10/rx_by_1recv.csv
- tx_cmd: taskset -c 3 ./bin/tx --dst-ip 127.0.0.1 --dst-port 24001 --rate-hz 1200 --duration-sec 30 --log-path logs/w09/fec_comparison/fec_xor_trial10/tx.log --payload-len 48 --version 1 --fec-mode xor --drop-rate 0.10 --drop-seed 110 --drop-target datagram

- tx_status: 0
- rx_status: 0

