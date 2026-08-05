#include "mcu_uart_protocol.h"

#include <stdio.h>
#include <string.h>

typedef struct {
    unsigned count;
    uint32_t last_seq;
    uint8_t last_payload[32];
    size_t last_payload_len;
} capture_t;

static void capture_packet(const mcu_uart_packet_view_t *packet, void *user_data)
{
    capture_t *capture = (capture_t *)user_data;
    capture->count++;
    capture->last_seq = packet->seq;
    capture->last_payload_len = packet->payload_len;
    if (packet->payload_len <= sizeof(capture->last_payload)) {
        memcpy(capture->last_payload, packet->payload, packet->payload_len);
    }
}

static int build_data(uint32_t seq, const char *text, uint8_t *wire,
                      size_t capacity, size_t *wire_len)
{
    return mcu_uart_build_packet(MCU_UART_PACKET_DATA, seq,
                                 (const uint8_t *)text, strlen(text), wire,
                                 capacity, wire_len);
}

#define CHECK(condition)                                                       \
    do {                                                                       \
        if (!(condition)) {                                                    \
            printf("[FAIL] %s:%d: %s\n", __func__, __LINE__, #condition);     \
            return 1;                                                          \
        }                                                                      \
    } while (0)

static int test_python_golden_vector(void)
{
    static const uint8_t expected[] = {
        0xA5, 0x5A, 0xC3, 0x3C, 0x01, 0x01, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x05, 0x25, 0x12,
        0x13, 0xDE, 0x68, 0x65, 0x6C, 0x6C, 0x6F,
    };
    uint8_t wire[MCU_UART_MAX_PACKET_LEN];
    size_t wire_len = 0;

    CHECK(build_data(1, "hello", wire, sizeof(wire), &wire_len) == 0);
    CHECK(wire_len == sizeof(expected));
    CHECK(memcmp(wire, expected, sizeof(expected)) == 0);
    return 0;
}

static int test_one_byte_chunks(void)
{
    uint8_t wire[MCU_UART_MAX_PACKET_LEN];
    size_t wire_len = 0;
    size_t i;
    mcu_uart_parser_t parser;
    capture_t capture = {0};

    CHECK(build_data(7, "split", wire, sizeof(wire), &wire_len) == 0);
    mcu_uart_parser_init(&parser);
    for (i = 0; i < wire_len; ++i) {
        CHECK(mcu_uart_parser_feed(&parser, wire + i, 1, capture_packet,
                                   &capture) == 0);
    }
    CHECK(capture.count == 1);
    CHECK(capture.last_seq == 7);
    CHECK(capture.last_payload_len == 5);
    CHECK(memcmp(capture.last_payload, "split", 5) == 0);
    CHECK(parser.telemetry.rx_byte_count == wire_len);
    CHECK(parser.telemetry.rx_data_count == 1);
    return 0;
}

static int test_concatenated_packets(void)
{
    uint8_t wire[MCU_UART_MAX_PACKET_LEN * 2];
    size_t first_len = 0;
    size_t second_len = 0;
    mcu_uart_parser_t parser;
    capture_t capture = {0};

    CHECK(build_data(0, "first", wire, sizeof(wire), &first_len) == 0);
    CHECK(build_data(1, "second", wire + first_len,
                     sizeof(wire) - first_len, &second_len) == 0);
    mcu_uart_parser_init(&parser);
    CHECK(mcu_uart_parser_feed(&parser, wire, first_len + second_len,
                               capture_packet, &capture) == 0);
    CHECK(capture.count == 2);
    CHECK(capture.last_seq == 1);
    CHECK(parser.telemetry.rx_packet_count == 2);
    return 0;
}

static int test_garbage_and_partial_preamble(void)
{
    static const uint8_t garbage[] = {0x00, 0x10, 0xA5, 0x5A};
    uint8_t wire[MCU_UART_MAX_PACKET_LEN];
    size_t wire_len = 0;
    mcu_uart_parser_t parser;
    capture_t capture = {0};

    CHECK(build_data(2, "ok", wire, sizeof(wire), &wire_len) == 0);
    mcu_uart_parser_init(&parser);
    CHECK(mcu_uart_parser_feed(&parser, garbage, sizeof(garbage),
                               capture_packet, &capture) == 0);
    CHECK(mcu_uart_parser_feed(&parser, wire, wire_len, capture_packet,
                               &capture) == 0);
    CHECK(capture.count == 1);
    CHECK(parser.telemetry.preamble_miss_count == sizeof(garbage));
    return 0;
}

static int test_bad_crc_resyncs(void)
{
    uint8_t bad[MCU_UART_MAX_PACKET_LEN];
    uint8_t good[MCU_UART_MAX_PACKET_LEN];
    size_t bad_len = 0;
    size_t good_len = 0;
    mcu_uart_parser_t parser;
    capture_t capture = {0};

    CHECK(build_data(10, "bad", bad, sizeof(bad), &bad_len) == 0);
    CHECK(build_data(11, "good", good, sizeof(good), &good_len) == 0);
    bad[MCU_UART_HEADER_LEN] ^= 0x01;
    mcu_uart_parser_init(&parser);
    CHECK(mcu_uart_parser_feed(&parser, bad, bad_len, capture_packet,
                               &capture) == 0);
    CHECK(mcu_uart_parser_feed(&parser, good, good_len, capture_packet,
                               &capture) == 0);
    CHECK(capture.count == 1);
    CHECK(capture.last_seq == 11);
    CHECK(parser.telemetry.crc_error_count == 1);
    return 0;
}

static int test_invalid_headers(void)
{
    uint8_t wire[MCU_UART_MAX_PACKET_LEN];
    size_t wire_len = 0;
    mcu_uart_parser_t parser;

    mcu_uart_parser_init(&parser);
    CHECK(build_data(0, "x", wire, sizeof(wire), &wire_len) == 0);
    wire[4] = 2;
    CHECK(mcu_uart_parser_feed(&parser, wire, wire_len, NULL, NULL) == 0);
    CHECK(parser.telemetry.invalid_version_count == 1);

    CHECK(build_data(0, "x", wire, sizeof(wire), &wire_len) == 0);
    wire[5] = 0x55;
    CHECK(mcu_uart_parser_feed(&parser, wire, wire_len, NULL, NULL) == 0);
    CHECK(parser.telemetry.invalid_type_count == 1);

    CHECK(build_data(0, "x", wire, sizeof(wire), &wire_len) == 0);
    wire[10] = 0x04;
    wire[11] = 0x01;
    CHECK(mcu_uart_parser_feed(&parser, wire, MCU_UART_HEADER_LEN, NULL,
                               NULL) == 0);
    CHECK(parser.telemetry.length_error_count == 1);
    return 0;
}

static int test_sequence_counters(void)
{
    uint8_t wire[MCU_UART_MAX_PACKET_LEN];
    size_t wire_len = 0;
    mcu_uart_parser_t parser;

    mcu_uart_parser_init(&parser);
    CHECK(build_data(0, "a", wire, sizeof(wire), &wire_len) == 0);
    CHECK(mcu_uart_parser_feed(&parser, wire, wire_len, NULL, NULL) == 0);
    CHECK(build_data(3, "b", wire, sizeof(wire), &wire_len) == 0);
    CHECK(mcu_uart_parser_feed(&parser, wire, wire_len, NULL, NULL) == 0);
    CHECK(build_data(3, "c", wire, sizeof(wire), &wire_len) == 0);
    CHECK(mcu_uart_parser_feed(&parser, wire, wire_len, NULL, NULL) == 0);

    CHECK(parser.telemetry.rx_data_count == 3);
    CHECK(parser.telemetry.seq_gap_count == 2);
    CHECK(parser.telemetry.duplicate_count == 1);
    CHECK(parser.telemetry.expected_seq == 4);
    return 0;
}

int main(void)
{
    int failures = 0;
    failures += test_python_golden_vector();
    failures += test_one_byte_chunks();
    failures += test_concatenated_packets();
    failures += test_garbage_and_partial_preamble();
    failures += test_bad_crc_resyncs();
    failures += test_invalid_headers();
    failures += test_sequence_counters();

    if (failures != 0) {
        printf("%d MCU UART protocol test(s) failed\n", failures);
        return 1;
    }
    printf("All MCU UART protocol tests passed\n");
    return 0;
}
