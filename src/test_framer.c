// src/test_framer.c
//
// Framer ユニットテスト
//
// rx.c の static 関数をそのままテストするのではなく、
// frame_v1_wire.c の公開 API（parse / validate_header / validate_crc）を使った
// ミニマル Framer をここに再実装して 3 シナリオを検証する。
//
// テストシナリオ:
//   1. 正常+正常+正常:    3 フレーム全て抽出できること
//   2. 正常+CRC破損+正常: 2 フレーム抽出・1 bad_crc を検出できること
//   3. ゴミ+正常+正常:    ゴミをリシンクして 2 フレーム抽出できること

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <inttypes.h>

#include "frame.h"
#include "frame_v1_wire.h"

// ---------------------------------------------------------------------------
// テスト用ミニマル Framer
// ---------------------------------------------------------------------------

#define TEST_BUF_CAP (FRAME_V1_MAX_WIRE_BYTES * 8)

typedef struct {
    uint8_t data[TEST_BUF_CAP];
    size_t  len;
} TestBuf;

typedef enum {
    TFR_OK        = 0,
    TFR_NEED_MORE = 1,
    TFR_RESYNCED  = 2,
} TestFramerResult;

typedef struct {
    uint64_t ok_count;
    uint64_t bad_crc;
    uint64_t bad_header;
    uint64_t resynced;
} TestFramerStats;

static void tbuf_consume(TestBuf *b, size_t n) {
    if (n >= b->len) { b->len = 0; return; }
    memmove(b->data, b->data + n, b->len - n);
    b->len -= n;
}

static size_t tbuf_find_preamble(const TestBuf *b) {
    const uint8_t p0 = (uint8_t)(kFrameV1Preamble >> 24);
    const uint8_t p1 = (uint8_t)(kFrameV1Preamble >> 16);
    const uint8_t p2 = (uint8_t)(kFrameV1Preamble >> 8);
    const uint8_t p3 = (uint8_t)(kFrameV1Preamble);
    for (size_t i = 0; i + 4 <= b->len; i++) {
        if (b->data[i]   == p0 && b->data[i+1] == p1 &&
            b->data[i+2] == p2 && b->data[i+3] == p3) {
            return i;
        }
    }
    return b->len;
}

static TestFramerResult test_framer_step(TestBuf *b, FrameV1Parsed *out, TestFramerStats *st) {
    size_t off = tbuf_find_preamble(b);

    if (off == b->len) {
        // preamble なし。末尾 3 バイトを保持して残りを捨てる
        if (b->len > 3) {
            st->resynced++;
            tbuf_consume(b, b->len - 3);
        }
        return TFR_NEED_MORE;
    }

    if (off > 0) {
        // preamble が先頭にない: ゴミをスキップ
        st->resynced++;
        tbuf_consume(b, off);
        return TFR_RESYNCED;
    }

    if (b->len < FRAME_V1_WIRE_HEADER_LEN) return TFR_NEED_MORE;

    uint16_t payload_len_peek =
        ((uint16_t)b->data[FRAME_V1_PAYLOAD_LEN_OFFSET] << 8) |
        (uint16_t)b->data[FRAME_V1_PAYLOAD_LEN_OFFSET + 1];

    if ((size_t)payload_len_peek > FRAME_V1_PAYLOAD_MAX_BYTES) {
        st->resynced++;
        tbuf_consume(b, 1);
        return TFR_RESYNCED;
    }

    size_t frame_len = FRAME_V1_WIRE_HEADER_LEN + (size_t)payload_len_peek;
    if (b->len < frame_len) return TFR_NEED_MORE;

    if (frame_v1_parse(b->data, frame_len, out) != 0) {
        st->resynced++;
        tbuf_consume(b, 1);
        return TFR_RESYNCED;
    }

    if (frame_v1_validate_header(out) != 0) {
        st->resynced++;
        st->bad_header++;
        tbuf_consume(b, 1);
        return TFR_RESYNCED;
    }

    if (frame_v1_validate_crc(&out->header, out->payload, out->payload_len) != 1) {
        // CRC 不一致: フレーム境界は確定しているので frame_len バイト丸ごとスキップ
        st->resynced++;
        st->bad_crc++;
        tbuf_consume(b, frame_len);
        return TFR_RESYNCED;
    }

    tbuf_consume(b, frame_len);
    st->ok_count++;
    return TFR_OK;
}

static int tbuf_append(TestBuf *b, const uint8_t *data, size_t len) {
    if (b->len + len > TEST_BUF_CAP) return -1;
    memcpy(b->data + b->len, data, len);
    b->len += len;
    return 0;
}

// フレームをビルドして buf に追加する
static int build_and_append(TestBuf *buf, uint32_t seq,
                             const uint8_t *payload, size_t payload_len) {
    FrameV1Header hdr;
    uint8_t wire[FRAME_V1_MAX_WIRE_BYTES];
    size_t frame_len = 0;
    memset(&hdr, 0, sizeof(hdr));
    hdr.seq   = seq;
    hdr.tx_ts = 0;
    hdr.flags = kFrameV1FlagsNone;
    if (frame_v1_build(&hdr, payload, payload_len, wire, sizeof(wire), &frame_len) != 0) {
        return -1;
    }
    return tbuf_append(buf, wire, frame_len);
}

// NEED_MORE になるまで Framer を回す
static void run_framer(TestBuf *buf, TestFramerStats *st) {
    FrameV1Parsed out;
    for (;;) {
        memset(&out, 0, sizeof(out));
        TestFramerResult r = test_framer_step(buf, &out, st);
        if (r == TFR_NEED_MORE) break;
        (void)r;  // TFR_OK / TFR_RESYNCED はループ継続
    }
}

// ---------------------------------------------------------------------------
// テストケース
// ---------------------------------------------------------------------------

static int test_normal_normal_normal(void) {
    const char *name = "正常+正常+正常";
    static const uint8_t payload[] = {0x01, 0x02, 0x03, 0x04};
    TestBuf buf;
    TestFramerStats st;
    memset(&buf, 0, sizeof(buf));
    memset(&st,  0, sizeof(st));

    if (build_and_append(&buf, 0, payload, sizeof(payload)) != 0 ||
        build_and_append(&buf, 1, payload, sizeof(payload)) != 0 ||
        build_and_append(&buf, 2, payload, sizeof(payload)) != 0) {
        printf("[FAIL] %s: フレームビルド失敗\n", name);
        return 1;
    }

    run_framer(&buf, &st);

    if (st.ok_count != 3 || st.bad_crc != 0 || st.resynced != 0) {
        printf("[FAIL] %s: ok=%" PRIu64 " bad_crc=%" PRIu64 " resynced=%" PRIu64 "\n",
               name, st.ok_count, st.bad_crc, st.resynced);
        return 1;
    }
    printf("[PASS] %s\n", name);
    return 0;
}

static int test_normal_badcrc_normal(void) {
    const char *name = "正常+CRC破損+正常";
    static const uint8_t payload[] = {0x0A, 0x0B, 0x0C, 0x0D};
    FrameV1Header hdr;
    uint8_t wire[FRAME_V1_MAX_WIRE_BYTES];
    size_t frame_len = 0;
    TestBuf buf;
    TestFramerStats st;
    memset(&buf, 0, sizeof(buf));
    memset(&st,  0, sizeof(st));

    // frame0: 正常
    if (build_and_append(&buf, 10, payload, sizeof(payload)) != 0) {
        printf("[FAIL] %s: frame0 ビルド失敗\n", name);
        return 1;
    }

    // frame1: ビルド後に CRC32 フィールドを壊す
    memset(&hdr, 0, sizeof(hdr));
    hdr.seq   = 11;
    hdr.tx_ts = 0;
    hdr.flags = kFrameV1FlagsNone;
    if (frame_v1_build(&hdr, payload, sizeof(payload), wire, sizeof(wire), &frame_len) != 0) {
        printf("[FAIL] %s: frame1 ビルド失敗\n", name);
        return 1;
    }
    wire[FRAME_V1_CRC32_OFFSET] ^= 0xFF;  // CRC を意図的に破壊
    if (tbuf_append(&buf, wire, frame_len) != 0) {
        printf("[FAIL] %s: frame1 追加失敗\n", name);
        return 1;
    }

    // frame2: 正常
    if (build_and_append(&buf, 12, payload, sizeof(payload)) != 0) {
        printf("[FAIL] %s: frame2 ビルド失敗\n", name);
        return 1;
    }

    run_framer(&buf, &st);

    if (st.ok_count != 2 || st.bad_crc != 1) {
        printf("[FAIL] %s: ok=%" PRIu64 " bad_crc=%" PRIu64 " resynced=%" PRIu64 "\n",
               name, st.ok_count, st.bad_crc, st.resynced);
        return 1;
    }
    printf("[PASS] %s\n", name);
    return 0;
}

static int test_garbage_normal_normal(void) {
    const char *name = "ゴミ+正常+正常";
    // preamble パターン（0xA5 0x5A 0xC3 0x3C）を含まないゴミバイト列
    // 全バイトが 0x09 以下なので preamble 誤検知はない
    static const uint8_t garbage[] = {
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09
    };
    static const uint8_t payload[] = {0x11, 0x22, 0x33, 0x44};
    TestBuf buf;
    TestFramerStats st;
    memset(&buf, 0, sizeof(buf));
    memset(&st,  0, sizeof(st));

    if (tbuf_append(&buf, garbage, sizeof(garbage)) != 0) {
        printf("[FAIL] %s: ゴミ追加失敗\n", name);
        return 1;
    }
    if (build_and_append(&buf, 20, payload, sizeof(payload)) != 0 ||
        build_and_append(&buf, 21, payload, sizeof(payload)) != 0) {
        printf("[FAIL] %s: フレームビルド失敗\n", name);
        return 1;
    }

    run_framer(&buf, &st);

    if (st.ok_count != 2 || st.resynced < 1) {
        printf("[FAIL] %s: ok=%" PRIu64 " resynced=%" PRIu64 " bad_crc=%" PRIu64 "\n",
               name, st.ok_count, st.resynced, st.bad_crc);
        return 1;
    }
    printf("[PASS] %s\n", name);
    return 0;
}

int main(void) {
    int failures = 0;
    failures += test_normal_normal_normal();
    failures += test_normal_badcrc_normal();
    failures += test_garbage_normal_normal();
    if (failures == 0) {
        printf("全テスト合格\n");
        return 0;
    }
    printf("%d テスト失敗\n", failures);
    return 1;
}
