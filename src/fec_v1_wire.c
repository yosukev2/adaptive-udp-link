#include "fec_v1_wire.h"

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

static uint16_t get_u16_be(const uint8_t *p) {
    return (uint16_t)(((uint16_t)p[0] << 8) | (uint16_t)p[1]);
}

static uint32_t get_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) |
           ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8) |
           (uint32_t)p[3];
}

int fec_v1_build_header(const FecV1Header *header, uint8_t *out, size_t out_cap) {
    if (!header || !out || out_cap < FEC_V1_HEADER_LEN) {
        return -1;
    }
    if (header->version != FEC_V1_VERSION || header->header_len != FEC_V1_HEADER_LEN) {
        return -1;
    }
    if (header->k != FEC_V1_K_FIXED || header->r != FEC_V1_R_FIXED) {
        return -1;
    }
    if (header->packet_type != FEC_V1_TYPE_DATA && header->packet_type != FEC_V1_TYPE_PARITY) {
        return -1;
    }
    if (header->index_in_block >= header->k && header->packet_type == FEC_V1_TYPE_DATA) {
        return -1;
    }

    memset(out, 0, FEC_V1_HEADER_LEN);
    put_u32_be(&out[0], FEC_V1_MAGIC);
    out[4] = header->version;
    out[5] = header->header_len;
    out[6] = header->packet_type;
    out[7] = header->k;
    out[8] = header->r;
    out[9] = header->index_in_block;
    put_u16_be(&out[10], header->payload_len);
    put_u32_be(&out[12], header->block_id);
    put_u32_be(&out[16], header->first_seq);
    put_u32_be(&out[20], header->flags);
    return 0;
}

int fec_v1_parse_header(const uint8_t *buf, size_t len, FecV1Header *out) {
    if (!buf || !out || len < FEC_V1_HEADER_LEN) {
        return -1;
    }
    if (get_u32_be(&buf[0]) != FEC_V1_MAGIC) {
        return -1;
    }
    memset(out, 0, sizeof(*out));
    out->version = buf[4];
    out->header_len = buf[5];
    out->packet_type = buf[6];
    out->k = buf[7];
    out->r = buf[8];
    out->index_in_block = buf[9];
    out->payload_len = get_u16_be(&buf[10]);
    out->block_id = get_u32_be(&buf[12]);
    out->first_seq = get_u32_be(&buf[16]);
    out->flags = get_u32_be(&buf[20]);

    if (out->version != FEC_V1_VERSION || out->header_len != FEC_V1_HEADER_LEN) {
        return -1;
    }
    if (out->k != FEC_V1_K_FIXED || out->r != FEC_V1_R_FIXED) {
        return -1;
    }
    if (out->packet_type != FEC_V1_TYPE_DATA && out->packet_type != FEC_V1_TYPE_PARITY) {
        return -1;
    }
    if (out->packet_type == FEC_V1_TYPE_DATA && out->index_in_block >= out->k) {
        return -1;
    }
    return 0;
}

const char *fec_v1_type_name(uint8_t packet_type) {
    switch (packet_type) {
        case FEC_V1_TYPE_DATA:
            return "data";
        case FEC_V1_TYPE_PARITY:
            return "parity";
        default:
            return "unknown";
    }
}
