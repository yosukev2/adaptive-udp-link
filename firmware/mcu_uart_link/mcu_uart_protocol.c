#include "mcu_uart_protocol.h"

#include <string.h>

static const uint8_t k_preamble_bytes[4] = {0xA5, 0x5A, 0xC3, 0x3C};

static uint16_t read_u16_be(const uint8_t *p)
{
    return (uint16_t)(((uint16_t)p[0] << 8) | (uint16_t)p[1]);
}

static uint32_t read_u32_be(const uint8_t *p)
{
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8) | (uint32_t)p[3];
}

static void write_u16_be(uint8_t *p, uint16_t value)
{
    p[0] = (uint8_t)(value >> 8);
    p[1] = (uint8_t)value;
}

static void write_u32_be(uint8_t *p, uint32_t value)
{
    p[0] = (uint8_t)(value >> 24);
    p[1] = (uint8_t)(value >> 16);
    p[2] = (uint8_t)(value >> 8);
    p[3] = (uint8_t)value;
}

static uint32_t crc32_update(uint32_t crc, const uint8_t *data, size_t len)
{
    size_t i;
    unsigned bit;

    for (i = 0; i < len; ++i) {
        crc ^= data[i];
        for (bit = 0; bit < 8; ++bit) {
            uint32_t mask = (uint32_t)-(int32_t)(crc & 1u);
            crc = (crc >> 1) ^ (UINT32_C(0xEDB88320) & mask);
        }
    }
    return crc;
}

uint32_t mcu_uart_crc32(const uint8_t *data, size_t len)
{
    if (data == NULL && len != 0) {
        return 0;
    }
    return crc32_update(UINT32_C(0xFFFFFFFF), data, len) ^
           UINT32_C(0xFFFFFFFF);
}

static uint32_t packet_crc(const uint8_t *wire, size_t payload_len)
{
    uint32_t crc = UINT32_C(0xFFFFFFFF);
    crc = crc32_update(crc, wire + 4, 8);
    crc = crc32_update(crc, wire + MCU_UART_HEADER_LEN, payload_len);
    return crc ^ UINT32_C(0xFFFFFFFF);
}

bool mcu_uart_packet_type_is_valid(uint8_t type)
{
    switch (type) {
    case MCU_UART_PACKET_DATA:
    case MCU_UART_PACKET_ACK:
    case MCU_UART_PACKET_NACK:
    case MCU_UART_PACKET_TELEMETRY:
    case MCU_UART_PACKET_HEARTBEAT:
    case MCU_UART_PACKET_ERROR:
        return true;
    default:
        return false;
    }
}

int mcu_uart_build_packet(uint8_t type, uint32_t seq, const uint8_t *payload,
                          size_t payload_len, uint8_t *output,
                          size_t output_capacity, size_t *output_len)
{
    size_t packet_len = MCU_UART_HEADER_LEN + payload_len;
    uint32_t crc;

    if (!mcu_uart_packet_type_is_valid(type) ||
        payload_len > MCU_UART_MAX_PAYLOAD_LEN ||
        (payload == NULL && payload_len != 0) || output == NULL ||
        output_len == NULL || output_capacity < packet_len) {
        return -1;
    }

    write_u32_be(output, MCU_UART_PREAMBLE);
    output[4] = MCU_UART_VERSION;
    output[5] = type;
    write_u32_be(output + 6, seq);
    write_u16_be(output + 10, (uint16_t)payload_len);
    memset(output + 12, 0, 4);
    if (payload_len != 0) {
        memcpy(output + MCU_UART_HEADER_LEN, payload, payload_len);
    }
    crc = packet_crc(output, payload_len);
    write_u32_be(output + 12, crc);
    *output_len = packet_len;
    return 0;
}

void mcu_uart_parser_init(mcu_uart_parser_t *parser)
{
    if (parser == NULL) {
        return;
    }
    memset(parser, 0, sizeof(*parser));
    parser->telemetry.state = MCU_UART_STATE_IDLE;
}

static void consume(mcu_uart_parser_t *parser, size_t len)
{
    if (len >= parser->buffered_len) {
        parser->buffered_len = 0;
        return;
    }
    memmove(parser->buffer, parser->buffer + len, parser->buffered_len - len);
    parser->buffered_len -= len;
}

static size_t find_preamble(const uint8_t *data, size_t len)
{
    size_t i;
    for (i = 0; i + sizeof(k_preamble_bytes) <= len; ++i) {
        if (memcmp(data + i, k_preamble_bytes, sizeof(k_preamble_bytes)) == 0) {
            return i;
        }
    }
    return len;
}

static size_t preamble_prefix_suffix_len(const uint8_t *data, size_t len)
{
    size_t candidate = len < 3 ? len : 3;
    while (candidate > 0) {
        if (memcmp(data + len - candidate, k_preamble_bytes, candidate) == 0) {
            return candidate;
        }
        --candidate;
    }
    return 0;
}

static void discard_preamble_miss(mcu_uart_parser_t *parser, size_t len)
{
    if (len == 0) {
        return;
    }
    parser->telemetry.preamble_miss_count += len;
    parser->telemetry.last_error_code = MCU_UART_ERROR_BAD_PREAMBLE;
    consume(parser, len);
}

static void update_sequence(mcu_uart_telemetry_t *telemetry, uint32_t seq)
{
    if (!telemetry->has_sequence) {
        telemetry->has_sequence = true;
        telemetry->last_seq = seq;
        telemetry->expected_seq = seq + 1u;
    } else if (seq == telemetry->expected_seq) {
        telemetry->last_seq = seq;
        telemetry->expected_seq = seq + 1u;
    } else if (seq > telemetry->expected_seq) {
        telemetry->seq_gap_count += (uint64_t)(seq - telemetry->expected_seq);
        telemetry->last_error_code = MCU_UART_ERROR_SEQ_GAP;
        telemetry->last_seq = seq;
        telemetry->expected_seq = seq + 1u;
    } else {
        telemetry->duplicate_count++;
        telemetry->last_error_code = MCU_UART_ERROR_DUPLICATE;
    }
}

static void process_buffer(mcu_uart_parser_t *parser,
                           mcu_uart_packet_callback_t callback,
                           void *user_data)
{
    for (;;) {
        size_t offset = find_preamble(parser->buffer, parser->buffered_len);
        uint8_t version;
        uint8_t type;
        uint32_t seq;
        uint16_t payload_len;
        size_t packet_len;
        uint32_t wire_crc;
        mcu_uart_packet_view_t packet;

        if (offset == parser->buffered_len) {
            size_t keep = preamble_prefix_suffix_len(parser->buffer,
                                                     parser->buffered_len);
            discard_preamble_miss(parser, parser->buffered_len - keep);
            return;
        }
        if (offset > 0) {
            discard_preamble_miss(parser, offset);
        }
        if (parser->buffered_len < MCU_UART_HEADER_LEN) {
            return;
        }

        version = parser->buffer[4];
        type = parser->buffer[5];
        seq = read_u32_be(parser->buffer + 6);
        payload_len = read_u16_be(parser->buffer + 10);

        if (version != MCU_UART_VERSION) {
            parser->telemetry.invalid_version_count++;
            parser->telemetry.last_error_code = MCU_UART_ERROR_BAD_VERSION;
            consume(parser, 1);
            continue;
        }
        if (!mcu_uart_packet_type_is_valid(type)) {
            parser->telemetry.invalid_type_count++;
            parser->telemetry.last_error_code = MCU_UART_ERROR_BAD_TYPE;
            consume(parser, 1);
            continue;
        }
        if (payload_len > MCU_UART_MAX_PAYLOAD_LEN) {
            parser->telemetry.length_error_count++;
            parser->telemetry.last_error_code = MCU_UART_ERROR_BAD_LENGTH;
            consume(parser, 1);
            continue;
        }

        packet_len = MCU_UART_HEADER_LEN + (size_t)payload_len;
        if (parser->buffered_len < packet_len) {
            return;
        }
        wire_crc = read_u32_be(parser->buffer + 12);
        if (wire_crc != packet_crc(parser->buffer, payload_len)) {
            parser->telemetry.crc_error_count++;
            parser->telemetry.last_error_code = MCU_UART_ERROR_BAD_CRC;
            consume(parser, 1);
            continue;
        }

        packet.type = type;
        packet.seq = seq;
        packet.payload_len = payload_len;
        packet.crc32 = wire_crc;
        packet.payload = parser->buffer + MCU_UART_HEADER_LEN;
        parser->telemetry.rx_packet_count++;
        parser->telemetry.state = MCU_UART_STATE_RUN;
        if (type == MCU_UART_PACKET_DATA) {
            parser->telemetry.rx_data_count++;
            update_sequence(&parser->telemetry, seq);
        }
        if (callback != NULL) {
            callback(&packet, user_data);
        }
        consume(parser, packet_len);
    }
}

int mcu_uart_parser_feed(mcu_uart_parser_t *parser, const uint8_t *data,
                         size_t len, mcu_uart_packet_callback_t callback,
                         void *user_data)
{
    size_t i;

    if (parser == NULL || (data == NULL && len != 0)) {
        return -1;
    }

    parser->telemetry.rx_byte_count += len;
    for (i = 0; i < len; ++i) {
        if (parser->buffered_len == sizeof(parser->buffer)) {
            parser->telemetry.rx_buffer_overflow_count++;
            parser->telemetry.last_error_code = MCU_UART_ERROR_BUFFER_OVERFLOW;
            return -1;
        }
        parser->buffer[parser->buffered_len++] = data[i];
        process_buffer(parser, callback, user_data);
    }
    return 0;
}
