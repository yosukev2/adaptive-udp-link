date=2026-06-28T23:33:08+09:00
host=Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
branch=issue-131-w08-socket-buffer-matrix
commit=ce21ea32431384ba7c85e405697627c5e357a7d6
lo=lo               UNKNOWN        127.0.0.1/8 ::1/128
socket_buf_defaults=212992/212992
purpose=socket_buffer_tiny_sweep
buffer_option=SO_RCVBUF
rates=10000 14000
requested_rcvbufs=100 512 1024 4096 8000
trials=1 2 3
fixed_conditions=loopback 127.0.0.1:9000 payload_len=48 tx_duration_sec=10 rx_duration_sec=12 recovery_mode=fsm no_affinity sndbuf_default

rate_hz=10000
rcvbuf_requested=100
trial=1
time=2026-06-28T23:33:08+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial1/rx.log --rcvbuf 100 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:33:08 [INFO] socket buffer option=SO_RCVBUF requested=100 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=100
trial=2
time=2026-06-28T23:33:20+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial2/rx.log --rcvbuf 100 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:33:20 [INFO] socket buffer option=SO_RCVBUF requested=100 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=100
trial=3
time=2026-06-28T23:33:32+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial3/rx.log --rcvbuf 100 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_100_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:33:32 [INFO] socket buffer option=SO_RCVBUF requested=100 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=512
trial=1
time=2026-06-28T23:33:44+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial1/rx.log --rcvbuf 512 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:33:44 [INFO] socket buffer option=SO_RCVBUF requested=512 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=512
trial=2
time=2026-06-28T23:33:56+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial2/rx.log --rcvbuf 512 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:33:56 [INFO] socket buffer option=SO_RCVBUF requested=512 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=512
trial=3
time=2026-06-28T23:34:08+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial3/rx.log --rcvbuf 512 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_512_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:34:08 [INFO] socket buffer option=SO_RCVBUF requested=512 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=1024
trial=1
time=2026-06-28T23:34:20+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial1/rx.log --rcvbuf 1024 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:34:20 [INFO] socket buffer option=SO_RCVBUF requested=1024 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=1024
trial=2
time=2026-06-28T23:34:32+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial2/rx.log --rcvbuf 1024 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:34:32 [INFO] socket buffer option=SO_RCVBUF requested=1024 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=1024
trial=3
time=2026-06-28T23:34:44+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial3/rx.log --rcvbuf 1024 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_1024_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:34:44 [INFO] socket buffer option=SO_RCVBUF requested=1024 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=10000
rcvbuf_requested=4096
trial=1
time=2026-06-28T23:34:56+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial1/rx.log --rcvbuf 4096 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:34:56 [INFO] socket buffer option=SO_RCVBUF requested=4096 actual=8192
rcvbuf_actual=8192
run_validity=ok

rate_hz=10000
rcvbuf_requested=4096
trial=2
time=2026-06-28T23:35:08+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial2/rx.log --rcvbuf 4096 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:35:08 [INFO] socket buffer option=SO_RCVBUF requested=4096 actual=8192
rcvbuf_actual=8192
run_validity=ok

rate_hz=10000
rcvbuf_requested=4096
trial=3
time=2026-06-28T23:35:20+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial3/rx.log --rcvbuf 4096 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_4096_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:35:20 [INFO] socket buffer option=SO_RCVBUF requested=4096 actual=8192
rcvbuf_actual=8192
run_validity=ok

rate_hz=10000
rcvbuf_requested=8000
trial=1
time=2026-06-28T23:35:32+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:35:32 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
run_validity=ok

rate_hz=10000
rcvbuf_requested=8000
trial=2
time=2026-06-28T23:35:44+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:35:44 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
run_validity=ok

rate_hz=10000
rcvbuf_requested=8000
trial=3
time=2026-06-28T23:35:56+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_10000_rcvbuf_8000_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:35:56 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=100
trial=1
time=2026-06-28T23:36:08+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial1/rx.log --rcvbuf 100 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:36:08 [INFO] socket buffer option=SO_RCVBUF requested=100 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=100
trial=2
time=2026-06-28T23:36:20+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial2/rx.log --rcvbuf 100 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:36:20 [INFO] socket buffer option=SO_RCVBUF requested=100 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=100
trial=3
time=2026-06-28T23:36:32+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial3/rx.log --rcvbuf 100 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_100_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:36:32 [INFO] socket buffer option=SO_RCVBUF requested=100 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=512
trial=1
time=2026-06-28T23:36:44+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial1/rx.log --rcvbuf 512 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:36:44 [INFO] socket buffer option=SO_RCVBUF requested=512 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=512
trial=2
time=2026-06-28T23:36:56+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial2/rx.log --rcvbuf 512 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:36:56 [INFO] socket buffer option=SO_RCVBUF requested=512 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=512
trial=3
time=2026-06-28T23:37:08+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial3/rx.log --rcvbuf 512 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_512_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:37:08 [INFO] socket buffer option=SO_RCVBUF requested=512 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=1024
trial=1
time=2026-06-28T23:37:20+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial1/rx.log --rcvbuf 1024 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:37:20 [INFO] socket buffer option=SO_RCVBUF requested=1024 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=1024
trial=2
time=2026-06-28T23:37:32+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial2/rx.log --rcvbuf 1024 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:37:32 [INFO] socket buffer option=SO_RCVBUF requested=1024 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=1024
trial=3
time=2026-06-28T23:37:44+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial3/rx.log --rcvbuf 1024 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_1024_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:37:44 [INFO] socket buffer option=SO_RCVBUF requested=1024 actual=2304
rcvbuf_actual=2304
run_validity=ok

rate_hz=14000
rcvbuf_requested=4096
trial=1
time=2026-06-28T23:37:56+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial1/rx.log --rcvbuf 4096 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:37:56 [INFO] socket buffer option=SO_RCVBUF requested=4096 actual=8192
rcvbuf_actual=8192
run_validity=ok

rate_hz=14000
rcvbuf_requested=4096
trial=2
time=2026-06-28T23:38:08+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial2/rx.log --rcvbuf 4096 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:38:08 [INFO] socket buffer option=SO_RCVBUF requested=4096 actual=8192
rcvbuf_actual=8192
run_validity=ok

rate_hz=14000
rcvbuf_requested=4096
trial=3
time=2026-06-28T23:38:21+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial3/rx.log --rcvbuf 4096 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_4096_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:38:21 [INFO] socket buffer option=SO_RCVBUF requested=4096 actual=8192
rcvbuf_actual=8192
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
trial=1
time=2026-06-28T23:38:33+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial1
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_tiny --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:38:33 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
trial=2
time=2026-06-28T23:38:45+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial2
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_tiny --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:38:45 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
trial=3
time=2026-06-28T23:38:57+09:00
run_dir=logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial3
rx_csv=data/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_tiny --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_tiny/rate_14000_rcvbuf_8000_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 23:38:57 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
run_validity=ok
