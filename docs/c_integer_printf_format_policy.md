# C整数printf format方針

## 採用方針

Linux側Cコードと実験用Cコードでは、`PRIu32` / `PRIu64` / `PRIX32` などの `inttypes.h` format macro を使わず、明示cast + 明示formatへ統一する。

| 元の型 | decimal出力 | hex出力 |
| --- | --- | --- |
| `uint32_t` | `%lu`, `(unsigned long)value` | `%08lX`, `(unsigned long)value` |
| `uint64_t` | `%llu`, `(unsigned long long)value` | `%016llX`, `(unsigned long long)value` |
| `int64_t` | `%lld`, `(long long)value` | 非対象 |
| `uint16_t` / `uint8_t` | `%u`, `(unsigned int)value` | 必要時は `%X`, `(unsigned int)value` |

## 理由

- ログformat上の型をソース上で明確にするため
- 組込み・教育資料寄りのレビューで読みやすくするため
- `PRI*` macro と明示formatの混在を避けるため

## 適用範囲

- `src/tx.c`
- `src/rx.c`
- `src/test_framer.c`
- `experiments/w06_jitter/linux_jitter.c`

現時点で `firmware/` 配下には `PRI*` macro の使用箇所はない。

## 注意点

- ログ内容、CSV列定義、frame formatは変更しない
- formatだけを変える場合も、必ず値側に明示castを付ける
- 新規コードでも `PRI*` macro を追加しない
