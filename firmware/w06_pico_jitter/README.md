# w06_pico_jitter

Issue #86 向けの Raspberry Pi Pico firmware 雛形です。Pico SDK / C を使い、`repeating_timer` で 10ms 周期の timestamp を 1000 回保存し、計測完了後に USB serial で CSV を出力します。

## 設計方針

- 周期条件は `10ms = 10000us`
- 有効サンプル数は 1000
- timer callback / interrupt 内では timer 由来の timestamp 保存と停止判定だけを行う
- `printf` / USB serial 出力は callback 内で行わず、計測完了後に main loop でまとめて実行する
- CSV 列は Issue #84 の共通スキーマに合わせる

出力 CSV ヘッダ:

```text
env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

`sample_index` は `1..1000`、`jitter_us = delta_us - 10000` です。Issue #84 のサンプル定義に合わせるため、CSV に出さない基準 timestamp を 1 回ぶんだけ内部保持します。

## ファイル

- `main.c`: timer callback と CSV 出力本体
- `CMakeLists.txt`: Pico SDK 向け standalone build 定義

## Build

前提:

- Pico SDK がインストール済み
- `PICO_SDK_PATH` が設定済み
- `arm-none-eabi-gcc` と `cmake` が利用可能

### 実機向け build

`picotool` が導入済みなら `UF2` まで生成します。

```bash
cmake -G Ninja -S firmware/w06_pico_jitter -B firmware/w06_pico_jitter/build
cmake --build firmware/w06_pico_jitter/build
```

### Windows ローカル検証用 build

`picotool` が未導入でも、`ELF` / `BIN` / `HEX` までの構文確認用 build はできます。
この開発機では `Ninja` generator の C compiler ABI try-compile が停止したため、Windows ローカル検証では `MinGW Makefiles` generator を使います。

```bash
cmake -G "MinGW Makefiles" -S firmware/w06_pico_jitter -B firmware/w06_pico_jitter/build-mingw -DW06_ENABLE_PICOTOOL=OFF
cmake --build firmware/w06_pico_jitter/build-mingw
```

想定成果物:

- 実機向け: `firmware/w06_pico_jitter/build/w06_pico_jitter.uf2`
- ローカル検証向け: `firmware/w06_pico_jitter/build-mingw/w06_pico_jitter.elf`

## Flash

USB mass storage 書き込みの想定手順:

1. Pico を `BOOTSEL` を押しながら USB 接続する
2. `RPI-RP2` として認識されたら `w06_pico_jitter.uf2` をコピーする
3. 自動再起動後、USB serial を開いて CSV を受信する

Linux 例:

```bash
cp firmware/w06_pico_jitter/build/w06_pico_jitter.uf2 /media/$USER/RPI-RP2/
```

## Serial Capture

この雛形は USB CDC serial を既定で使います。UART GPIO 配線は未設定です。

重要点:

- firmware 起動後 `2s` 待ってから計測を開始する
- callback 中の serial 出力は行わない
- 1000 サンプル取得後に header + 1000 行の CSV を一括出力する

Raspberry Pi 5 側の想定取得例:

```bash
mkdir -p data/w06
stty -F /dev/ttyACM0 115200 raw -echo -echoe -echok -icanon -isig -iexten -ixon -ixoff -icrnl -inlcr -opost
cat /dev/ttyACM0 > data/w06/pico_jitter_raw.csv
```

その後に Pico を reset または再接続して計測を開始します。USB CDC では baudrate が実質無視される構成もありますが、運用上は `115200` を記録値として残す想定です。

## 実機未確認事項

- Pico SDK/toolchain が対象実機環境で build 成功するか
- Pico への書き込み手順がそのまま通るか
- Raspberry Pi 5 側での USB serial device 名が `/dev/ttyACM0` になるか
- `data/w06/pico_jitter_raw.csv` に 1001 行が取得できるか
- UART 経由が必要な配線条件かどうか

実機確認コマンド案は [../../docs/w06_run_log.md](../../docs/w06_run_log.md) にまとめています。
