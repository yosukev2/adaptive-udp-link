# W06 計測仕様

## 目的

W06 では、Raspberry Pi 5 Linux と Raspberry Pi Pico の 10ms 周期処理を同一の定義で記録し、後続 Issue #85、#86、#88 で比較可能な raw CSV と統計値を作る。本書は測定方法の仕様書であり、実測結果そのものは含めない。

## 比較対象

- `linux_rpi5`: Raspberry Pi 5 上の Linux ユーザー空間プログラム
- `pico`: Raspberry Pi Pico 上の Pico SDK / C or C++ firmware

Raspberry Pi 5 は Linux SBC、Raspberry Pi Pico は MCU である。ボード選定理由と役割差分は [board_selection.md](board_selection.md) を参照する。

## 固定条件

- 目標周期は `10ms = 10000us`
- 有効サンプル数は 1000 回
- Linux 側、Pico 側ともに raw CSV は共通スキーマを使う
- 後続の比較統計は `P50 / P95 / P99 / max / stddev` を必須とする
- 本 Issue では実機確認を行わない
- 本書や後続文書に未測定の値を実測値のように書かない

## サンプルの数え方

1 回の有効サンプルは、直前サンプルから今回サンプルまでの 1 区間を表す。`delta_us` と `jitter_us` を 1000 個そろえるため、実装は CSV 出力対象とは別に直前 timestamp を 1 個だけ内部保持してよい。

CSV のデータ行は 1000 行とし、`sample_index` は `1..1000` を使う。header 行は別扱いとする。

## 時刻とジッタの定義

- `timestamp_us`: 各周期イベント時点で取得した単調増加時刻。単位は us
- `delta_us`: `current_timestamp_us - previous_timestamp_us`
- `jitter_us = delta_us - 10000`
- 統計対象は `abs(jitter_us)`

`timestamp_us` は各デバイス内の単調増加時刻であり、Linux と Pico の timestamp 同士を絶対時刻として直接比較しない。比較対象は各環境で計算した `delta_us` と `jitter_us` である。

## 統計ルール

後続 Issue #88 では、各環境の 1000 サンプルについて `abs(jitter_us)` から次の統計値を出す。

- `P50`
- `P95`
- `P99`
- `max`
- `stddev`

追加ルール:

- percentile は既存 README の方針に合わせて nearest-rank を使う
- `stddev` は `abs(jitter_us)` の母標準偏差を使う
- `na` や欠損行は統計対象に入れない

## Raw CSV 共通スキーマ

列順は次の通りに固定する。

```text
env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

| column | type | meaning |
| --- | --- | --- |
| `env` | string | `linux_rpi5` または `pico` |
| `board` | string | `raspberry_pi_5` または `raspberry_pi_pico` |
| `sample_index` | integer | 1 始まりの連番。範囲は `1..1000` |
| `period_target_us` | integer | 固定値 `10000` |
| `timestamp_us` | integer | 各環境の単調増加 timestamp |
| `delta_us` | integer | 直前サンプルとの差分 us |
| `jitter_us` | integer | `delta_us - 10000` |

共通スキーマの運用ルール:

- Linux 側 raw CSV と Pico 側 raw CSV は同じ列順、同じ列名を使う
- 環境固有の追加情報は raw CSV に増やさず、`docs/w06_run_log.md` に記録する
- `timestamp_us` は `delta_us` 再計算ができる値であること
- `jitter_us` は CSV 出力時点で計算済みとする

## 実装制約

- Linux 側は単調増加 clock を使う
- Pico 側は hardware timer または repeating timer を使う
- Pico 側では timer callback / interrupt 内で timestamp をメモリへ保存する
- UART 出力、USB serial 出力は timer callback / interrupt 内で行わない
- Pico 側の CSV 出力は 1000 サンプル取得完了後に行う

serial 出力を interrupt 内で行わない理由は、I/O 処理時間や host 側の受信待ちが周期ジッタへ混入するのを避けるためである。

## 報告ルール

- 未測定の `X us / Y us` を結果欄へ書かない
- 実測後の比較文は raw CSV または生成した比較 CSV を根拠に書く
- W06 の主張範囲は UDP 遅延そのものではなく、UDP 遅延計測に混入し得る送信周期ジッタの比較に限定する
