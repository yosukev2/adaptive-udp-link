# W06 Pico Jitter Run Log

Issue #86 の Pico hardware timer jitter logger 実装と検証記録です。

Raspberry Pi Pico上でPico SDKのrepeating timerを用いて10ms周期のtimestampを1000回記録し、計測完了後にUSB CDC経由でCSV出力しました。Raspberry Pi 5側でCSVとして保存し、期待する1001行のデータを取得できることを確認しました。

## 状態

* firmware source 追加: 完了
* Windows ローカル開発機での Pico SDK build: 完了
* Raspberry Pi 5上での Pico SDK build / UF2生成: 完了
* Picoへのfirmware書き込み: 完了
* Raspberry Pi 5でのUSB serial認識: 完了
* `data/w06/pico_jitter_raw.csv` 保存: 完了
* CSV行数・スキーマ確認: 完了

## 共通 CSV スキーマ

Issue #84 に合わせて、保存先CSVは次の列順を使用する。

```text
env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

計測条件:

* 目標周期: `10000 us`（10ms）
* 保存サンプル数: `1000`
* 期待行数: `1001`（header 1行 + data 1000行）
* jitter定義: `jitter_us = delta_us - 10000`

## 実装方針

Pico側では、10ms周期のrepeating timer callback内で `time_us_64()` によるtimestamp取得とメモリ配列への保存のみを実行する。

USB CDCへのCSV出力は1000回のtimestamp記録完了後に `emit_csv()` でまとめて実行する。これにより、serial出力処理による遅延を計測中のtimer callbackへ混入させない。

USB CDC出力でCSVの各行間に空行が挿入される現象が発生したため、以下を設定して改行変換を無効化した。

```c
stdio_init_all();
stdio_set_translate_crlf(&stdio_usb, false);
```

修正後、CSVが1001行で取得できることを確認した。

## Windows ローカルbuild確認

Windowsローカル開発機では、次の環境でfirmware sourceのbuildを確認した。

* `PICO_SDK_PATH=C:\pico\pico-sdk`
* `arm-none-eabi-gcc` 導入済み
* `cmake` 導入済み
* `ninja` 導入済み
* `picotool` 未導入

`picotool` 未導入のため、Windows上では `W06_ENABLE_PICOTOOL=OFF` として `.elf` / `.bin` / `.hex` の生成を確認した。

```bash
cmake -G "MinGW Makefiles" -S firmware/w06_pico_jitter -B firmware/w06_pico_jitter/build-mingw -DW06_ENABLE_PICOTOOL=OFF
cmake --build firmware/w06_pico_jitter/build-mingw
```

確認結果:

* 実施日: 2026-06-02
* 結果: 成功
* 生成物: `build-mingw/w06_pico_jitter.elf`, `build-mingw/w06_pico_jitter.bin`, `build-mingw/w06_pico_jitter.hex`

補足:

* `cmake -G Ninja ... -DW06_ENABLE_PICOTOOL=OFF` は C compiler ABI の try-compile で停止した
* `arm-none-eabi-gcc` 単体のcompile / linkは成功した
* Windowsローカル検証では `MinGW Makefiles` generator を使用した
* UF2生成と実機確認はRaspberry Pi 5側で実施した

## Raspberry Pi 5 実機build・書き込み・CSV取得

### 環境

* Host: Raspberry Pi 5
* Target MCU: Raspberry Pi Pico
* Firmware framework: Pico SDK / C
* Firmware source: `firmware/w06_pico_jitter/main.c`
* Build definition: `firmware/w06_pico_jitter/CMakeLists.txt`
* 実行スクリプト: `scripts/run_w06_pico_jitter.sh`
* Flash方式: Pico BOOTSEL / UF2コピー
* Serial interface: USB CDC ACM
* Serial device: `/dev/ttyACM0`
* Baudrate: USB CDCのため未使用
* CSV保存先: `data/w06/pico_jitter_raw.csv`

### Pico SDKパス設定

Raspberry Pi 5上のPico SDKパスを環境変数に設定した。

```bash
echo 'export PICO_SDK_PATH=/home/pi5/pico/pico-sdk' >> ~/.bashrc
source ~/.bashrc
echo $PICO_SDK_PATH
```

確認値:

```text
/home/pi5/pico/pico-sdk
```

### 実行コマンド

PicoをBOOTSELモードでUSB接続した状態で、以下を実行した。

```bash
./scripts/run_w06_pico_jitter.sh
```

このスクリプトでは以下を実行する。

1. BOOTSELデバイス `RPI-RP2` の確認
2. firmwareのCMake configure / build
3. `.uf2` の生成確認
4. PicoへのUF2コピーと再起動
5. `/dev/ttyACM0` からのUSB CDC出力取得
6. `data/w06/pico_jitter_raw.csv` への保存
7. 行数と先頭・末尾データの表示

### 実行結果

```text
1001 data/w06/pico_jitter_raw.csv
env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
pico,raspberry_pi_pico,1,10000,2021752,9998,-2
pico,raspberry_pi_pico,999,10000,12001752,10000,0
pico,raspberry_pi_pico,1000,10000,12011752,10000,0
Saved: data/w06/pico_jitter_raw.csv
```

## 検証

### CSV行数

```bash
wc -l data/w06/pico_jitter_raw.csv
```

結果:

```text
1001 data/w06/pico_jitter_raw.csv
```

判定:

* header: 1行
* data: 1000行
* 合計: 1001行
* 期待値と一致

### CSVヘッダ

```bash
head -n 1 data/w06/pico_jitter_raw.csv
```

結果:

```text
env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

判定:

* Issue #84 の共通CSVスキーマと一致

### sample index

確認コマンド:

```bash
awk -F, '
NR > 1 { count++; last=$3 }
NR == 2 { first=$3 }
END {
    print "sample_count=" count
    print "first_index=" first
    print "last_index=" last
}' data/w06/pico_jitter_raw.csv
```

期待結果:

```text
sample_count=1000
first_index=1
last_index=1000
```

### CSV列数

確認コマンド:

```bash
awk -F, '
NF != 7 { bad++ }
END { print "invalid_rows=" bad+0 }
' data/w06/pico_jitter_raw.csv
```

期待結果:

```text
invalid_rows=0
```

### jitter定義

確認コマンド:

```bash
awk -F, '
NR > 1 && $7 != ($6 - 10000) { bad++ }
END { print "jitter_mismatch_rows=" bad+0 }
' data/w06/pico_jitter_raw.csv
```

期待結果:

```text
jitter_mismatch_rows=0
```

### interrupt内のserial出力禁止

実装では、`capture_timer_callback()` 内で以下のみを実行する。

* `time_us_64()` によるtimestamp取得
* `captured_timestamps_us[]` への保存
* count / 完了フラグの更新

CSV出力処理 `emit_csv()` は、1000サンプル取得後に `main()` 側から呼び出す。

判定:

* timer callback / interrupt中にserial出力を行わない設計となっている

## Issue #86 完了判定

* [x] Pico SDKでfirmwareをbuildできる
* [x] Picoへfirmwareを書き込める
* [x] 10ms周期で1000回timestampを保存できる
* [x] 計測完了後にCSVをserial出力できる
* [x] Raspberry Pi 5側でPicoログをCSV保存できる
* [x] CSV列がIssue #84の共通スキーマに一致している
* [x] interrupt内でserial出力していない
* [x] 実行ログを `docs/w06_run_log.md` に記録している
