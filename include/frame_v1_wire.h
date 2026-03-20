#pragma once

#include <stddef.h>
#include <stdint.h>

#include "frame.h"

/*
 * Frame v1 wire helper
 *
 * - tx/rx で共有したい v1 の wire 定数と serialize helper をまとめる
 * - CRC32 実装はこの module を唯一の正にして、送受信で差分が出ないようにする
 */

enum {
    FRAME_V1_PREAMBLE_OFFSET = 0,
    FRAME_V1_VERSION_OFFSET = 4,
    FRAME_V1_HEADER_LEN_OFFSET = 5,
    FRAME_V1_PAYLOAD_LEN_OFFSET = 6,
    FRAME_V1_SEQ_OFFSET = 8,
    FRAME_V1_TX_TS_OFFSET = 12,
    FRAME_V1_FLAGS_OFFSET = 20,
    FRAME_V1_CRC32_OFFSET = 21,
    FRAME_V1_WIRE_HEADER_LEN = 25,
    FRAME_V1_CRC_INPUT_FIXED_LEN = 17,
    FRAME_V1_MAX_WIRE_BYTES = FRAME_V1_WIRE_HEADER_LEN + FRAME_V1_PAYLOAD_MAX_BYTES
};

static const uint32_t kFrameV1Preamble = 0xA55AC33CU;
static const uint8_t kFrameV1Version = 1U;
static const uint8_t kFrameV1FlagsNone = 0U;

typedef struct {
    FrameV1Header header;
    const uint8_t *payload;
    size_t payload_len;
    size_t frame_len;
} FrameV1Parsed;

uint32_t frame_v1_crc32(const uint8_t *data, size_t len);

int frame_v1_recalculate_crc(
    const FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len,
    uint32_t *out_crc
);

int frame_v1_validate_crc(
    const FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len
);

int frame_v1_parse(
    const uint8_t *buf,
    size_t len,
    FrameV1Parsed *out
);

int frame_v1_validate_header(const FrameV1Parsed *parsed);

int frame_v1_parse_and_validate(
    const uint8_t *buf,
    size_t len,
    FrameV1Parsed *out
);

int frame_v1_build(
    FrameV1Header *frame,
    const uint8_t *payload,
    size_t payload_len,
    uint8_t *out_frame,
    size_t out_frame_cap,
    size_t *out_frame_len
);

int frame_v1_build_crc32_test_frame(
    FrameV1Header *frame,
    uint8_t *out_frame,
    size_t out_frame_cap,
    size_t *out_frame_len
);
