# W06 Bring-up Log Template

この文書は Issue #91 向けの記録テンプレートです。Raspberry Pi 5 と Raspberry Pi Pico を接続したときの立ち上げ確認、Pico 書き込み確認、USB serial 疎通確認を漏れなく残すために使います。

## 記録ルール

- この文書内の `コマンド例` は未実行です。実際に使ったコマンドは `実行コマンド` 欄へ記録してください。
- 実行結果は捏造せず、実際の出力をそのまま貼るか、要点を要約して元ログの保存先を併記してください。
- 未確認の項目は空欄のままにするか、`未確認` と明記してください。
- 実機到着前にこのテンプレートを事前記入する場合でも、確認済みとは書かないでください。

## 1. セッション概要

| 項目 | 記録 |
| --- | --- |
| 実施日 |  |
| 実施者 |  |
| 関連 Issue | #91 |
| 参照している後続 Issue | #85, #86 |
| Raspberry Pi 5 |  |
| Raspberry Pi 5 OS イメージ |  |
| Raspberry Pi Pico |  |
| 接続方法 | USB serial / UART GPIO / その他 |
| 電源構成 |  |
| 保存した補助ログ/写真/メモの場所 |  |

## 2. 完了チェック

- [ ] Raspberry Pi 5 の起動確認を記録した
- [ ] `uname -a`、`gcc --version`、`python3 --version` の結果を記録した
- [ ] Raspberry Pi 5 上で C プログラムの build/run 確認を記録した
- [ ] Pico SDK / toolchain の確認を記録した
- [ ] `blink` / `hello_serial` 等のサンプル firmware build 確認を記録した
- [ ] Pico 書き込み確認を記録した
- [ ] `/dev/ttyACM*` 認識確認を記録した
- [ ] serial 出力読み取り確認を記録した
- [ ] 詰まった箇所と対処内容を記録した
- [ ] #85 / #86 に進めるかの判定を記録した

## 3. Raspberry Pi 5 起動確認

### 目的

- Raspberry Pi 5 が起動し、操作可能なシェルまたはログイン画面まで到達できることを記録する

### コマンド例（未実行）

```bash
hostnamectl
uptime
```

### 実測記録

| 項目 | 記録 |
| --- | --- |
| 起動確認の方法 | HDMI / SSH / serial console / その他 |
| 電源投入時刻 |  |
| ログイン到達時刻 |  |
| ログイン方法 |  |
| ホスト名 |  |
| ネットワーク状態メモ |  |
| 判定 | Pass / Fail / 未確認 |

### 起動時メモ

```text

```

## 4. Raspberry Pi 5 環境情報

### コマンド例（未実行）

```bash
uname -a
gcc --version
python3 --version
```

### 4.1 `uname -a`

- 実行日時:
- 実行コマンド:
- 判定: Pass / Fail / 未確認
- 出力:

```text

```

### 4.2 `gcc --version`

- 実行日時:
- 実行コマンド:
- 判定: Pass / Fail / 未確認
- 出力:

```text

```

### 4.3 `python3 --version`

- 実行日時:
- 実行コマンド:
- 判定: Pass / Fail / 未確認
- 出力:

```text

```

## 5. C プログラム build/run 確認

### 目的

- Raspberry Pi 5 上で C の build と実行ができることを確認し、Issue #85 の実装着手可否を判断できるようにする

### コマンド例（未実行）

```bash
make all
make test
```

必要なら、このリポジトリ以外の最小 C プログラムで確認してもよいです。その場合は使ったソースファイルと保存場所を記録してください。

### 実測記録

| 項目 | 記録 |
| --- | --- |
| 確認対象 | 例: `make all`, `make test`, 最小 hello.c など |
| 対象リビジョン |  |
| 実行ディレクトリ |  |
| build コマンド |  |
| run / test コマンド |  |
| 生成物または実行対象 |  |
| 判定 | Pass / Fail / 未確認 |
| ログ保存先 |  |

### build 出力

```text

```

### run / test 出力

```text

```

## 6. Pico SDK / Toolchain 確認

### 目的

- Pico 向け firmware を build する前提環境が揃っているかを記録し、Issue #86 の着手可否を判断できるようにする

### コマンド例（未実行）

```bash
cmake --version
ninja --version
arm-none-eabi-gcc --version
echo "$PICO_SDK_PATH"
```

### 実測記録

| 項目 | 記録 |
| --- | --- |
| セットアップ方法 | パッケージ / ソース checkout / その他 |
| `cmake` |  |
| `ninja` |  |
| `arm-none-eabi-gcc` |  |
| `PICO_SDK_PATH` |  |
| 追加で必要だった設定 |  |
| 判定 | Pass / Fail / 未確認 |
| ログ保存先 |  |

### 出力メモ

```text

```

## 7. サンプル firmware build 確認

### 目的

- `blink`、`hello_serial` などの既知サンプルを build できることを確認し、Pico 側 build 系の詰まりを先に潰す

### コマンド例（未実行）

```bash
cmake -S <pico-examples-dir> -B <build-dir> -DPICO_BOARD=pico
cmake --build <build-dir> --target blink
cmake --build <build-dir> --target hello_serial
```

### 実測記録

| サンプル | ソース場所 | build ディレクトリ | build コマンド | 生成物 | 判定 | メモ |
| --- | --- | --- | --- | --- | --- | --- |
| `blink` |  |  |  |  | Pass / Fail / 未確認 |  |
| `hello_serial` |  |  |  |  | Pass / Fail / 未確認 |  |

### build 出力メモ

```text

```

## 8. Pico 書き込み確認

### 目的

- build した firmware を Pico に書き込みできることを確認する

### コマンド例（未実行）

```bash
cp <firmware>.uf2 <mount-point>/RPI-RP2/
picotool info
```

### 実測記録

| 項目 | 記録 |
| --- | --- |
| 書き込んだ firmware |  |
| 書き込み方法 | BOOTSEL + UF2 copy / picotool / その他 |
| マウントポイントまたは使用デバイス |  |
| 書き込み時刻 |  |
| 書き込み後の再起動確認 |  |
| 判定 | Pass / Fail / 未確認 |
| ログ保存先 |  |

### 書き込み時メモ

```text

```

## 9. `/dev/ttyACM*` 認識確認

### 目的

- Raspberry Pi 5 から Pico が USB serial device として見えているかを確認する

### コマンド例（未実行）

```bash
ls /dev/ttyACM*
dmesg | tail -n 50
udevadm info -qn /dev/ttyACM0
```

### 実測記録

| 項目 | 記録 |
| --- | --- |
| 確認時刻 |  |
| 実行コマンド |  |
| 認識したデバイス名 | 例: `/dev/ttyACM0` |
| `dmesg` の要点 |  |
| `udevadm` の要点 |  |
| 判定 | Pass / Fail / 未確認 |
| ログ保存先 |  |

### 出力メモ

```text

```

## 10. serial 出力読み取り確認

### 目的

- Raspberry Pi 5 側で Pico の serial 出力を読めることを確認する

### コマンド例（未実行）

```bash
stty -F /dev/ttyACM0 115200 raw -echo
timeout 5 cat /dev/ttyACM0
python3 -m serial.tools.miniterm /dev/ttyACM0 115200
```

### 実測記録

| 項目 | 記録 |
| --- | --- |
| 対象デバイス |  |
| 使用 firmware |  |
| 使用ツール | `cat`, `miniterm`, `screen`, `picocom` など |
| 実行コマンド |  |
| baudrate / line setting |  |
| 期待した出力 |  |
| 実際に見えた出力の要点 |  |
| 判定 | Pass / Fail / 未確認 |
| ログ保存先 |  |

### serial 出力

```text

```

## 11. 詰まった場合の記録

| 時刻 | 症状 | 直前にやったこと | 切り分け内容 | 次に試すこと | 状態 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | Open / Resolved |

## 12. 未確認事項

- 実機が未到着で未確認の項目:
- 実機到着後に追加で確認する項目:
- 補助機材や追加パッケージが必要ならその内容:

## 13. 後続 Issue への進行判定

| Issue | 判定 | 根拠 | 足りないもの |
| --- | --- | --- | --- |
| #85 Raspberry Pi 5 Linux 側の 10ms ジッタログ | Go / Hold / No-Go | Raspberry Pi 5 起動、環境情報、C build/run の確認結果を書く |  |
| #86 Pico の hardware timer 10ms ジッタログ | Go / Hold / No-Go | Pico SDK/toolchain、sample build、書き込み、`/dev/ttyACM*`、serial 読み取りの確認結果を書く |  |

## 14. 引き継ぎメモ

- 次に着手する人への注意点:
- 再現に必要なコマンド一覧:
- 保存したログやスクリーンショットの場所:
