# W06 ボード選定

## 結論

W06 では、Linux 側の比較対象として Raspberry Pi 5、MCU 側の比較対象として Raspberry Pi Pico を使う。これは同型ボードの性能比較ではなく、Linux SBC と bare-metal MCU の周期処理ジッタを同じ 10ms 条件で比較するための選定である。

## 役割差分

| board | class | role in W06 | note |
| --- | --- | --- | --- |
| `Raspberry Pi 5` | Linux SBC | Linux 側 baseline | MCU ではない。OS scheduler、割り込み、バックグラウンド処理の影響を含む |
| `Raspberry Pi Pico` | MCU | bare-metal 側 baseline | OS scheduler を持たない MCU として hardware timer の挙動を測る |

Raspberry Pi 5 は Linux SBC、Raspberry Pi Pico は MCU である。この差分自体が W06 の比較前提であり、Raspberry Pi 5 を bare-metal 比較対象として扱わない。

## Raspberry Pi Pico を使う理由

- Pico SDK が整備されており、Pico SDK / C or C++ で hardware timer を直接扱える
- MCU としての実装経路が明確で、timer callback、timestamp 保存、CSV 出力の責務を分離しやすい
- USB serial を使って計測後に CSV を取り出しやすい
- 1000 サンプルぶんの timestamp を RAM に保持してから後出しできるため、計測中の I/O を避けやすい
- W06 の論点である「汎用 OS 上の周期処理」と「MCU timer ベースの周期処理」を分けて説明しやすい

## MicroPython を使わない理由

W06 の目的は、Linux の周期実行と MCU の bare-metal timer 実行を比較することであり、言語ランタイムやインタプリタの揺らぎを比較することではない。そのため Pico 側は MicroPython ではなく Pico SDK / C or C++ を使う。

MicroPython を採用しない理由:

- interpreter dispatch の実行時間が周期ジッタに混入する
- garbage collection や動的確保の停止時間が周期性を乱し得る
- REPL や runtime の補助処理が timer 起点の挙動を見えにくくする
- timer callback で何をしているかを C/C++ より厳密に制御しにくい

Pico SDK / C or C++ を使うことで、後続 Issue #86 では timer callback では timestamp 保存だけを行い、CSV 化や serial 出力は計測完了後に回す、という設計を明確に維持できる。

## UART / USB serial 出力方針

UART 出力や USB serial 出力は timer interrupt 内で行わない。これは USB host 側の受信待ち、serial FIFO の空き状況、driver 処理時間が割り込み処理へ混ざると、測りたい周期ジッタではなく I/O 待ち時間を測ることになるためである。

W06 の Pico 側方針は次の通り。

- timer callback / interrupt では timestamp を RAM に保存する
- 1000 サンプル取得後に計測を止める
- 停止後に main loop 側から UART または USB serial で CSV を出力する

## 非スコープ

- この文書は実機の在庫、配線、USB device 名を確定しない
- この文書は実測結果を主張しない
- `Linux は P99 が X us`、`Pico は Y us` のような未測定値は書かない

実機の疎通確認は Issue #91、Linux 側ログ取得は Issue #85、Pico 側ログ取得は Issue #86、統計比較は Issue #88 で実施する。
