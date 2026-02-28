# W01: 遅延算出（now - timestamp）+ drop推定（seq欠損）ロジック

## 親EPIC

* Parent: [EPIC] W01 - UDP基礎通信基盤の構築（Frame v0 + 計測基礎） #1

## 依存

* Depends on: W01: リポジトリ雛形 + ビルド/実行スクリプト + 最低限CLI #2
* Depends on: W01: Frame v0定義（frame.h）+ サイズ検証 + v0ルール固定 #3
* Depends on: W01: rx.c（poll ベースの安定受信ループ） #5

## 目的

受信した FrameV0 から、後続の比較に使える最小計測値を逐次算出できるようにする。
このイシューでは「1秒ごとの統計出力」まではやらず、各パケット到着時に更新できる遅延・欠損推定・重複・逆順の基礎ロジックを固める。

## スコープ

* `recv_now_ns - frame.timestamp_ns` による遅延算出
* `frame.seq` 差分による欠損推定（gap）
* 重複（dup）検出
* 逆順到着（reorder）検出
* 累積カウンタの更新
* 最終 summary に必要な最小集計値の保持

  * `latency_sum_ns`
  * `latency_sample_cnt`
  * `gap_cnt`
  * `dup_cnt`
  * `reord_cnt`
  * `future_ts_cnt`
  * `future_ts_detected`

## 非スコープ（このイシューではやらない）

* 1秒ごとの統計出力（Issue #7）
* P95 / P99 / ヒストグラム / ジッタ詳細
* seq wrap-around（uint32_t周回）対応
* clock差がある別ホスト間での遅延精度保証
* magic/version/checksum による高度検証

## 前提

* tx/rx が同一マシン、または同一 `CLOCK_MONOTONIC` 系として扱える環境で動くこと
* `FrameV0` のレイアウトは tx/rx で共有済みであること
* UDP は順序保証がないため、seq 差分ベースの欠損はあくまで推定値であること

## 実装方針

### 1. FrameV0 の復元

* `recvfrom()` で受けた `buf_udp` はバイナリとして扱う
* `n == sizeof(FrameV0)` を確認した後、`memcpy(&frame, buf_udp, sizeof(frame))` で構造体へ復元する

### 2. 遅延算出

* `recvfrom()` 成功直後に `recv_now_ns` を `CLOCK_MONOTONIC` で取得する
* `recv_now_ns >= frame.timestamp_ns` の場合のみ遅延サンプルとして採用する
* 遅延は以下で算出する

`latency_ns = recv_now_ns - frame.timestamp_ns`

* 採用時に以下を更新する

  * `latency_sum_ns += latency_ns`
  * `latency_sample_cnt++`
* `recv_now_ns < frame.timestamp_ns` の場合は future timestamp として扱い、通常遅延には入れない

  * `future_ts_cnt++`
  * `future_ts_detected = 1`

### 3. seq差分ベースの欠損推定

* 初回受信時は `prev_seq = frame.seq` を設定し、比較は行わない
* 2件目以降は以下のルールで更新する

#### 前進

* 条件: `prev_seq < frame.seq`
* 欠損推定:

  * `gap = frame.seq - prev_seq - 1`
* 更新:

  * `gap_cnt += gap`
  * `prev_seq = frame.seq`

#### 重複

* 条件: `prev_seq == frame.seq`
* 更新:

  * `dup_cnt++`
* `gap_cnt` には加算しない
* `prev_seq` は更新しない

#### 逆順

* 条件: `frame.seq < prev_seq`
* 更新:

  * `reord_cnt++`
* `gap_cnt` には加算しない
* `prev_seq` は更新しない
  （逆順到着で更新すると、その後の欠損推定を崩しやすいため）

### 4. 最終 summary に出す値

* `avg_latency_ms = latency_sum_ns / latency_sample_cnt / 1e6`
* `gap_cnt`
* `dup_cnt`
* `reord_cnt`
* `future_ts_cnt`
* `future_ts_detected`

## 学習目的

### ロジック要素

* 逐次到着するデータに対して、配列に貯めずにオンライン更新する考え方
* 「前進 / 重複 / 逆順」を分けて数えることで、欠損推定を壊さない考え方
* 遅延算出がクロック前提に依存すること
* UDPでの欠損推定が“推定”であり、真の欠損とは一致しない場合があること

### 暗記要素

* `recvfrom()` の戻り値と `socklen_t`
* `memcpy()` による構造体復元
* `CLOCK_MONOTONIC`
* `avg = sum / count`
* `prev_seq < seq`, `==`, `>` の3分岐

## 受入条件（AC）

* [ ] `FrameV0` をサイズ確認後に構造体へ復元できる
* [ ] 遅延サンプルを累積できる
* [ ] seq差分から `gap_cnt` を更新できる
* [ ] 重複と逆順を `gap_cnt` と分離して計上できる
* [ ] future timestamp を検出し、通常遅延から除外できる
* [ ] 最終 summary に `avg_latency_ms / gap_cnt / dup_cnt / reord_cnt / future_ts_*` を出せる
* [ ] 60秒実行でクラッシュせず動く

## テスト手順

### 正常系

1. rx を起動
2. tx を通常レートで起動
3. 実行終了後、summary に以下が出ることを確認

   * `avg_latency_ms`
   * `gap_cnt`
   * `dup_cnt`
   * `reord_cnt`
   * `future_ts_cnt`
   * `future_ts_detected`

### 期待値（ローカル通常実行）

* `avg_latency_ms` が0以上
* `gap_cnt` は通常0付近
* `dup_cnt` は通常0
* `reord_cnt` は通常0
* `future_ts_detected` は通常0

### 異常・境界系

* tx未起動で rx 単体起動してもクラッシュしない
* `latency_sample_cnt == 0` のとき、ゼロ除算しない
* サイズ不一致パケットで `WARN` を出して継続できる

## 実装メモ

* `gap_cnt` の加算は `uint64_t` に揃える
* `frame.seq` は W01 では wrap-around 未対応
* `avg_latency_ms` は summary 時点で計算し、途中では `sum/count` を保持するだけにする
* このイシューでは累積値のみを正とし、時間窓リセットはまだ行わない

## レビュー観点（セルフチェック）

* [ ] `recv_now_ns` を `recvfrom()` 成功直後に取っている
* [ ] `buf_udp` を文字列として扱っていない
* [ ] `n != sizeof(FrameV0)` を弾いている
* [ ] `dup` と `reorder` を `gap` に混ぜていない
* [ ] `latency_sample_cnt == 0` のとき平均計算を防いでいる
* [ ] summary の項目名が固定されている

## 次イシューへの引き継ぎ

* Issue #7 で、この累積ロジックを 1秒窓に分けて出力する
* 1秒窓では以下を追加で持つ

  * `*_in_1sec`
  * `min/max latency`
  * 固定フォーマットの `rx_stats` 行

