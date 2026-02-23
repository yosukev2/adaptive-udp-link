#pragma once

#include <stdint.h>
#include <stddef.h>

/*
 * Frame v0 (W01)
 *
 * v0 の目的:
 * - tx/rx 間の共通フォーマットを固定する
 * - seq / timestamp / payload の意味を明確にする
 *
 * v0 方針（割り切り）:
 * - ローカル検証前提（同一ホスト / 同一ABI想定）
 * - バイトオーダーはホストオーダーのまま（v0では簡略化）
 * - 構造体直送を一旦許容
 *
 * 将来方針（v1+）:
 * - 手動serialize/deserialize
 * - network byte order（endianness明示）
 *
 * 注意:
 * - この struct は packed にしない。
 * - パディング/アライメント差による破壊を防ぐため、下で static assert により
 *   レイアウトを固定・検証する。
 */

#define FRAME_V0_PAYLOAD_BYTES 48

typedef struct {
    uint32_t seq;                              // 単調増加シーケンス番号
    uint64_t timestamp_ns;                     // 送信側が付与する時刻（単位: ns）
    uint8_t  payload[FRAME_V0_PAYLOAD_BYTES];  // 固定長ペイロード（v0）
} FrameV0;

/* レイアウト検証（想定: sizeof=64, offsets: seq=0, ts=8, payload=16） */
_Static_assert(offsetof(FrameV0, seq) == 0, "FrameV0.seq offset must be 0");
_Static_assert(offsetof(FrameV0, timestamp_ns) == 8, "FrameV0.timestamp_ns offset must be 8");
_Static_assert(offsetof(FrameV0, payload) == 16, "FrameV0.payload offset must be 16");
_Static_assert(sizeof(FrameV0) == 64, "sizeof(FrameV0) must be 64");