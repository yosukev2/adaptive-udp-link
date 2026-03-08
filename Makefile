# Makefile は「何を、どの順番で、どのコマンドで作るか」を定義するファイル
# 目的:
#   - 毎回同じ手順でビルドできるようにする（再現可能性）
#   - 人間の手打ちミスを減らす
#   - 後続の issue で AC 判定手順を固定する
#
# この #2 では「最小の土台」が目的なので、
#   - tx/rx の2つをビルドできる
#   - cleanできる
#   - 実行スクリプトを叩ける
# だけに絞る（過剰設計しない）

# 使用するCコンパイラ
# 将来 clang に変えたくなったらここだけ変えればよい
CC := gcc

# コンパイルオプション
# -std=c11   : C11規格でコンパイル（使える文法を明示）
# -Wall      : 基本的な警告を出す
# -Wextra    : 追加の警告を出す
# -O2        : 最適化（普段使いでバランスが良い）
# -g         : デバッグ情報を埋め込む（gdbで使う）
# -Iinclude  : #include "xxx.h" の探索先に include/ を追加
CFLAGS := -std=c11 -Wall -Wextra -O2 -g -Iinclude
CFLAGS := -std=c11 -D_POSIX_C_SOURCE=200809L -Wall -Wextra -O2 -g -Iinclude

# リンク時オプション（今は不要だが、将来ライブラリ追加で使う）
# 例: -lm（数学ライブラリ）など
LDFLAGS :=

# ディレクトリ名を変数にしておく理由:
# 文字列をあちこちに直接書くと、構成変更時に修正漏れが起きるため
BIN_DIR := bin
SRC_DIR := src

# 実行ファイルの出力先
# 「最終的に何ができるか」が見えやすいよう変数化している
TX := $(BIN_DIR)/tx
RX := $(BIN_DIR)/rx
FRAME_V1_WIRE := $(SRC_DIR)/frame_v1_wire.c

# .PHONY は「同名のファイルが存在しても、これはファイルではなくコマンド名として扱う」
# 例: clean という名前のファイルが偶然あっても、make clean が壊れない
.PHONY: all clean run10 run60

# デフォルトターゲット（make とだけ打つと all が実行される）
# #2のAC「ワンコマンドでビルド」を満たすため、allで tx/rx 両方を作る
all: $(TX) $(RX)

# bin/ ディレクトリを作るターゲット
# 実行ファイルの出力先が無いと gcc -o bin/tx が失敗するため、先に作る
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# tx をビルドするルール
# 意味: src/tx.c から bin/tx を作る
# | $(BIN_DIR) は「順序だけ必要な依存関係（order-only prerequisite）」
#   - bin/ が先に必要
#   - ただし bin/ の更新時刻が変わっても tx を無駄に再ビルドしない
$(TX): $(SRC_DIR)/tx.c $(FRAME_V1_WIRE) | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# 自動変数の意味（上の行で使っている）
#   $@ : ターゲット名（ここでは bin/tx）
#   $^ : すべての通常依存ファイル（ここでは src/tx.c と src/frame_v1_wire.c）
#
# つまり上のコマンドは実質:
#   gcc ... -o bin/tx src/tx.c src/frame_v1_wire.c

# rx をビルドするルール（txと同じ考え方）
$(RX): $(SRC_DIR)/rx.c $(FRAME_V1_WIRE) | $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# 10秒実行のショートカット
# 「make run10」で、ビルド→実行スクリプトの順に動く
# all に依存させることで、古いバイナリのまま実行する事故を減らす
run10: all
	./scripts/run_local_10s.sh

# 60秒実行のショートカット
run60: all
	./scripts/run_local_60s.sh

# 生成物の削除
# #2の段階では bin/ と build/ を消せば十分
# logs は検証証跡になるので消さない（必要なら別 target を作る）
clean:
	rm -rf $(BIN_DIR) build
