<!-- FILE: docs/issues/W01_ISSUE_03_frame_v0.md -->

# W01 / Issue #3
# Frame v0定義（frame.h）+ サイズ検証 + v0ルール固定

## 親Issue

- EPIC: W01 - UDP基礎通信基盤の構築（Frame v0 + 計測基礎） #1

## 目的

送受信の共通言語（Frame v0）を固定し、以降の拡張（v1, v2...）に耐える土台を作る。  
`timestamp` をどこに置くか、`seq` をなぜ入れるかをコードと仕様の両方で明確化する。

## このIssueのスコープ

- `include/frame.h` を作成
- Frame v0 の最小フィールドを定義
  - `seq`: `uint32_t`（単調増加）
  - `timestamp_ns`: `uint64_t`（送信側が付与、単位 ns）
  - `payload`: 固定長（v0）
- サイズ/レイアウト検証（`_Static_assert`, `offsetof`）
- tx/rx 起動時ログに `sizeof(FrameV0)` 等を出力
- v0ルール（バイトオーダー、padding/ABI差の扱い）を明文化

## アウトオブスコープ

- UDP送受信本体
- seq更新ロジック
- timestamp付与実装
- latency算出 / drop推定
- serialize/deserialize 実装
- htonl/ntohl の実適用
- packed属性の導入による最適化検討

## 成果物（期待）

- `include/frame.h`
- `src/tx.c`（`frame.h` include + 起動時 frame情報ログ）
- `src/rx.c`（`frame.h` include + 起動時 frame情報ログ）
- 本ドキュメント（Frame v0仕様と設計ルールの明文化）

## Frame v0 仕様（固定）

### フィールド定義

- `seq` (`uint32_t`)
  - 送信ごとに単調増加するシーケンス番号
  - 受信側で seq 欠損ベースの drop推定に使う（W01後半で使用）
- `timestamp_ns` (`uint64_t`)
  - 送信側が付与する送信時刻
  - 単位は ns（nanoseconds）
  - W01ではローカル検証前提の相対遅延確認用途
- `payload` (`uint8_t[FRAME_V0_PAYLOAD_BYTES]`)
  - v0の固定長ペイロード
  - 後続Issueで内容を埋める前提の領域

### v0 定数

- `FRAME_V0_PAYLOAD_BYTES = 48`

### 想定レイアウト（v0）

- `offsetof(FrameV0, seq) == 0`
- `offsetof(FrameV0, timestamp_ns) == 8`
- `offsetof(FrameV0, payload) == 16`
- `sizeof(FrameV0) == 64`

注記:
- `seq` (4 byte) の後に、`timestamp_ns` (8 byte) のアライメント都合で padding が入る想定
- packed は使わず、自然アライメント + static assert で検証する

## 設計ルール（v0で固定すること）

### バイトオーダー方針

- v0はローカル検証前提のため、ホストバイトオーダーを許容する
- v0での目的は「共通レイアウト固定」と「計測基礎の土台づくり」
- 将来（v1+）は手動 serialize/deserialize + network byte order を基本方針とする

### 構造体直送の扱い

- v0では同一ホスト / 同一ABI前提で構造体直送を一旦許容
- ただし以下の理由でネットワーク越しにそのまま送ると壊れる可能性がある
  - padding
  - endianness（バイトオーダー）
  - ABI差 / アライメント差

### packed の扱い

- v0では packed を使わない
- 理由:
  - paddingの存在を学習/可視化したい
  - 将来は packed ではなく serialize で解決する方針のため

## 学習ポイント（このIssueで押さえること）

### ロジック要素

- 「構造体をそのまま送る」と壊れる可能性がある理由
  - padding / endianness / ABI差
- v0で割り切る設計と、将来拡張に備える設計のトレードオフ

### 暗記要素（最低限）

- 固定幅整数型
  - `uint32_t`, `uint64_t`
- `offsetof`
- `_Static_assert`
- `htonl/ntohl` の存在と役割（今回は未適用）

## 受入条件（AC）

- [ ] `include/frame.h` が作成されている
- [ ] `FrameV0` に `seq(uint32_t)` / `timestamp_ns(uint64_t)` / 固定長payload が定義されている
- [ ] `tx.c` と `rx.c` が `frame.h` を include している
- [ ] `_Static_assert` / `offsetof` によるサイズ/レイアウト検証がある
- [ ] 起動時ログに `sizeof(FrameV0)` を出力できる
- [ ] 起動時ログに payload bytes / offsets を出力できる（推奨、実装済みならACに含める）
- [ ] Frame v0 の仕様（フィールド/意味/単位）がコメントまたはドキュメントに明文化されている
- [ ] v0のバイトオーダー方針と将来方針が明文化されている

## テスト手順（Issue #3）

### 1) ビルド

~~~bash
make clean && make
~~~

確認:
- ビルド成功
- `bin/tx`, `bin/rx` 生成
- `frame.h` の static assert によるエラーなし

### 2) ログ用ディレクトリ準備（手動実行）

~~~bash
mkdir -p logs
~~~

### 3) rx 起動（frame情報ログ確認）

~~~bash
./bin/rx --port 9000 --duration-sec 1 --log-path logs/rx_frame_check.log
~~~

### 4) rx ログ確認

~~~bash
tail -n +1 logs/rx_frame_check.log
~~~

確認:
- `frame_v0 sizeof=... payload_bytes=... offsets(...)` が出る
- 期待値に一致する（想定: `sizeof=64`, `payload_bytes=48`, `seq=0`, `ts=8`, `payload=16`）

### 5) tx 起動（frame情報ログ確認）

~~~bash
./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 100 --duration-sec 1 --log-path logs/tx_frame_check.log
~~~

### 6) tx ログ確認

~~~bash
tail -n +1 logs/tx_frame_check.log
~~~

確認:
- tx 側でも `frame_v0 ...` が出る
- rx と同じ値が出る

### 7) 10秒スクリプトで再現性確認（任意・推奨）

~~~bash
make run10
tail -n +1 logs/run_*_10s/*.log
~~~

確認:
- tx/rx 両方のログに frame情報が出る
- 値が一致する

## 証跡（PRに貼る想定）

- `make clean && make` の成功ログ
- `tail -n +1 logs/rx_frame_check.log`
- `tail -n +1 logs/tx_frame_check.log`
- `make run10` 実行ログ（任意）
- `tail -n +1 logs/run_*_10s/*.log`（任意）

## 実装メモ（次Issueへの接続）

- #4 で `tx.c` に seq 付与 / timestamp_ns 付与 / 固定レート送信を実装
- #5 で `rx.c` に受信ループ（non-blocking / select/poll）を実装
- #6 以降で latency / drop推定 / 統計 / CSV を実装
- v0は「レイアウト固定」が目的。最適化やserialize実装は後続Issueで扱う