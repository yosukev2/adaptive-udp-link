date=2026-06-29T22:02:22+09:00
host=Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
branch=issue-131-w08-socket-buffer-matrix
commit=ef32b7efcf8033535a4705f628a2b7ef51f10c68
lo=lo               UNKNOWN        127.0.0.1/8 ::1/128
socket_buf_defaults=212992/212992
purpose=socket_buffer_txrx_matrix
buffer_options=SO_RCVBUF SO_SNDBUF
rates=14000 18000
requested_rcvbufs=8000 12000 16000
requested_sndbufs=2000 4000 8000 10000 12000 16000
trials=1 2 3
fixed_conditions=loopback 127.0.0.1:9000 payload_len=48 tx_duration_sec=10 rx_duration_sec=12 recovery_mode=fsm no_affinity

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=2000
trial=1
time=2026-06-29T22:02:22+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial1/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:02:22 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:02:23 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=2000
trial=2
time=2026-06-29T22:02:34+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial2/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:02:34 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:02:35 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=2000
trial=3
time=2026-06-29T22:02:46+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_2000_trial3/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:02:46 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:02:47 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=4000
trial=1
time=2026-06-29T22:02:59+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial1/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:02:59 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:03:00 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=4000
trial=2
time=2026-06-29T22:03:11+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial2/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:03:11 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:03:12 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=4000
trial=3
time=2026-06-29T22:03:23+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_4000_trial3/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:03:23 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:03:24 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=8000
trial=1
time=2026-06-29T22:03:35+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial1/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:03:35 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:03:36 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=8000
trial=2
time=2026-06-29T22:03:47+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial2/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:03:47 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:03:48 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=8000
trial=3
time=2026-06-29T22:03:59+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_8000_trial3/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:03:59 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:04:00 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=10000
trial=1
time=2026-06-29T22:04:11+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial1/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:04:11 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:04:12 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=10000
trial=2
time=2026-06-29T22:04:23+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial2/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:04:23 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:04:24 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=10000
trial=3
time=2026-06-29T22:04:35+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_10000_trial3/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:04:35 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:04:36 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=12000
trial=1
time=2026-06-29T22:04:47+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial1/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:04:47 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:04:48 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=12000
trial=2
time=2026-06-29T22:04:59+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial2/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:04:59 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:05:00 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=12000
trial=3
time=2026-06-29T22:05:11+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_12000_trial3/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:05:11 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:05:12 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=16000
trial=1
time=2026-06-29T22:05:23+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial1/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:05:23 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:05:24 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=16000
trial=2
time=2026-06-29T22:05:35+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial2/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:05:35 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:05:36 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=8000
sndbuf_requested=16000
trial=3
time=2026-06-29T22:05:47+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_8000_sndbuf_16000_trial3/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:05:47 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:05:48 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=2000
trial=1
time=2026-06-29T22:05:59+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial1/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:05:59 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:06:00 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=2000
trial=2
time=2026-06-29T22:06:11+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial2/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:06:11 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:06:12 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=2000
trial=3
time=2026-06-29T22:06:23+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_2000_trial3/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:06:23 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:06:24 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=4000
trial=1
time=2026-06-29T22:06:35+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial1/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:06:35 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:06:36 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=4000
trial=2
time=2026-06-29T22:06:47+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial2/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:06:47 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:06:48 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=4000
trial=3
time=2026-06-29T22:06:59+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_4000_trial3/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:06:59 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:07:00 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=8000
trial=1
time=2026-06-29T22:07:11+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial1/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:07:11 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:07:12 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=8000
trial=2
time=2026-06-29T22:07:23+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial2/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:07:23 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:07:24 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=8000
trial=3
time=2026-06-29T22:07:35+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_8000_trial3/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:07:35 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:07:36 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=10000
trial=1
time=2026-06-29T22:07:47+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial1/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:07:47 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:07:48 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=10000
trial=2
time=2026-06-29T22:07:59+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial2/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:07:59 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:08:00 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=10000
trial=3
time=2026-06-29T22:08:11+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_10000_trial3/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:08:11 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:08:12 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=12000
trial=1
time=2026-06-29T22:08:24+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial1/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:08:24 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:08:25 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=12000
trial=2
time=2026-06-29T22:08:36+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial2/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:08:36 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:08:37 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=12000
trial=3
time=2026-06-29T22:08:48+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_12000_trial3/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:08:48 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:08:49 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=16000
trial=1
time=2026-06-29T22:09:00+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial1/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:09:00 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:09:01 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=16000
trial=2
time=2026-06-29T22:09:12+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial2/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:09:12 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:09:13 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=12000
sndbuf_requested=16000
trial=3
time=2026-06-29T22:09:24+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_12000_sndbuf_16000_trial3/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:09:24 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:09:25 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=2000
trial=1
time=2026-06-29T22:09:36+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial1/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:09:36 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:09:37 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=2000
trial=2
time=2026-06-29T22:09:48+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial2/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:09:48 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:09:49 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=2000
trial=3
time=2026-06-29T22:10:00+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_2000_trial3/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:10:00 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:10:01 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=4000
trial=1
time=2026-06-29T22:10:12+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial1/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:10:12 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:10:13 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=4000
trial=2
time=2026-06-29T22:10:24+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial2/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:10:24 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:10:25 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=4000
trial=3
time=2026-06-29T22:10:36+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_4000_trial3/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:10:36 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:10:37 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=8000
trial=1
time=2026-06-29T22:10:48+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial1/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:10:48 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:10:49 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=8000
trial=2
time=2026-06-29T22:11:00+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial2/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:11:00 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:11:01 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=8000
trial=3
time=2026-06-29T22:11:12+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_8000_trial3/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:11:12 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:11:13 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=10000
trial=1
time=2026-06-29T22:11:24+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial1/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:11:24 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:11:25 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=10000
trial=2
time=2026-06-29T22:11:36+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial2/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:11:36 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:11:37 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=10000
trial=3
time=2026-06-29T22:11:48+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_10000_trial3/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:11:48 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:11:49 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=12000
trial=1
time=2026-06-29T22:12:00+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial1/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:12:00 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:12:01 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=12000
trial=2
time=2026-06-29T22:12:12+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial2/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:12:12 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:12:13 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=12000
trial=3
time=2026-06-29T22:12:24+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_12000_trial3/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:12:24 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:12:25 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=16000
trial=1
time=2026-06-29T22:12:36+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial1/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:12:36 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:12:37 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=16000
trial=2
time=2026-06-29T22:12:48+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial2/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:12:48 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:12:49 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=14000
rcvbuf_requested=16000
sndbuf_requested=16000
trial=3
time=2026-06-29T22:13:00+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_14000_rcvbuf_16000_sndbuf_16000_trial3/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:13:00 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:13:01 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=2000
trial=1
time=2026-06-29T22:13:12+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial1/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:13:12 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:13:13 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=2000
trial=2
time=2026-06-29T22:13:24+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial2/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:13:24 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:13:25 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=2000
trial=3
time=2026-06-29T22:13:37+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_2000_trial3/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:13:37 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:13:38 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=4000
trial=1
time=2026-06-29T22:13:49+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial1/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:13:49 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:13:50 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=4000
trial=2
time=2026-06-29T22:14:01+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial2/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:14:01 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:14:02 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=4000
trial=3
time=2026-06-29T22:14:13+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_4000_trial3/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:14:13 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:14:14 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=8000
trial=1
time=2026-06-29T22:14:25+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial1/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:14:25 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:14:26 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=8000
trial=2
time=2026-06-29T22:14:37+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial2/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:14:37 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:14:38 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=8000
trial=3
time=2026-06-29T22:14:49+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_8000_trial3/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:14:49 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:14:50 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=10000
trial=1
time=2026-06-29T22:15:01+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial1/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:15:01 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:15:02 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=10000
trial=2
time=2026-06-29T22:15:13+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial2/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:15:13 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:15:14 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=10000
trial=3
time=2026-06-29T22:15:25+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_10000_trial3/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:15:25 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:15:26 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=12000
trial=1
time=2026-06-29T22:15:37+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial1/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:15:37 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:15:38 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=12000
trial=2
time=2026-06-29T22:15:49+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial2/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:15:49 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:15:50 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=12000
trial=3
time=2026-06-29T22:16:01+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_12000_trial3/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:16:01 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:16:02 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=16000
trial=1
time=2026-06-29T22:16:13+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial1/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial1/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:16:13 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:16:14 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=16000
trial=2
time=2026-06-29T22:16:25+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial2/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial2/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:16:25 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:16:26 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=8000
sndbuf_requested=16000
trial=3
time=2026-06-29T22:16:37+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial3/rx.log --rcvbuf 8000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_8000_sndbuf_16000_trial3/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:16:37 [INFO] socket buffer option=SO_RCVBUF requested=8000 actual=16000
rcvbuf_actual=16000
sndbuf_line=2026-06-29 22:16:38 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=2000
trial=1
time=2026-06-29T22:16:49+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial1/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:16:49 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:16:50 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=2000
trial=2
time=2026-06-29T22:17:01+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial2/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:17:01 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:17:02 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=2000
trial=3
time=2026-06-29T22:17:13+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_2000_trial3/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:17:13 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:17:14 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=4000
trial=1
time=2026-06-29T22:17:25+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial1/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:17:25 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:17:26 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=4000
trial=2
time=2026-06-29T22:17:37+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial2/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:17:37 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:17:38 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=4000
trial=3
time=2026-06-29T22:17:49+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_4000_trial3/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:17:49 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:17:50 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=8000
trial=1
time=2026-06-29T22:18:01+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial1/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:18:01 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:18:02 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=8000
trial=2
time=2026-06-29T22:18:14+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial2/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:18:14 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:18:15 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=8000
trial=3
time=2026-06-29T22:18:26+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_8000_trial3/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:18:26 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:18:27 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=10000
trial=1
time=2026-06-29T22:18:38+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial1/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:18:38 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:18:39 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=10000
trial=2
time=2026-06-29T22:18:50+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial2/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:18:50 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:18:51 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=10000
trial=3
time=2026-06-29T22:19:02+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_10000_trial3/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:19:02 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:19:03 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=12000
trial=1
time=2026-06-29T22:19:14+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial1/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:19:14 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:19:15 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=12000
trial=2
time=2026-06-29T22:19:26+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial2/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:19:26 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:19:27 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=12000
trial=3
time=2026-06-29T22:19:38+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_12000_trial3/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:19:38 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:19:39 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=16000
trial=1
time=2026-06-29T22:19:50+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial1/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial1/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:19:50 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:19:51 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=16000
trial=2
time=2026-06-29T22:20:02+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial2/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial2/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:20:02 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:20:03 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=12000
sndbuf_requested=16000
trial=3
time=2026-06-29T22:20:14+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial3/rx.log --rcvbuf 12000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_12000_sndbuf_16000_trial3/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:20:14 [INFO] socket buffer option=SO_RCVBUF requested=12000 actual=24000
rcvbuf_actual=24000
sndbuf_line=2026-06-29 22:20:15 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=2000
trial=1
time=2026-06-29T22:20:26+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial1/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:20:26 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:20:27 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=2000
trial=2
time=2026-06-29T22:20:38+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial2/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:20:38 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:20:39 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=2000
trial=3
time=2026-06-29T22:20:50+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_2000_trial3/tx.log --sndbuf 2000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:20:50 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:20:51 [INFO] socket buffer option=SO_SNDBUF requested=2000 actual=4608
sndbuf_actual=4608
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=4000
trial=1
time=2026-06-29T22:21:02+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial1/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:21:02 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:21:03 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=4000
trial=2
time=2026-06-29T22:21:14+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial2/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:21:14 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:21:15 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=4000
trial=3
time=2026-06-29T22:21:26+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_4000_trial3/tx.log --sndbuf 4000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:21:26 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:21:27 [INFO] socket buffer option=SO_SNDBUF requested=4000 actual=8000
sndbuf_actual=8000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=8000
trial=1
time=2026-06-29T22:21:38+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial1/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:21:38 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:21:39 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=8000
trial=2
time=2026-06-29T22:21:50+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial2/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:21:50 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:21:51 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=8000
trial=3
time=2026-06-29T22:22:02+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_8000_trial3/tx.log --sndbuf 8000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:22:02 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:22:03 [INFO] socket buffer option=SO_SNDBUF requested=8000 actual=16000
sndbuf_actual=16000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=10000
trial=1
time=2026-06-29T22:22:14+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial1/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:22:14 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:22:15 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=10000
trial=2
time=2026-06-29T22:22:26+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial2/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:22:26 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:22:27 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=10000
trial=3
time=2026-06-29T22:22:38+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_10000_trial3/tx.log --sndbuf 10000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:22:38 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:22:39 [INFO] socket buffer option=SO_SNDBUF requested=10000 actual=20000
sndbuf_actual=20000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=12000
trial=1
time=2026-06-29T22:22:51+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial1/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:22:51 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:22:52 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=12000
trial=2
time=2026-06-29T22:23:03+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial2/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:23:03 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:23:04 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=12000
trial=3
time=2026-06-29T22:23:15+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_12000_trial3/tx.log --sndbuf 12000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:23:15 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:23:16 [INFO] socket buffer option=SO_SNDBUF requested=12000 actual=24000
sndbuf_actual=24000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=16000
trial=1
time=2026-06-29T22:23:27+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial1
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial1/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial1/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:23:27 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:23:28 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=16000
trial=2
time=2026-06-29T22:23:39+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial2
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial2/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial2/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:23:39 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:23:40 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok

rate_hz=18000
rcvbuf_requested=16000
sndbuf_requested=16000
trial=3
time=2026-06-29T22:23:51+09:00
run_dir=logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial3
rx_csv=data/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial3/rx.log --rcvbuf 16000 --link-name w08_socket_buffer_txrx_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_txrx_matrix/rate_18000_rcvbuf_16000_sndbuf_16000_trial3/tx.log --sndbuf 16000 --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-29 22:23:51 [INFO] socket buffer option=SO_RCVBUF requested=16000 actual=32000
rcvbuf_actual=32000
sndbuf_line=2026-06-29 22:23:52 [INFO] socket buffer option=SO_SNDBUF requested=16000 actual=32000
sndbuf_actual=32000
run_validity=ok
