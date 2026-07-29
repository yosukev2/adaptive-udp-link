# MCU UART Baseline Runbook

## 目的

Issue #194 の実機 baseline を取得するための手順を固定する。dry-run は実装検証には
使えるが、正常通信 baseline の完了条件には含めない。

手順 1 から 13 まで順に実行する。各手順の「期待結果」を確認してから次へ進む。
途中で失敗した場合、その手順の「失敗したら」に従い、後の手順へは進まない。

手順 10 以降は `$TRIAL` と `$CAPTURE_PID` を引き継ぐため、**同じ terminal で続けて
実行する**。手順 8 で一度 Pi 5 を落とすので、shell 変数の設定は手順 10 から始まる。

## 用意するもの

| 品目 | 数 | 備考 |
|------|---:|------|
| Raspberry Pi 5 | 1 | |
| Raspberry Pi Pico | 1 | ピンヘッダがはんだ付け済みであること |
| ジャンパーワイヤ メス-メス | 3 | 色を分けると挿し間違いを防げる |
| USB ケーブル (Pico - Pi 5) | 1 | **データ線入り**。給電専用は不可 |

Pico にピンヘッダが付いていない場合は、先にはんだ付けが必要。

## 実行環境

| 手順 | 実行場所 |
|------|----------|
| 1 - 3 | 任意の PC。Windows でも可 |
| 4 - 13 | **Pi 5 上のみ**。実機 device が必要 |

手順 1 - 3 はソフトウェアだけで完結するので、配線前にどこでも先に潰しておける。
コマンドは bash 表記。Windows PowerShell で実行する場合は各手順の
「PowerShell の場合」を使う。`\` の行継続、`column`、`<` は PowerShell では動かない。

---

## 手順 1: リポジトリと Python の準備

Pi 5 上でリポジトリを最新にし、`pyserial` を入れる。

```bash
cd ~/adaptive-udp-link
git pull
python -m pip install pyserial
python -c "import serial; print(serial.__version__)"
```

PowerShell の場合:

```powershell
git pull
python -m pip install pyserial
python -c "import serial; print(serial.__version__)"
```

期待結果: version が表示される。

失敗したら: `python3 -m pip install pyserial` を試す。`externally-managed-environment`
エラーなら `python3 -m pip install --break-system-packages pyserial` か venv を使う。

---

## 手順 2: dry-run で harness を確認

配線前に、PC 側の harness と summary 生成だけを先に通しておく。ここが通らなければ
実機に進んでも切り分けが増えるだけ。

```bash
python scripts/mcu_uart/pc_harness.py \
  --dry-run \
  --trial-id m0_dryrun_001 \
  --packet-count 10 \
  --payload-len 16 \
  --output-dir logs/mcu_uart/m0_dryrun_001

python scripts/mcu_uart/generate_summary.py \
  --input-dir logs/mcu_uart/m0_dryrun_001 \
  --output logs/mcu_uart/m0_dryrun_001/summary.csv \
  --note "dry-run only; no MCU hardware observed"

column -s, -t < logs/mcu_uart/m0_dryrun_001/summary.csv
```

PowerShell の場合（1 行ずつ実行する）:

```powershell
python scripts/mcu_uart/pc_harness.py --dry-run --trial-id m0_dryrun_001 --packet-count 10 --payload-len 16 --output-dir logs/mcu_uart/m0_dryrun_001

python scripts/mcu_uart/generate_summary.py --input-dir logs/mcu_uart/m0_dryrun_001 --output logs/mcu_uart/m0_dryrun_001/summary.csv --note "dry-run only; no MCU hardware observed"

Import-Csv logs/mcu_uart/m0_dryrun_001/summary.csv | Format-List
```

期待結果:

- `pc_tx_log.csv` に header + 10 行
- `summary.csv` の `pass_fail` が `TEMPLATE_ONLY`
- `hardware_observed=false`

---

## 手順 3: parser のホストテスト

firmware に載せる前に、パーサ単体を host で検証する。

```bash
make -C firmware/mcu_uart_link test
```

PowerShell の場合（`make` が無いので直接ビルドする）:

```powershell
gcc -std=c11 -Wall -Wextra -Werror -O2 -g -o firmware/mcu_uart_link/test_mcu_uart_protocol.exe firmware/mcu_uart_link/test_mcu_uart_protocol.c firmware/mcu_uart_link/mcu_uart_protocol.c

.\firmware\mcu_uart_link\test_mcu_uart_protocol.exe
```

期待結果: `All MCU UART protocol tests passed`

失敗したら: firmware を焼かない。パーサ側の問題なので先に直す。

---

## 手順 4: Pi 5 の UART を有効化

GPIO UART を有効にし、serial console を無効にする。console が有効なままだと OS が
同じ port を掴んで harness と衝突する。

```bash
sudo raspi-config
#   3 Interface Options -> I6 Serial Port
#     "login shell accessible over serial?"  -> No
#     "serial port hardware enabled?"        -> Yes
sudo reboot
```

再起動後に確認する。

```bash
ls -l /dev/ttyAMA0
grep -E "enable_uart|console=serial" /boot/firmware/config.txt /boot/firmware/cmdline.txt
```

期待結果: `/dev/ttyAMA0` が存在し、`cmdline.txt` に `console=serial0` が**無い**。

失敗したら: `/boot/firmware/config.txt` に `enable_uart=1` を追記して再起動。

---

## 手順 5: Pi 5 単体でループバック確認

Pico を繋ぐ前に、Pi 側の UART だけを確認する。**この確認をしておくと、後で失敗した
ときに原因が Pi 設定か配線/Pico かに絞れる。**

ジャンパ 1 本で **pin 8 と pin 10 を直結**する。

```bash
python3 -c "
import serial, time
s = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
s.write(b'hello'); time.sleep(0.2); print(s.read(5))
s.close()
"
```

期待結果: `b'hello'` が返る。

失敗したら: 配線ではなく手順 4 の設定問題。`b''` なら console が port を掴んでいる
可能性が高いので `sudo systemctl stop serial-getty@ttyAMA0.service` を試す。

確認できたらループバックのジャンパを外す。

---

## 手順 6: firmware をビルド

```bash
export PICO_SDK_PATH=/path/to/pico-sdk        # 例: /home/pi5/pico/pico-sdk
cmake -G Ninja -S firmware/mcu_uart_link -B firmware/mcu_uart_link/build
cmake --build firmware/mcu_uart_link/build
ls -l firmware/mcu_uart_link/build/mcu_uart_link.uf2
```

期待結果: `mcu_uart_link.uf2` が生成される。

失敗したら: `picotool` の UF2 変換で落ちる場合、ELF/BIN は生成されている。
`picotool` を別途インストールするか、`-DMCU_UART_LINK_ENABLE_PICOTOOL=OFF` で
再 configure して BIN から UF2 を作る。

---

## 手順 7: firmware を書き込む

Pico の **BOOTSEL ボタンを押しながら** USB を挿す。押したまま挿し、挿してから離す。

```bash
lsblk | grep RPI-RP2 || ls /media/$USER/
cp firmware/mcu_uart_link/build/mcu_uart_link.uf2 /media/$USER/RPI-RP2/
sync
```

期待結果: コピー後に Pico が自動で再起動し、`RPI-RP2` ドライブが消える。

失敗したら: `RPI-RP2` が見えないなら BOOTSEL のタイミングか、USB ケーブルが
給電専用。ケーブルを替えて再試行する。

---

## 手順 8: 配線する

**Pi 5 の電源を切ってから**配線する。TX と RX はクロスする。

```bash
sudo shutdown -h now
```

| Pi 5 | 物理 pin | 向き | Pico | 物理 pin |
|------|---------:|:----:|------|---------:|
| GPIO14 (TXD) | 8 | -> | GPIO1 (RX) | 2 |
| GPIO15 (RXD) | 10 | <- | GPIO0 (TX) | 1 |
| GND | 6 | -- | GND | 3 |

Pi 5 の pin 6 / 8 / 10 は**基板の外周側の列**にあり、pin 1 側の端から数えて
3・4・5 番目。Pico の pin 1/2/3 は USB を上にしたとき左列の上から 3 本。

**3.3V と 5V は繋がない。線は 3 本だけ。** Pi の pin 2 / pin 4 は 5V なので、
pin 6 の数え間違いは Pico の破損に直結する。数えたら一度確認する。

配線後、Pico の USB を Pi 5 の USB port に挿してから Pi 5 を起動する。

---

## 手順 9: device を確認

```bash
ls -l /dev/ttyAMA0 /dev/ttyACM0
```

期待結果: 両方存在する。`/dev/ttyAMA0` が packet link、`/dev/ttyACM0` が
Pico の USB CDC (telemetry)。

失敗したら: `/dev/ttyACM0` が無い場合は firmware が焼けていないか、USB ケーブルが
給電専用。手順 7 に戻る。

---

## 手順 10: telemetry の capture を開始

firmware は USB CDC 接続を最大 10 秒待ってから CSV header を 1 回出力し、その後
200 ms 周期で行を追記する。**harness より先に capture を開始する。**

```bash
TRIAL=m0_baseline_001
mkdir -p logs/mcu_uart/$TRIAL
stty -F /dev/ttyACM0 raw -echo
cat /dev/ttyACM0 > logs/mcu_uart/$TRIAL/mcu_telemetry.csv &
CAPTURE_PID=$!
sleep 3
head -1 logs/mcu_uart/$TRIAL/mcu_telemetry.csv
```

期待結果: `trial_id,mono_ms,state,...` という header 行が表示される。

失敗したら: header が出ないなら Pico を reset（USB を挿し直す）して、capture を
開始してから 10 秒以内に接続が確立するようにする。

---

## 手順 11: harness を実行

```bash
python scripts/mcu_uart/pc_harness.py \
  --port /dev/ttyAMA0 \
  --baudrate 115200 \
  --trial-id $TRIAL \
  --test-name m0_baseline_10pkt \
  --firmware-version "$(git rev-parse --short HEAD)" \
  --packet-count 10 \
  --payload-len 16 \
  --output-dir logs/mcu_uart/$TRIAL
```

期待結果: エラーなく終了する。

`--firmware-version` に commit を入れておくと、後から firmware と log を対応付け
られる。USB-serial アダプタ経由なら `--port /dev/ttyUSB0` にする。

---

## 手順 12: capture を停止して中身を確認

```bash
kill "$CAPTURE_PID"
wc -l logs/mcu_uart/$TRIAL/pc_tx_log.csv \
      logs/mcu_uart/$TRIAL/pc_rx_log.csv \
      logs/mcu_uart/$TRIAL/mcu_telemetry.csv
tail -1 logs/mcu_uart/$TRIAL/mcu_telemetry.csv
```

期待結果:

- `pc_tx_log.csv` が 11 行 (header + 10)
- `pc_rx_log.csv` が 11 行 (header + ACK 10)
- `mcu_telemetry.csv` の最終行が `state=RUN`、`rx_data_count=10`

`pc_rx_log.csv` が header だけなら ACK が返っていない。手順 8 のクロス配線を疑う。

---

## 手順 13: summary を生成して判定

```bash
python scripts/mcu_uart/generate_summary.py \
  --input-dir logs/mcu_uart/$TRIAL \
  --output logs/mcu_uart/$TRIAL/summary.csv \
  --note "M0 no-fault 10 packet baseline"

column -s, -t < logs/mcu_uart/$TRIAL/summary.csv
```

期待結果: `pass_fail=PASS` かつ `hardware_observed=true`。

---

## PASS 条件

- `sent_count=10`
- `received_count=10`
- `crc_error_count=0`
- `seq_gap_count=0`
- `duplicate_count=0`
- `overflow_count=0`
- `buffer_miss_count=0`
- `unrecovered_count=0`
- `safe_enter_count=0`
- `hardware_observed=true`
- `pass_fail=PASS`

---

## FAIL 時の切り分け

まず `mcu_telemetry.csv` の最終行の `last_error_code` を見る。

| code | 意味 | 主に疑う箇所 |
|-----:|------|--------------|
| 0 | OK | telemetry 以外。`pc_rx_log.csv` を見る |
| 1 | BAD_PREAMBLE | baudrate 不一致、配線、GND 未共有 |
| 2 | BAD_VERSION | protocol version 不一致 |
| 3 | BAD_TYPE | packet type 不一致 |
| 4 | BAD_LENGTH | length の endian |
| 5 | BAD_CRC | CRC 対象範囲か endian の不一致 |
| 6 | SEQ_GAP | 取りこぼし。baudrate か buffer |
| 7 | DUPLICATE | 再送または seq 初期化漏れ |
| 9 | BUFFER_OVERFLOW | 受信が追いつかない |

症状別:

| 症状 | 疑う箇所 |
|------|----------|
| `pc_rx_log.csv` が header だけ | TX/RX がクロスされていない |
| `rx_byte_count=0` | 配線、GND、Pi 側 console が port を掴んでいる |
| 文字化けのような preamble miss が大量 | baudrate 不一致 |
| `/dev/ttyACM0` が無い | firmware 未書き込み、USB ケーブルが給電専用 |

---

## 付録: Windows から実行する場合

Pico を Windows PC に直結し、USB-serial アダプタ経由で packet link を張る構成。

```powershell
python -m pip install pyserial
python scripts/mcu_uart/pc_harness.py `
  --port COM5 `
  --baudrate 115200 `
  --trial-id m0_baseline_001 `
  --packet-count 10 `
  --payload-len 16 `
  --output-dir logs/mcu_uart/m0_baseline_001
```

MCU telemetry を別経路で保存する場合は、同じ trial directory に
`mcu_telemetry.csv` として置く。
