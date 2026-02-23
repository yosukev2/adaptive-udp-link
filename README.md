# adaptive-udp-link

Cで作る自己回復リンク基盤のための、UDPベース通信・計測・耐障害化・適応制御の学習/実装プロジェクトです。

このリポジトリでは、段階的に以下を構築していきます。

- UDP基礎通信（tx/rx）
- Frame定義（seq / timestamp / payload）
- 計測（latency / drop推定 / 1秒統計 / CSV）
- 故障注入
- 復旧/適応制御

## 現在のフェーズ

- W01: UDP基礎通信基盤の構築（Frame v0 + 計測基礎）
- 現在の実装は段階的に追加中（Issueごとに進行）

## リポジトリ構成（予定含む）

```text
adaptive-udp-link/
├── README.md
├── Makefile
├── .gitignore
├── src/
├── include/
├── scripts/
├── logs/
└── docs/
    └── issues/
```

## ビルド/実行（最短）

~~~bash
make
make run10
make run60
~~~

## ドキュメント方針

- README.md
  - プロジェクト概要
  - 現在地
  - 全体の使い方（最短）
- docs/issues/
  - Issue単位の目的、スコープ、受入条件、テスト手順、証跡

## Issue別ドキュメント

- `docs/issues/W01_ISSUE_02_scaffold_cli.md`
- `docs/issues/W01_ISSUE_03_frame_v0.md`

## 今後の進め方（W01の例）

- Issue #2: 雛形 + ビルド/実行スクリプト + 最小CLI
- Issue #3: Frame v0定義（frame.h）+ サイズ検証
- Issue #4: tx実装（固定レート送信 + seq/timestamp）
- Issue #5: rx実装（受信ループ）
- Issue #6-8: 計測ロジック/統計/CSV
- Issue #9: 設計判断の明文化（面接用説明ノート）
