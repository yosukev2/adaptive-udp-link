# MCU UART Link Bring-up Triage

## 目的

Pi 5 と Pico の UART リンクが繋がらないときに、原因を1箇所に絞り込む手順。
`docs/mcu_uart/baseline_runbook.md` の手順 9 以降で通信が成立しない場合に使う。

## 進め方

1. **段階 0 から順に実行する。** 各段階の PASS 基準を満たしてから次へ進む
2. **失敗した段階で止まる。** その先の段階は前提が崩れているので実行しても情報が得られない
3. **一度に1つだけ変える。** 複数の配線を同時に動かすと、どの操作が効いたか分からなくなる

## 前提知識

| 事項 | 内容 |
|------|------|
| GND | Pico の USB を Pi に挿していれば GND は共通。GND 線が無くても通信は成立する |
| ファントム給電 | Pi が GPIO に 3.3V を出したまま Pico の USB を抜くと、保護ダイオード経由で Pico が中途半端に通電し、USB 列挙も BOOTSEL も失敗する。**Pico の電源を抜く前に必ずジャンパを外す** |
| 列挙とメインループ | USB は割り込みで処理されるため、メインループが停止してもデバイスノードは残る。`/dev/ttyACM0` の存在は firmware 正常動作の証明にならない |
| 送信カウンタ | `heartbeat_sent_count` が増えるのは送信関数を呼んだ証拠であり、信号がピンから出た証明ではない |

---

## 段階 0: 既知の正常状態に戻す

**ジャンパを全て外す。** そのうえで Pico の USB を抜き、5 秒待って挿し直す。

```bash
bash scripts/mcu_uart/telemetry_snapshot.sh
```

PASS 基準: 行が表示され、再実行すると `mono_ms` が増えている。

FAIL の場合: firmware が動いていない。`/dev/ttyACM0` が無ければ USB ケーブルを交換。
ノードはあるのに行が出ないならメインループが停止しているので、BOOTSEL で書き直す。

---

## 段階 1: Pi 単体の UART

ジャンパ 1 本で **Pi の pin 7 (GPIO4) と pin 29 (GPIO5) を直結**する。Pico には繋がない。

```bash
python3 scripts/mcu_uart/uart_loopback_check.py /dev/ttyAMA2
```

PASS 基準: `RESULT: PASS`

FAIL の場合: Pi 側の問題。`dtoverlay=uart2-pi5` が `config.txt` にあるか、
追記後に再起動したか、`serial-getty` が port を掴んでいないかを確認する。

```bash
grep -n uart /boot/firmware/config.txt
systemctl is-active serial-getty@ttyAMA2.service
```

---

## 段階 2: ジャンパ線を 1 本ずつ

段階 1 と同じ短絡を、**使用予定の線それぞれ**で行う。線を替えて 3 本とも試す。

```bash
python3 scripts/mcu_uart/uart_loopback_check.py /dev/ttyAMA2
```

PASS 基準: 全ての線で `RESULT: PASS`

FAIL の場合: その線が断線している。除外して別の線を使う。
**この段階を省略しない。** 導通する線と断線した線は外見で区別できない。

---

## 段階 3: Pico 自己ループバック

Pi 側の線を全て外し、**Pico の `GP0` と `GP1` だけ**をジャンパ 1 本で直結する。
`GND` (pin 3) には触れない。GP0 を GND に短絡すると送信が返らなくなり、
メインループが停止する。

HEARTBEAT 有効版の firmware が必要。

```bash
cmake -S firmware/mcu_uart_link -B firmware/mcu_uart_link/build -DMCU_UART_HEARTBEAT_MS=500
cmake --build firmware/mcu_uart_link/build
```

書き込み後、少し待ってから確認する。

```bash
bash scripts/mcu_uart/telemetry_snapshot.sh
```

PASS 基準: `rx_byte_count` が増加し、`rx_packet_count` も増える。
Pico が自分の HEARTBEAT を自分で受信している状態。

FAIL の場合: **Pico の GP0/GP1 が機能していない。** Pi も配線も関与しない試験なので、
結果がそのまま結論になる。UART0 の代替ピン (GP12/GP13、GP16/GP17) へ移すか、
基板を交換する。

---

## 段階 4: Pico から Pi への片方向

自己ループバックの線を外し、**Pico `GP0` → Pi pin 29** の 1 本だけ繋ぐ。

```bash
stty -F /dev/ttyAMA2 115200 raw -echo
timeout 3 cat /dev/ttyAMA2 | od -t x1 | head -4
```

PASS 基準: `a5 5a c3 3c 01 11` で始まる 16 バイトが 500ms 周期で並ぶ。
`a55ac33c` が preamble、`01` が version、`11` が HEARTBEAT の type。

FAIL の場合: 段階 2・3 が PASS していれば、線の挿し位置が誤っている。
Pico 側はシルク印刷の `GP0` ラベルを直接確認する。

---

## 段階 5: Pi から Pico への片方向

段階 4 の線に加えて **Pi pin 7 → Pico `GP1`** を繋ぐ。

```bash
python3 -c "import serial;serial.Serial('/dev/ttyAMA2',115200).write(b'U'*512)"
bash scripts/mcu_uart/telemetry_snapshot.sh
```

PASS 基準: `rx_byte_count` が 512 以上増える。
`U` は有効な preamble ではないので `preamble_miss_count` も増えるが、それでよい。
ここで確認したいのはバイトが届くかどうかだけ。

FAIL の場合: 段階 2・3 が PASS していれば、`GP1` への挿し位置の誤り。

---

## 段階 6: 全結線して baseline

HEARTBEAT を無効化した firmware に戻す。baseline のログを DATA と ACK だけにするため。

```bash
cmake -S firmware/mcu_uart_link -B firmware/mcu_uart_link/build -DMCU_UART_HEARTBEAT_MS=0
cmake --build firmware/mcu_uart_link/build
```

書き込み後、`docs/mcu_uart/baseline_runbook.md` の手順 10 から再開する。

---

## 配線表

| 信号 | Pi 5 物理 pin | 向き | Pico ラベル | Pico 物理 pin |
|------|-------------:|:----:|-------------|-------------:|
| TX -> RX | 7 (GPIO4) | -> | `GP1` | 2 |
| RX <- TX | 29 (GPIO5) | <- | `GP0` | 1 |
| GND | 9 | -- | `GND` | 3 |

Pi の 7 / 9 / 29 は内側の列 (奇数 pin)。Pico の 1/2/3 は USB を上にして左列の上から
3 本だが、**物理位置を数えるよりシルク印刷のラベルで確認するほうが確実**。

## 記録

原因が判明したら `docs/mcu_uart/baseline_runbook.md` の該当手順に反映する。
同じ問題を次回も踏まないための更新であり、この triage 文書自体も追記して育てる。
