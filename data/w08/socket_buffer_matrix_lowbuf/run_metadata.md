date=2026-06-28T21:50:34+09:00
host=Linux pi5 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
branch=issue-131-w08-socket-buffer-matrix
commit=fac1520cb25e2f30a9c0f18cd6acebf6a05903cd
lo=lo               UNKNOWN        127.0.0.1/8 ::1/128
socket_buf_defaults=212992/212992
purpose=socket_buffer_matrix_sweep
buffer_option=SO_RCVBUF
rates=10000 14000 18000
requested_rcvbufs=8192 16384 32768 49152 65536 98304
trials=1 2 3
fixed_conditions=loopback 127.0.0.1:9000 payload_len=48 tx_duration_sec=10 rx_duration_sec=12 recovery_mode=fsm no_affinity sndbuf_default

rate_hz=10000
rcvbuf_requested=8192
trial=1
time=2026-06-28T21:50:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial1/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:50:34 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=10000
rcvbuf_requested=8192
trial=2
time=2026-06-28T21:50:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial2/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:50:46 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=10000
rcvbuf_requested=8192
trial=3
time=2026-06-28T21:50:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial3/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_8192_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:50:58 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=10000
rcvbuf_requested=16384
trial=1
time=2026-06-28T21:51:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial1/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:51:10 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=10000
rcvbuf_requested=16384
trial=2
time=2026-06-28T21:51:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial2/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:51:22 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=10000
rcvbuf_requested=16384
trial=3
time=2026-06-28T21:51:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial3/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_16384_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:51:34 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=10000
rcvbuf_requested=32768
trial=1
time=2026-06-28T21:51:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial1/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:51:46 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=10000
rcvbuf_requested=32768
trial=2
time=2026-06-28T21:51:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial2/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:51:58 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=10000
rcvbuf_requested=32768
trial=3
time=2026-06-28T21:52:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial3/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_32768_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:52:10 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=10000
rcvbuf_requested=49152
trial=1
time=2026-06-28T21:52:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial1/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:52:22 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=10000
rcvbuf_requested=49152
trial=2
time=2026-06-28T21:52:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial2/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:52:34 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=10000
rcvbuf_requested=49152
trial=3
time=2026-06-28T21:52:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial3/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_49152_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:52:46 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=10000
rcvbuf_requested=65536
trial=1
time=2026-06-28T21:52:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:52:58 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=10000
rcvbuf_requested=65536
trial=2
time=2026-06-28T21:53:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:53:10 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=10000
rcvbuf_requested=65536
trial=3
time=2026-06-28T21:53:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:53:22 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=10000
rcvbuf_requested=98304
trial=1
time=2026-06-28T21:53:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial1/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:53:34 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=10000
rcvbuf_requested=98304
trial=2
time=2026-06-28T21:53:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial2/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:53:46 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=10000
rcvbuf_requested=98304
trial=3
time=2026-06-28T21:53:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial3/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 10000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_10000_rcvbuf_98304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:53:58 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=14000
rcvbuf_requested=8192
trial=1
time=2026-06-28T21:54:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial1/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:54:10 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=14000
rcvbuf_requested=8192
trial=2
time=2026-06-28T21:54:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial2/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:54:22 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=14000
rcvbuf_requested=8192
trial=3
time=2026-06-28T21:54:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial3/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_8192_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:54:34 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=14000
rcvbuf_requested=16384
trial=1
time=2026-06-28T21:54:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial1/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:54:46 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=14000
rcvbuf_requested=16384
trial=2
time=2026-06-28T21:54:58+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial2/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:54:58 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=14000
rcvbuf_requested=16384
trial=3
time=2026-06-28T21:55:10+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial3/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_16384_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:55:10 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=14000
rcvbuf_requested=32768
trial=1
time=2026-06-28T21:55:22+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial1/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:55:22 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=14000
rcvbuf_requested=32768
trial=2
time=2026-06-28T21:55:34+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial2/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:55:34 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=14000
rcvbuf_requested=32768
trial=3
time=2026-06-28T21:55:46+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial3/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_32768_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:55:46 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=14000
rcvbuf_requested=49152
trial=1
time=2026-06-28T21:55:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial1/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:55:59 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=14000
rcvbuf_requested=49152
trial=2
time=2026-06-28T21:56:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial2/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:56:11 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=14000
rcvbuf_requested=49152
trial=3
time=2026-06-28T21:56:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial3/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_49152_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:56:23 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=14000
rcvbuf_requested=65536
trial=1
time=2026-06-28T21:56:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:56:35 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=14000
rcvbuf_requested=65536
trial=2
time=2026-06-28T21:56:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:56:47 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=14000
rcvbuf_requested=65536
trial=3
time=2026-06-28T21:56:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:56:59 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=14000
rcvbuf_requested=98304
trial=1
time=2026-06-28T21:57:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial1/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:57:11 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=14000
rcvbuf_requested=98304
trial=2
time=2026-06-28T21:57:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial2/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:57:23 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=14000
rcvbuf_requested=98304
trial=3
time=2026-06-28T21:57:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial3/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 14000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_14000_rcvbuf_98304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:57:35 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=18000
rcvbuf_requested=8192
trial=1
time=2026-06-28T21:57:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial1/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:57:47 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=18000
rcvbuf_requested=8192
trial=2
time=2026-06-28T21:57:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial2/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:57:59 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=18000
rcvbuf_requested=8192
trial=3
time=2026-06-28T21:58:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial3/rx.log --rcvbuf 8192 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_8192_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:58:11 [INFO] socket buffer option=SO_RCVBUF requested=8192 actual=16384
rcvbuf_actual=16384
run_validity=ok

rate_hz=18000
rcvbuf_requested=16384
trial=1
time=2026-06-28T21:58:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial1/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:58:23 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=18000
rcvbuf_requested=16384
trial=2
time=2026-06-28T21:58:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial2/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:58:35 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=18000
rcvbuf_requested=16384
trial=3
time=2026-06-28T21:58:47+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial3/rx.log --rcvbuf 16384 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_16384_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:58:47 [INFO] socket buffer option=SO_RCVBUF requested=16384 actual=32768
rcvbuf_actual=32768
run_validity=ok

rate_hz=18000
rcvbuf_requested=32768
trial=1
time=2026-06-28T21:58:59+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial1/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:58:59 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=18000
rcvbuf_requested=32768
trial=2
time=2026-06-28T21:59:11+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial2/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:59:11 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=18000
rcvbuf_requested=32768
trial=3
time=2026-06-28T21:59:23+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial3/rx.log --rcvbuf 32768 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_32768_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:59:23 [INFO] socket buffer option=SO_RCVBUF requested=32768 actual=65536
rcvbuf_actual=65536
run_validity=ok

rate_hz=18000
rcvbuf_requested=49152
trial=1
time=2026-06-28T21:59:35+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial1/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:59:35 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=18000
rcvbuf_requested=49152
trial=2
time=2026-06-28T21:59:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial2/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 21:59:48 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=18000
rcvbuf_requested=49152
trial=3
time=2026-06-28T22:00:00+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial3/rx.log --rcvbuf 49152 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_49152_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:00:00 [INFO] socket buffer option=SO_RCVBUF requested=49152 actual=98304
rcvbuf_actual=98304
run_validity=ok

rate_hz=18000
rcvbuf_requested=65536
trial=1
time=2026-06-28T22:00:12+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:00:12 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=18000
rcvbuf_requested=65536
trial=2
time=2026-06-28T22:00:24+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:00:24 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=18000
rcvbuf_requested=65536
trial=3
time=2026-06-28T22:00:36+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/rx.log --rcvbuf 65536 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_65536_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:00:36 [INFO] socket buffer option=SO_RCVBUF requested=65536 actual=131072
rcvbuf_actual=131072
run_validity=ok

rate_hz=18000
rcvbuf_requested=98304
trial=1
time=2026-06-28T22:00:48+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial1
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_run1.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial1/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 1 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial1/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial1/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial1/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:00:48 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=18000
rcvbuf_requested=98304
trial=2
time=2026-06-28T22:01:00+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial2
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_run2.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial2/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 2 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial2/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial2/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial2/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:01:00 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok

rate_hz=18000
rcvbuf_requested=98304
trial=3
time=2026-06-28T22:01:12+09:00
run_dir=logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial3
rx_csv=data/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_run3.csv
rx_cmd=./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 12 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial3/rx.log --rcvbuf 98304 --link-name w08_socket_buffer_matrix --trial 3 --csv-in-1sec-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial3/rx_1sec.csv --csv-by-1recv-log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial3/rx_by_1recv.csv --recovery-mode fsm
tx_cmd=./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 18000 --duration-sec 10 --log-path logs/w08/socket_buffer_matrix/rate_18000_rcvbuf_98304_trial3/tx.log --payload-len 48 --version 1
tx_status=0
rx_status=0
copy_status=0
rcvbuf_line=2026-06-28 22:01:12 [INFO] socket buffer option=SO_RCVBUF requested=98304 actual=196608
rcvbuf_actual=196608
run_validity=ok
