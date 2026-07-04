#include "feedback_v1_wire.h"

#include <stddef.h>
#include <stdint.h>
#include <string.h>

static void put_u16_be(uint8_t *p, uint16_t v) {
    p[0] = (uint8_t)(v >> 8);
    p[1] = (uint8_t)v;
}

static void put_u32_be(uint8_t *p, uint32_t v) {
    p[0] = (uint8_t)(v >> 24);
    p[1] = (uint8_t)(v >> 16);
    p[2] = (uint8_t)(v >> 8);
    p[3] = (uint8_t)v;
}

static void put_u64_be(uint8_t *p, uint64_t v) {
    p[0] = (uint8_t)(v >> 56);
    p[1] = (uint8_t)(v >> 48);
    p[2] = (uint8_t)(v >> 40);
    p[3] = (uint8_t)(v >> 32);
    p[4] = (uint8_t)(v >> 24);
    p[5] = (uint8_t)(v >> 16);
    p[6] = (uint8_t)(v >> 8);
    p[7] = (uint8_t)v;
}

static uint16_t get_u16_be(const uint8_t *p) {
    return ((uint16_t)p[0] << 8) | (uint16_t)p[1];
}

static uint32_t get_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) |
           ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8) |
           (uint32_t)p[3];
}

static uint64_t get_u64_be(const uint8_t *p) {
    return ((uint64_t)p[0] << 56) |
           ((uint64_t)p[1] << 48) |
           ((uint64_t)p[2] << 40) |
           ((uint64_t)p[3] << 32) |
           ((uint64_t)p[4] << 24) |
           ((uint64_t)p[5] << 16) |
           ((uint64_t)p[6] << 8) |
           (uint64_t)p[7];
}

int feedback_v1_build(const FeedbackV1Packet *packet, uint8_t *out, size_t out_cap, size_t *out_len) {
    if (!packet || !out || out_cap < FEEDBACK_V1_WIRE_LEN) {
        return -1;
    }

    memset(out, 0, FEEDBACK_V1_WIRE_LEN);
    out[0] = packet->feedback_version;
    out[1] = packet->header_len;
    put_u16_be(&out[2], packet->flags);
    put_u32_be(&out[4], packet->feedback_seq);
    put_u64_be(&out[8], packet->window_start_ns);
    put_u64_be(&out[16], packet->window_end_ns);
    put_u32_be(&out[24], packet->recv_ok);
    put_u32_be(&out[28], packet->missing_delta);
    put_u32_be(&out[32], packet->missing_rate_ppm);
    put_u32_be(&out[36], packet->p99_latency_us);
    put_u32_be(&out[40], packet->retransmit_start_seq);
    put_u32_be(&out[44], packet->retransmit_count);

    if (out_len) {
        *out_len = FEEDBACK_V1_WIRE_LEN;
    }
    return 0;
}

int feedback_v1_parse(const uint8_t *buf, size_t len, FeedbackV1Packet *out) {
    if (!buf || !out || len < FEEDBACK_V1_WIRE_LEN) {
        return -1;
    }
    if (buf[0] != FEEDBACK_V1_VERSION || buf[1] != FEEDBACK_V1_HEADER_LEN) {
        return -1;
    }

    out->feedback_version = buf[0];
    out->header_len = buf[1];
    out->flags = get_u16_be(&buf[2]);
    out->feedback_seq = get_u32_be(&buf[4]);
    out->window_start_ns = get_u64_be(&buf[8]);
    out->window_end_ns = get_u64_be(&buf[16]);
    out->recv_ok = get_u32_be(&buf[24]);
    out->missing_delta = get_u32_be(&buf[28]);
    out->missing_rate_ppm = get_u32_be(&buf[32]);
    out->p99_latency_us = get_u32_be(&buf[36]);
    out->retransmit_start_seq = get_u32_be(&buf[40]);
    out->retransmit_count = get_u32_be(&buf[44]);
    return 0;
}
