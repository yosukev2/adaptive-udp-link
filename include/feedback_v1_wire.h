#pragma once

#include <stddef.h>
#include <stdint.h>

#define FEEDBACK_V1_WIRE_LEN 40u
#define FEEDBACK_V1_VERSION 1u
#define FEEDBACK_V1_HEADER_LEN 40u

typedef struct {
    uint8_t feedback_version;
    uint8_t header_len;
    uint16_t flags;
    uint32_t feedback_seq;
    uint64_t window_start_ns;
    uint64_t window_end_ns;
    uint32_t recv_ok;
    uint32_t missing_delta;
    uint32_t missing_rate_ppm;
    uint32_t p99_latency_us;
} FeedbackV1Packet;

int feedback_v1_build(const FeedbackV1Packet *packet, uint8_t *out, size_t out_cap, size_t *out_len);
int feedback_v1_parse(const uint8_t *buf, size_t len, FeedbackV1Packet *out);
