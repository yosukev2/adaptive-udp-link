# W01: rx.c（poll で安定受信ループ + 1秒周期処理の土台）

## 親EPIC
- Parent: [EPIC] W01 - UDP基礎通信基盤の構築（Frame v0 + 計測基礎） #1

## 目的
- UDP受信ができるだけでなく、受信が途切れても固まらない受信ループを作る。
- 1秒ごとの統計出力（将来のP95/P99やdrop推定）の土台となる待機構造を作る。

## スコープ（やること）
- UDPソケット生成（AF_INET / SOCK_DGRAM）
- bind（bind-ip + port）
- poll() による「受信待ち or タイムアウト」の統合待機
- recvfrom() による受信
- 受信サイズの検証（FrameV0サイズ）
- duration_sec まで安定動作するループ
- ログ出力（start / timeout / recv / end）

## 非スコープ（このイシューではやらない）
- latency算出
- drop推定
- seq連番チェック
- payload解釈
- 統計の本実装（件数/レート/分位点）
- Ctrl+C graceful shutdown の完成版（SIGINTハンドラ）

## 依存
- Depends on: #2（scaffold/CLI）, #3（Frame v0定義）

## 受入条件（AC）
- [ ] rx が指定portで bind して起動できる
- [ ] 受信が来ない状態でも固まらず、1秒ごとに timeout 進行できる
- [ ] tx 起動後に recv ログが出る
- [ ] 60秒以上安定動作する
- [ ] 想定外サイズのUDPを WARN として扱える
- [ ] 選定理由（pollを選んだ理由）がREADMEまたは本MDに残っている

## 学習目的
### ロジック要素（理解）
- ブロッキング recvfrom だけだと周期処理が止まる理由
- poll によって「I/O待ち」と「タイムアウト」を1つの待機に統合できること
- rx では bind が本質で、tx では sendto 宛先指定が本質であること
- recvfrom の戻り値 n は「今回受信したバイト数」であり、構造体サイズ保証ではないこと

### 暗記要素（API/用語）
- socket(), bind(), poll(), recvfrom()
- struct pollfd, POLLIN, POLLERR, POLLNVAL
- struct sockaddr_in, htons(), inet_pton()
- socklen_t, ssize_t
- CLOCK_MONOTONIC, clock_gettime()

## 実装メモ（方針）
- 今回は poll 方式を採用
  - 理由: non-blocking + busy loop より初心者にとって挙動が追いやすく、CPU燃焼を避けやすい
  - timeout を 1秒にすることで、将来の1秒統計出力に自然につながる
- 受信バッファは uint8_t buf_udp[sizeof(FrameV0)] を採用（バイナリとして扱う）
- recvfrom直前に src_len を毎回 sizeof(src_addr) で初期化する（入出力引数のため）

## テスト手順
1. rx単体起動（txなし）
   - timeoutログが1秒ごとに進むこと
   - duration経過で終了すること
2. rx起動後にtx起動
   - recvログが出ること
   - 受信サイズが sizeof(FrameV0) と一致すること
3. 異常系（任意）
   - 別サイズUDPを送って WARN が出ること

## 確認ログ/観測ポイント
- 期待ログ:
  - rx start ...
  - time out waiting for data
  - recv XX bytes
  - duration elapsed, exiting
  - rx end
- 異常時の見え方:
  - bind失敗 → perror("bind")
  - poll失敗 → perror("poll")
  - recvfrom失敗 → perror("recvfrom")
- 見るべきファイル:
  - logs/run_rx_test/*.log

## レビュー観点（セルフチェック）
- [ ] recvfrom の第7引数に socklen_t* を渡している
- [ ] bind先アドレスと送信元アドレスの変数を混同していない
- [ ] buf_udp を文字列としてログしていない
- [ ] close(sock), fclose(fp) を忘れていない
- [ ] ソース先頭コメントが現状と矛盾していない

## メモ（次イシューへの引き継ぎ）
- FrameV0 を memcpy で構造体へ復元して seq/timestamp を読む
- 1秒周期の統計出力（受信件数/バイト数）
- SIGINTハンドラで stop_flag を立てて graceful shutdown