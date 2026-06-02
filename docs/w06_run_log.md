# W06 Pico Jitter Run Log

Issue #86 の Pico hardware timer jitter logger 実装と検証記録です。現時点では firmware source を追加し、Windows ローカル開発機で Pico SDK build を確認済みです。Pico への書き込みと Raspberry Pi 5 側での serial CSV 取得は未確認です。

## 状態

- firmware source 追加: 完了
- ローカル開発機での Pico SDK build: 完了
- Pico 書き込み: 未確認
- Raspberry Pi 5 での USB serial 認識: 未確認
- `data/w06/pico_jitter_raw.csv` 保存: 未確認

## 共通 CSV スキーマ

Issue #84 に合わせて、保存先 CSV は次の列順を使います。

```text
env,board,sample_index,period_target_us,timestamp_us,delta_us,jitter_us
```

期待行数:

- header 1 行
- data 1000 行
- 合計 1001 行

## ローカル build 確認

この開発機では次のパスを確認済みです。

- `PICO_SDK_PATH=C:\pico\pico-sdk`
- `arm-none-eabi-gcc` は導入済み
- `cmake` は導入済み
- `ninja` は導入済み
- `picotool` は未導入

そのため、`W06_ENABLE_PICOTOOL=OFF` でのローカル build を確認対象にします。

```bash
cmake -G "MinGW Makefiles" -S firmware/w06_pico_jitter -B firmware/w06_pico_jitter/build-mingw -DW06_ENABLE_PICOTOOL=OFF
cmake --build firmware/w06_pico_jitter/build-mingw
```

確認結果:

- 2026-06-02: 成功
- 生成物: `build-mingw/w06_pico_jitter.elf`, `build-mingw/w06_pico_jitter.bin`, `build-mingw/w06_pico_jitter.hex`

原因調査:

- `cmake -G Ninja -S firmware/w06_pico_jitter -B firmware/w06_pico_jitter/build-codex -DW06_ENABLE_PICOTOOL=OFF` は C compiler ABI の try-compile で停止した
- 停止箇所は `CMakeFiles/CMakeScratch/TryCompile-*/CMakeCCompilerABI.c` の Ninja build
- `arm-none-eabi-gcc` 単体の compile は成功した
- `arm-none-eabi-gcc` 単体の link は成功した
- `cmd.exe /C` 経由で同じ ARM GCC link コマンドを実行しても成功した
- 一方で `ninja -C ... cmTC_*.elf` は完了せず、Ninja process が CPU 0 のまま残った
- `cmake -G "MinGW Makefiles" ... -DW06_ENABLE_PICOTOOL=OFF` と `cmake --build ...` は完了した

判定:

- firmware source 自体ではなく、この Windows 開発機の `CMake 4.2.1 + Ninja 1.13.2 + Arm GNU Toolchain 13.3.Rel1` の try-compile 経路でハングしている
- Windows ローカル検証では `MinGW Makefiles` generator を使う
- 実機向け UF2 生成、Pico 書き込み、serial CSV 取得は Raspberry Pi 5 側または `picotool` 導入済み環境で確認する

## 想定 flash コマンド

Pico を `BOOTSEL` で mount した後の例:

```bash
cp firmware/w06_pico_jitter/build/w06_pico_jitter.uf2 /media/$USER/RPI-RP2/
```

確認結果:

- 2026-05-17: 未確認

## 想定 serial 取得手順

Issue #91 の接続確認が終わっている前提です。device 名は実機依存のため、ここでは `/dev/ttyACM0` を仮置きしています。

```bash
mkdir -p data/w06
stty -F /dev/ttyACM0 115200 raw -echo -echoe -echok -icanon -isig -iexten -ixon -ixoff -icrnl -inlcr -opost
cat /dev/ttyACM0 > data/w06/pico_jitter_raw.csv
```

その後に Pico を reset または再接続して 2 秒待ち、CSV を吐かせます。

確認結果:

- 2026-05-17: 未確認

## 実機で確認すべき項目

- `build/w06_pico_jitter.uf2` が生成されること
- Pico 起動後、約 10 秒で 1000 サンプル取得が完了すること
- `pico_jitter_raw.csv` の header が Issue #84 の列順と一致すること
- `wc -l data/w06/pico_jitter_raw.csv` が `1001` を返すこと
- timer callback / interrupt 中に serial 出力していないことをコードレビューと実測挙動の両方で確認すること
