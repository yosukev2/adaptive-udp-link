# W01 / Issue #2
# リポジトリ雛形 + ビルド/実行スクリプト + 最低限CLI

## 親Issue

- EPIC: W01 - UDP基礎通信基盤の構築（Frame v0 + 計測基礎）

## 目的

実装の前に、毎回同じ手順でビルドして動かせる土台を作る。  
以降のIssueで、動作確認とAC判定がブレない状態にする。

## このIssueのスコープ

- ディレクトリ構成の作成（`src/`, `include/`, `scripts/`, `logs/` など）
- Makefile もしくは CMake のどちらか1つでビルド可能にする
- `tx` / `rx` の最小CLI引数を設計して固定する
- 60秒実行スクリプトを作る
- READMEに最短のビルド/実行/ログ場所を書く

## アウトオブスコープ

- UDP本体の送受信
- Frame v0本実装（seq / timestamp / payload）
- latency計測、drop推定、1秒統計、CSV本体
- CI導入
- クロスプラットフォーム完全対応

## 成果物（期待）

- `Makefile`（または `CMakeLists.txt`）
- `src/tx.c`（スタブ）
- `src/rx.c`（スタブ）
- `scripts/run_local_10s.sh`
- `scripts/run_local_60s.sh`
- `README.md`（最短導線）
- ログ出力先ルール（`logs/run_*`）

## 最小CLI仕様（固定）

### tx

- `--dst-ip <ip>`
- `--dst-port <port>`
- `--rate-hz <hz>`
- `--duration-sec <sec>`
- `--log-path <path>`

### rx

- `--bind-ip <ip>`（省略時 `0.0.0.0` 可）
- `--port <port>`
- `--duration-sec <sec>`
- `--log-path <path>`

## 受入条件（AC）

- ワンコマンドでビルドできる（例: `make`）
- `tx` と `rx` がそれぞれ起動できる
- 引数不足時に usage が出る
- 60秒実行スクリプトがある
- ログ保存先を固定できる
- READMEに「ビルド」「実行」「ログ場所」が最短で書かれている

## テスト手順（Issue #2）

### 1) ビルド

~~~bash
make
~~~

確認:
- `bin/tx`
- `bin/rx`

### 2) usage確認（引数不足）

~~~bash
./bin/tx
./bin/rx
~~~

確認:
- usageが表示される
- 終了コードが失敗（非0）であること（任意確認）

### 3) 手動起動（10秒）

#### rx 起動（別ターミナル or バックグラウンド）

~~~bash
./bin/rx --bind-ip 127.0.0.1 --port 9000 --duration-sec 10 --log-path logs/rx_manual.log
~~~

#### tx 起動

~~~bash
./bin/tx --dst-ip 127.0.0.1 --dst-port 9000 --rate-hz 100 --duration-sec 10 --log-path logs/tx_manual.log
~~~

確認:
- 両方が起動/終了できる
- `logs/*.log` が作成される

### 4) 10秒実行スクリプト

~~~bash
make run10
~~~

確認:
- `logs/run_YYYYMMDD_HHMMSS_10s/` が作成される
- `rx.log`, `tx.log` がある

### 5) 60秒実行スクリプト（AC対象）

~~~bash
make run60
~~~

確認:
- 60秒完走する
- `logs/run_YYYYMMDD_HHMMSS_60s/` が作成される
- `rx.log`, `tx.log` がある

### 6) ログ確認

~~~bash
find logs -maxdepth 2 -type f | sort
~~~

~~~bash
tail -n +1 logs/run_*/*.log
~~~

## 証跡（PRに貼る想定）

- `make` の成功ログ
- `./bin/tx` / `./bin/rx` のusage出力
- `make run10` 実行ログ
- `make run60` 実行ログ（完走）
- `find logs ...` の結果
- `tail ...` の結果（start/endが見える範囲）

## メモ（後続Issueへの接続）

- Issue #3で `include/frame.h` を追加し、Frame v0を固定
- Issue #4で `tx.c` を固定レート送信ループへ差し替え
- Issue #5で `rx.c` を受信ループへ差し替え
- Issue #6-8で計測/統計/CSVを実装