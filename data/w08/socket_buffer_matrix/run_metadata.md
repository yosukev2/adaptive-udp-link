date=2026-06-28T19:13:21+09:00
host=Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
branch=issue-131-w08-socket-buffer-matrix
commit=b6984d8cb770aa7a9bfd6ceed600bb1eb0658288
lo=lo               UNKNOWN        127.0.0.1/8 ::1/128
socket_buf_defaults=212992/212992
purpose=socket_buffer_matrix_sweep
buffer_option=SO_RCVBUF
rates=10000 12000 14000 16000 18000 20000
requested_rcvbufs=65536 262144 1048576 4194304 8388608 16777216
trials=1 2 3
fixed_conditions=loopback 127.0.0.1:9000 payload_len=48 tx_duration_sec=10 rx_duration_sec=12 recovery_mode=fsm no_affinity sndbuf_default

rate_hz=10000
rcvbuf_requested=65536
trial=1
time=2026-06-28T19:13:21+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:13:21 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=10000
rcvbuf_requested=65536
trial=2
time=2026-06-28T19:13:33+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:13:33 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=10000
rcvbuf_requested=65536
trial=3
time=2026-06-28T19:13:45+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:13:45 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=10000
rcvbuf_requested=262144
trial=1
time=2026-06-28T19:13:57+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial1/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:13:57 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=262144
trial=2
time=2026-06-28T19:14:09+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial2/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:14:09 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=262144
trial=3
time=2026-06-28T19:14:21+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial3/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_262144_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:14:21 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=1048576
trial=1
time=2026-06-28T19:14:33+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial1/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:14:33 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=1048576
trial=2
time=2026-06-28T19:14:45+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial2/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:14:45 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=1048576
trial=3
time=2026-06-28T19:14:57+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial3/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_1048576_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:14:57 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=4194304
trial=1
time=2026-06-28T19:15:09+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial1/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:15:09 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=4194304
trial=2
time=2026-06-28T19:15:21+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial2/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:15:21 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=4194304
trial=3
time=2026-06-28T19:15:33+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial3/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_4194304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:15:33 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=8388608
trial=1
time=2026-06-28T19:15:45+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial1/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:15:45 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=8388608
trial=2
time=2026-06-28T19:15:57+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial2/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:15:57 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=8388608
trial=3
time=2026-06-28T19:16:09+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial3/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8388608_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:16:09 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=16777216
trial=1
time=2026-06-28T19:16:21+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial1/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:16:21 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=16777216
trial=2
time=2026-06-28T19:16:33+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial2/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:16:33 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=10000
rcvbuf_requested=16777216
trial=3
time=2026-06-28T19:16:45+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial3/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16777216_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:16:45 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=65536
trial=1
time=2026-06-28T19:16:57+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:16:57 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=12000
rcvbuf_requested=65536
trial=2
time=2026-06-28T19:17:09+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:17:09 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=12000
rcvbuf_requested=65536
trial=3
time=2026-06-28T19:17:21+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:17:21 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=12000
rcvbuf_requested=262144
trial=1
time=2026-06-28T19:17:33+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial1/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:17:33 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=262144
trial=2
time=2026-06-28T19:17:45+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial2/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:17:45 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=262144
trial=3
time=2026-06-28T19:17:57+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial3/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_262144_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:17:57 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=1048576
trial=1
time=2026-06-28T19:18:09+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial1/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:18:09 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=1048576
trial=2
time=2026-06-28T19:18:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial2/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:18:22 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=1048576
trial=3
time=2026-06-28T19:18:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial3/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_1048576_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:18:34 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=4194304
trial=1
time=2026-06-28T19:18:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial1/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:18:46 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=4194304
trial=2
time=2026-06-28T19:18:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial2/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:18:58 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=4194304
trial=3
time=2026-06-28T19:19:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial3/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_4194304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:19:10 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=8388608
trial=1
time=2026-06-28T19:19:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial1/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:19:22 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=8388608
trial=2
time=2026-06-28T19:19:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial2/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:19:34 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=8388608
trial=3
time=2026-06-28T19:19:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial3/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_8388608_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:19:46 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=16777216
trial=1
time=2026-06-28T19:19:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial1/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:19:58 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=16777216
trial=2
time=2026-06-28T19:20:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial2/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:20:10 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=12000
rcvbuf_requested=16777216
trial=3
time=2026-06-28T19:20:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial3/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 12000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_12000_rcvbuf_16777216_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:20:22 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=65536
trial=1
time=2026-06-28T19:20:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:20:34 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=14000
rcvbuf_requested=65536
trial=2
time=2026-06-28T19:20:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:20:46 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=14000
rcvbuf_requested=65536
trial=3
time=2026-06-28T19:20:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:20:58 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=14000
rcvbuf_requested=262144
trial=1
time=2026-06-28T19:21:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial1/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:21:10 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=262144
trial=2
time=2026-06-28T19:21:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial2/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:21:22 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=262144
trial=3
time=2026-06-28T19:21:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial3/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_262144_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:21:34 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=1048576
trial=1
time=2026-06-28T19:21:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial1/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:21:46 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=1048576
trial=2
time=2026-06-28T19:21:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial2/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:21:58 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=1048576
trial=3
time=2026-06-28T19:22:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial3/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_1048576_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:22:10 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=4194304
trial=1
time=2026-06-28T19:22:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial1/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:22:22 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=4194304
trial=2
time=2026-06-28T19:22:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial2/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:22:34 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=4194304
trial=3
time=2026-06-28T19:22:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial3/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_4194304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:22:46 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=8388608
trial=1
time=2026-06-28T19:22:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial1/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:22:58 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=8388608
trial=2
time=2026-06-28T19:23:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial2/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:23:10 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=8388608
trial=3
time=2026-06-28T19:23:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial3/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8388608_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:23:22 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=16777216
trial=1
time=2026-06-28T19:23:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial1/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:23:34 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=16777216
trial=2
time=2026-06-28T19:23:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial2/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:23:46 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=14000
rcvbuf_requested=16777216
trial=3
time=2026-06-28T19:23:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial3/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16777216_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:23:58 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=65536
trial=1
time=2026-06-28T19:24:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:24:10 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=16000
rcvbuf_requested=65536
trial=2
time=2026-06-28T19:24:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:24:23 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=16000
rcvbuf_requested=65536
trial=3
time=2026-06-28T19:24:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:24:35 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=16000
rcvbuf_requested=262144
trial=1
time=2026-06-28T19:24:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial1/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:24:47 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=262144
trial=2
time=2026-06-28T19:24:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial2/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:24:59 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=262144
trial=3
time=2026-06-28T19:25:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial3/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_262144_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:25:11 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=1048576
trial=1
time=2026-06-28T19:25:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial1/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:25:23 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=1048576
trial=2
time=2026-06-28T19:25:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial2/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:25:35 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=1048576
trial=3
time=2026-06-28T19:25:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial3/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_1048576_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:25:47 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=4194304
trial=1
time=2026-06-28T19:25:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial1/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:25:59 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=4194304
trial=2
time=2026-06-28T19:26:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial2/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:26:11 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=4194304
trial=3
time=2026-06-28T19:26:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial3/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_4194304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:26:23 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=8388608
trial=1
time=2026-06-28T19:26:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial1/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:26:35 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=8388608
trial=2
time=2026-06-28T19:26:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial2/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:26:47 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=8388608
trial=3
time=2026-06-28T19:26:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial3/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_8388608_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:26:59 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=16777216
trial=1
time=2026-06-28T19:27:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial1/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:27:11 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=16777216
trial=2
time=2026-06-28T19:27:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial2/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:27:23 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=16000
rcvbuf_requested=16777216
trial=3
time=2026-06-28T19:27:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial3/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 16000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_16000_rcvbuf_16777216_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:27:35 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=65536
trial=1
time=2026-06-28T19:27:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:27:47 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=18000
rcvbuf_requested=65536
trial=2
time=2026-06-28T19:27:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:27:59 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=18000
rcvbuf_requested=65536
trial=3
time=2026-06-28T19:28:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:28:11 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=18000
rcvbuf_requested=262144
trial=1
time=2026-06-28T19:28:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial1/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:28:23 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=262144
trial=2
time=2026-06-28T19:28:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial2/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:28:35 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=262144
trial=3
time=2026-06-28T19:28:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial3/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_262144_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:28:47 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=1048576
trial=1
time=2026-06-28T19:28:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial1/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:28:59 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=1048576
trial=2
time=2026-06-28T19:29:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial2/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:29:11 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=1048576
trial=3
time=2026-06-28T19:29:24+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial3/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_1048576_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:29:24 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=4194304
trial=1
time=2026-06-28T19:29:36+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial1/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:29:36 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=4194304
trial=2
time=2026-06-28T19:29:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial2/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:29:48 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=4194304
trial=3
time=2026-06-28T19:30:00+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial3/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_4194304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:30:00 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=8388608
trial=1
time=2026-06-28T19:30:12+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial1/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:30:12 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=8388608
trial=2
time=2026-06-28T19:30:24+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial2/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:30:24 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=8388608
trial=3
time=2026-06-28T19:30:36+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial3/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8388608_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:30:36 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=16777216
trial=1
time=2026-06-28T19:30:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial1/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:30:48 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=16777216
trial=2
time=2026-06-28T19:31:00+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial2/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:31:00 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=18000
rcvbuf_requested=16777216
trial=3
time=2026-06-28T19:31:12+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial3/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16777216_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:31:12 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=65536
trial=1
time=2026-06-28T19:31:24+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:31:24 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=20000
rcvbuf_requested=65536
trial=2
time=2026-06-28T19:31:36+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:31:36 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=20000
rcvbuf_requested=65536
trial=3
time=2026-06-28T19:31:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:31:48 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=20000
rcvbuf_requested=262144
trial=1
time=2026-06-28T19:32:00+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial1/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:32:00 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=262144
trial=2
time=2026-06-28T19:32:12+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial2/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:32:12 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=262144
trial=3
time=2026-06-28T19:32:24+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial3/rx.log --rcvbuf 262144 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_262144_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:32:24 [INFO] socket buffer option=SO_RCVBUF requested=262144 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=1048576
trial=1
time=2026-06-28T19:32:36+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial1/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:32:36 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=1048576
trial=2
time=2026-06-28T19:32:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial2/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:32:48 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=1048576
trial=3
time=2026-06-28T19:33:00+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial3/rx.log --rcvbuf 1048576 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_1048576_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:33:00 [INFO] socket buffer option=SO_RCVBUF requested=1048576 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=4194304
trial=1
time=2026-06-28T19:33:12+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial1/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:33:12 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=4194304
trial=2
time=2026-06-28T19:33:24+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial2/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:33:24 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=4194304
trial=3
time=2026-06-28T19:33:36+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial3/rx.log --rcvbuf 4194304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_4194304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:33:36 [INFO] socket buffer option=SO_RCVBUF requested=4194304 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=8388608
trial=1
time=2026-06-28T19:33:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial1/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:33:48 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=8388608
trial=2
time=2026-06-28T19:34:01+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial2/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:34:01 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=8388608
trial=3
time=2026-06-28T19:34:13+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial3/rx.log --rcvbuf 8388608 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_8388608_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:34:13 [INFO] socket buffer option=SO_RCVBUF requested=8388608 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=16777216
trial=1
time=2026-06-28T19:34:25+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial1/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:34:25 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=16777216
trial=2
time=2026-06-28T19:34:37+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial2/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:34:37 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok

rate_hz=20000
rcvbuf_requested=16777216
trial=3
time=2026-06-28T19:34:49+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial3/rx.log --rcvbuf 16777216 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 20000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_20000_rcvbuf_16777216_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 19:34:49 [INFO] socket buffer option=SO_RCVBUF requested=16777216 actual=425984
rcvbuf_actual=425984
run_validity=ok
