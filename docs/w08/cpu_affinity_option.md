# W08 CPU affinity 実行ラッパー

## 目的

Linux 通信プロセスを指定 CPU core で実行できるようにし、CPU affinity を 1 変数として比較できるようにする。

## 実装方針

W08 では `taskset` を使い、`tx` と `rx` を同じ CPU core に固定する。  
既定の固定対象は `both` で、`tx` と `rx` の両方に同じ core を適用する。  
`--target none` を指定すると、CPU 固定をしない baseline 相当の実行になる。

## 使うスクリプト

- `scripts/w08/run_with_affinity.sh`

## 主なオプション

| オプション | 意味 |
| --- | --- |
| `--target both` | `tx` と `rx` の両方を固定する |
| `--target tx` | `tx` だけ固定する |
| `--target rx` | `rx` だけ固定する |
| `--target none` | `taskset` を使わない |
| `--core N` | 固定する CPU core 番号 |
| `--trial N` | trial 番号 |
| `--run-dir DIR` | 出力先ディレクトリ |

## 生成されるログ

- `run.log`
- `rx.log`
- `tx.log`
- `rx_1sec.csv`
- `rx_by_1recv.csv`

## ログに残す内容

- 実行日時
- trial 番号
- `target`
- `core`
- `rx_cmd`
- `tx_cmd`
- `tx_status`
- `rx_status`

## baseline と after の関係

- baseline は `--target none`
- after は `--target both` として `tx` / `rx` の両方を同じ core に固定する
- CPU affinity 以外の条件は固定する

## 確認方法

```bash
scripts/w08/run_with_affinity.sh --help
```

