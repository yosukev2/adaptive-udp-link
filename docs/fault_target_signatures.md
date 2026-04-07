# W03 fault-target 別シグネチャの最小確認

## 条件
- 実行手順: `bash scripts/run_fault_signatures.sh`
- link: Host loopback (`127.0.0.1`)
- trial: 各 target 1 回
- rate_hz: 30 frame/s
- tx_duration_sec: 3
- trial_summary duration_sec: 5
- tx_frames_per_datagram: 3
- payload_len: 48
- fault_rate: 0.50

## 比較表

| target | recv_ok | gap_est | crc_fail | len_invalid | preamble_miss | resync_count | Host補助 | 主シグネチャ |
|--------|--------:|--------:|---------:|------------:|--------------:|-------------:|----------|--------------|
| `preamble` | 41 | 44 | 0 | 0 | 21 | 39 | - | 共通 `trial_summary` では `header` と曖昧で、どちらも `preamble_miss + resync_count` 系になる |
| `payload_len` | 45 | 48 | 0 | 48 | 48 | 113 | - | `len_invalid` が最も分かりやすく、同時に `resync_count` も大きく増える |
| `header` | 45 | 46 | 0 | 0 | 48 | 113 | `bad_header=48` | 共通 `trial_summary` では `preamble` と曖昧で、Host補助ログがある場合だけ `bad_header` で切り分けられる |
| `crc` | 42 | 48 | 51 | 0 | 0 | 51 | - | `crc_fail` が増える |
| `payload` | 47 | 46 | 46 | 0 | 0 | 46 | - | `crc_fail` が増える |

## 読み方
- `crc` と `payload` は共通 `trial_summary` だけだと同型で、どちらも `crc_fail` 主体になる。
- `payload_len` は `len_invalid` が直接増えるので最も判別しやすい。
- `preamble` と `header` は共通 `trial_summary` だけだと同型で、どちらも `preamble_miss` と `resync_count` が主に増える。
- `header` を切り分けたい場合は Host 補助ログの `bad_header` が必要で、MCU/実リンクでは「header も疑う」までが共通面の説明範囲になる。

## 実測元
- `logs/fault_signatures/fault_signatures.csv`
