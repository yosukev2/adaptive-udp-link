// src/frame_v1_wire.c
//
// 役割
//   - Frame v1 の wire 定数に基づく serialize helper
//   - tx/rx で共通化したい CRC32 実装

#include <string.h>

#include "frame_v1_wire.h"

enum {
    CRC32_TABLE_ENTRY_COUNT = 256,
    CRC32_TABLE_INDEX_MASK = 0xFF,
    CRC32_TABLE_SHIFT_BITS = 8
};

// v1 は byte 列を順に処理する実装へ寄せたいので、ソフトウェア実装で一般的な LSB-first を採用する。
// LSB-first の reflected CRC32 は、0x04C11DB7 を反転した 0xEDB88320 を使う。
static const uint32_t kCrc32ReflectedPolynomial = 0xEDB88320U;
// CRC-32/IEEE と同じ all-ones の init/xorout にして、先頭の 0x00 列でも偏りにくくする。
static const uint32_t kCrc32Init = 0xFFFFFFFFU;
static const uint32_t kCrc32XorOut = 0xFFFFFFFFU;
// 固定テストベクタの期待値。production code とは別の bit-by-bit 参照計算で求めた値をここだけに固定する。
static const uint32_t kFrameV1Crc32TestExpected = 0x2D3B0C55U;
static const uint8_t kFrameV1Crc32TestPayload[] = "crc32-test-payload";

static uint32_t g_crc32_table[CRC32_TABLE_ENTRY_COUNT];
static int g_crc32_table_initialized = 0;

static int validate_payload_args(const uint8_t *payload, size_t payload_len) {
    if (payload_len > FRAME_V1_PAYLOAD_MAX_BYTES || payload_len > UINT16_MAX) {
        return -1;
    }
    if (payload_len > 0 && !payload) {
        return -1;
    }
    return 0;
}

static void write_u16_be(uint8_t *dst, uint16_t value) {
    dst[0] = (uint8_t)(value >> 8);
    dst[1] = (uint8_t)value;
}

static void write_u32_be(uint8_t *dst, uint32_t value) {
    dst[0] = (uint8_t)(value >> 24);
    dst[1] = (uint8_t)(value >> 16);
    dst[2] = (uint8_t)(value >> 8);
    dst[3] = (uint8_t)value;
}

static void write_u64_be(uint8_t *dst, uint64_t value) {
    dst[0] = (uint8_t)(value >> 56);
    dst[1] = (uint8_t)(value >> 48);
    dst[2] = (uint8_t)(value >> 40);
    dst[3] = (uint8_t)(value >> 32);
    dst[4] = (uint8_t)(value >> 24);
    dst[5] = (uint8_t)(value >> 16);
    dst[6] = (uint8_t)(value >> 8);
    dst[7] = (uint8_t)value;
}

// 将来、純理論版(MSB-first, 0x04C11DB7, init=0, xorout=0)へ切り替えるなら、
// table生成のシフト方向、更新式、polynomial、init/xorout をまとめて差し替える。
static void init_crc32_table(void) {
    if (g_crc32_table_initialized) {
        return;
    }

    for (uint32_t i = 0; i < CRC32_TABLE_ENTRY_COUNT; i++) {
        uint32_t crc = i;

        for (int bit = 0; bit < CRC32_TABLE_SHIFT_BITS; bit++) {
            if ((crc & 1U) != 0U) {
                crc = (crc >> 1U) ^ kCrc32ReflectedPolynomial;
            } else {
                crc >>= 1U;
            }
        }

        g_crc32_table[i] = crc;
    }

    g_crc32_table_initialized = 1;
}

uint32_t frame_v1_crc32(const uint8_t *data, size_t len) {
    uint32_t crc = kCrc32Init;

    init_crc32_table();

    for (size_t i = 0; i < len; i++) {
        // LSB-first では下位1byteを index にし、右シフトと反転多項式テーブルで次状態へ進める。
        crc = (crc >> CRC32_TABLE_SHIFT_BITS) ^ g_crc32_table[(crc ^ data[i]) & CRC32_TABLE_INDEX_MASK];
    }

    return crc ^ kCrc32XorOut;
}

static int frame_v1_normalize_header(FrameV1Header *frame, size_t payload_len) {
    if (!frame) {
        return -1;
    }
    if (payload_len > FRAME_V1_PAYLOAD_MAX_BYTES || payload_len > UINT16_MAX) {
        return -1;
    }

    frame->preamble = kFrameV1Preamble;
    frame->version = kFrameV1Version;
    frame->header_len = (uint8_t)FRAME_V1_WIRE_HEADER_LEN;
    frame->payload_len = (uint16_t)payload_len;
    return 0;
}

static int build_crc_input(
    const FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len,
    uint8_t *out_crc_input,
    size_t out_crc_input_cap,
    size_t *out_crc_input_len
) {
    size_t crc_input_len = 0;

    if (!frame || !out_crc_input || !out_crc_input_len) {
        return -1;
    }
    if (validate_payload_args(payload, payload_len) != 0) {
        return -1;
    }
    if ((size_t)frame->payload_len != payload_len) {
        return -1;
    }
    if (out_crc_input_cap < FRAME_V1_CRC_INPUT_FIXED_LEN + payload_len) {
        return -1;
    }

    // CRC は version..flags と payload の連続バイト列だけを対象にする。
    // preamble/crc32 を含めると protocol.md の v1 定義とずれるため、wire buffer を丸ごと使わない。
    // 対象フィールドを変える場合は、この連続列の順序と rx 側の検証ロジックを必ず同時に更新する。
    out_crc_input[crc_input_len++] = frame->version;
    out_crc_input[crc_input_len++] = frame->header_len;
    write_u16_be(&out_crc_input[crc_input_len], frame->payload_len);
    crc_input_len += sizeof(frame->payload_len);
    write_u32_be(&out_crc_input[crc_input_len], frame->seq);
    crc_input_len += sizeof(frame->seq);
    write_u64_be(&out_crc_input[crc_input_len], frame->tx_ts);
    crc_input_len += sizeof(frame->tx_ts);
    out_crc_input[crc_input_len++] = frame->flags;
    if (payload_len > 0) {
        memcpy(&out_crc_input[crc_input_len], payload, payload_len);
        crc_input_len += payload_len;
    }

    *out_crc_input_len = crc_input_len;
    return 0;
}

static int serialize_frame_v1(
    const FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len,
    uint8_t *out_frame,
    size_t out_frame_cap,
    size_t *out_frame_len
) {
    size_t frame_len = FRAME_V1_WIRE_HEADER_LEN + payload_len;

    if (!frame || !out_frame || !out_frame_len) {
        return -1;
    }
    if (validate_payload_args(payload, payload_len) != 0) {
        return -1;
    }
    if ((size_t)frame->payload_len != payload_len) {
        return -1;
    }
    if (out_frame_cap < frame_len) {
        return -1;
    }

    write_u32_be(&out_frame[FRAME_V1_PREAMBLE_OFFSET], frame->preamble);
    out_frame[FRAME_V1_VERSION_OFFSET] = frame->version;
    out_frame[FRAME_V1_HEADER_LEN_OFFSET] = frame->header_len;
    write_u16_be(&out_frame[FRAME_V1_PAYLOAD_LEN_OFFSET], frame->payload_len);
    write_u32_be(&out_frame[FRAME_V1_SEQ_OFFSET], frame->seq);
    write_u64_be(&out_frame[FRAME_V1_TX_TS_OFFSET], frame->tx_ts);
    out_frame[FRAME_V1_FLAGS_OFFSET] = frame->flags;
    write_u32_be(&out_frame[FRAME_V1_CRC32_OFFSET], frame->crc32);
    if (payload_len > 0) {
        // payload を増やす場合も、この serialize 順を tx/rx 両側の唯一の正として揃える。
        memcpy(&out_frame[FRAME_V1_WIRE_HEADER_LEN], payload, payload_len);
    }

    *out_frame_len = frame_len;
    return 0;
}

int frame_v1_recalculate_crc(
    const FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len,
    uint32_t *out_crc
) {
    uint8_t crc_input[FRAME_V1_CRC_INPUT_FIXED_LEN + FRAME_V1_PAYLOAD_MAX_BYTES];
    size_t crc_input_len = 0;

    if (!out_crc) {
        return -1;
    }
    if (build_crc_input(frame, payload, payload_len, crc_input, sizeof(crc_input), &crc_input_len) != 0) {
        return -1;
    }

    *out_crc = frame_v1_crc32(crc_input, crc_input_len);
    return 0;
}

int frame_v1_validate_crc(
    const FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len
) {
    uint32_t recalculated_crc = 0;

    if (!frame) {
        return -1;
    }
    if (frame_v1_recalculate_crc(frame, payload, payload_len, &recalculated_crc) != 0) {
        return -1;
    }

    return (recalculated_crc == frame->crc32) ? 1 : 0;
}

int frame_v1_build(
    FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len,
    uint8_t *out_frame,
    size_t out_frame_cap,
    size_t *out_frame_len
) {
    if (!frame) {
        return -1;
    }
    if (frame_v1_normalize_header(frame, payload_len) != 0) {
        return -1;
    }
    if (frame_v1_recalculate_crc(frame, payload, payload_len, &frame->crc32) != 0) {
        return -1;
    }

    return serialize_frame_v1(frame, payload, payload_len, out_frame, out_frame_cap, out_frame_len);
}

int frame_v1_build_crc32_test_frame(
    FrameV1Header *frame,
    uint8_t *out_frame,
    size_t out_frame_cap,
    size_t *out_frame_len
) {
    if (!frame) {
        return -1;
    }

    // テストベクタは wire module 側に置き、tx/rx の確認で同じ入力を再利用できるようにする。
    memset(frame, 0, sizeof(*frame));
    frame->preamble = kFrameV1Preamble;
    frame->version = kFrameV1Version;
    frame->seq = 0x01020304U;
    frame->tx_ts = UINT64_C(0x1122334455667788);
    frame->flags = kFrameV1FlagsNone;

    if (frame_v1_build(
        frame,
        kFrameV1Crc32TestPayload,
        sizeof(kFrameV1Crc32TestPayload) - 1,
        out_frame,
        out_frame_cap,
        out_frame_len
    ) != 0) {
        return -1;
    }
    if (frame->crc32 != kFrameV1Crc32TestExpected) {
        return -1;
    }
    if (frame_v1_validate_crc(frame, kFrameV1Crc32TestPayload, sizeof(kFrameV1Crc32TestPayload) - 1) != 1) {
        return -1;
    }

    return 0;
}
