# W08 socket buffer 変更オプション

## 目的

W08 では、Linux UDP の送受信で socket buffer size を 1 変数として変更できるようにする。  
送信側は `--sndbuf`、受信側は `--rcvbuf` を使う。

## 追加するオプション

| 対象 | オプション | 役割 |
| --- | --- | --- |
| `tx` | `--sndbuf <bytes>` | `SO_SNDBUF` を設定する |
| `rx` | `--rcvbuf <bytes>` | `SO_RCVBUF` を設定する |

## 動作

- オプション未指定では、従来どおり Linux デフォルトのまま動作する
- 指定値は `setsockopt()` で設定する
- 実際に反映された値は `getsockopt()` で確認して log に残す
- `0` 以下の値は無効とする

## ログ

設定に成功したら、以下のような情報を runtime log に残す。

- `requested`
- `actual`
- `SO_SNDBUF` または `SO_RCVBUF`

設定に失敗した場合は `ERROR` として記録し、run を失敗扱いにする。

## W08 での使い方

socket buffer を変更する after 条件では、baseline とそれ以外の条件を固定したまま、buffer size だけを変える。  
CPU affinity の変更と同時に使わない。

## 確認方法

```bash
./bin/tx --help | grep sndbuf
./bin/rx --help | grep rcvbuf
```

