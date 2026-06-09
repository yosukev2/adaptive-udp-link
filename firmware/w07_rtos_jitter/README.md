# w07_rtos_jitter

Issue #101 向けの Raspberry Pi Pico firmware です。bare-metal の単一ループ構成と、FreeRTOS のタスク分離構成で送信イベントの周期ジッタを比較します。

## ビルドターゲット

- `w07_baremetal_jitter`: 単一ループ内で絶対時刻基準の 10ms 周期処理と受信模擬負荷を実行する
- `w07_freertos_jitter`: `tx_task`、`rx_task`、`state_task` を FreeRTOS の Queue/Semaphore で連携させる

両ターゲットとも CSV 出力には USB CDC serial を使います。W07 では GPIO UART 配線は不要です。

## 計測ルール

- 目標周期: `10000 us`
- サンプル数: 1000
- 計測中の timestamp はメモリへ保存する
- タイミングが重要な計測処理内では `printf` しない
- CSV は計測完了後にまとめて出力する
- Pico SDK と FreeRTOS-Kernel は外部依存として扱い、このリポジトリにはコミットしない

## CSV スキーマ

bare-metal 版:

```text
mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

FreeRTOS 版:

```text
mode,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us,queue_latency_us,deadline_miss_count
```

`queue_latency_us` は次の差分です。

```text
state_task_receive_time_us - tx_task_queue_send_time_us
```

特殊値:

- `-1`: Queue への送信失敗
- `-2`: 完了処理までに Queue event を受信できなかった

## ビルド

前提:

- Pico SDK がリポジトリ外にインストールされている
- FreeRTOS-Kernel がリポジトリ外に配置されている
- `PICO_SDK_PATH` が Pico SDK を指している
- `FREERTOS_KERNEL_PATH` が FreeRTOS-Kernel を指している
- `arm-none-eabi-gcc`、CMake、対応する generator が利用できる

実行例:

```bash
export PICO_SDK_PATH=/home/pi5/pico/pico-sdk
export FREERTOS_KERNEL_PATH=/home/pi5/pico/FreeRTOS-Kernel
cmake -G Ninja -S firmware/w07_rtos_jitter -B firmware/w07_rtos_jitter/build
cmake --build firmware/w07_rtos_jitter/build
```

想定される UF2 出力:

- `firmware/w07_rtos_jitter/build/w07_baremetal_jitter.uf2`
- `firmware/w07_rtos_jitter/build/w07_freertos_jitter.uf2`

## 現在の状態

Issue #101 の範囲は firmware の正式配置とビルド定義の追加までです。Pico 実機での実行と CSV 取得は、後続の W07 Issue で実施します。
