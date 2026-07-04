#pragma once

#include <stddef.h>
#include <stdint.h>

enum {
    FEC_V1_MAGIC = 0x46454331U, /* "FEC1" */
    FEC_V1_VERSION = 1U,
    FEC_V1_HEADER_LEN = 24,
    FEC_V1_TYPE_DATA = 1,
    FEC_V1_TYPE_PARITY = 2,
    FEC_V1_K_FIXED = 4,
    FEC_V1_R_FIXED = 1
};

typedef struct {
    uint8_t version;
    uint8_t header_len;
    uint8_t packet_type;
    uint8_t k;
    uint8_t r;
    uint8_t index_in_block;
    uint16_t payload_len;
    uint32_t block_id;
    uint32_t first_seq;
    uint32_t flags;
} FecV1Header;

int fec_v1_build_header(const FecV1Header *header, uint8_t *out, size_t out_cap);
int fec_v1_parse_header(const uint8_t *buf, size_t len, FecV1Header *out);
const char *fec_v1_type_name(uint8_t packet_type);
