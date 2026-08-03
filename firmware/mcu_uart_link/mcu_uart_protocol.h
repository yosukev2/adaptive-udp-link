#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define MCU_UART_PREAMBLE UINT32_C(0xA55AC33C)
#define MCU_UART_VERSION 1u
#define MCU_UART_HEADER_LEN 16u
#define MCU_UART_MAX_PAYLOAD_LEN 1024u
#define MCU_UART_MAX_PACKET_LEN (MCU_UART_HEADER_LEN + MCU_UART_MAX_PAYLOAD_LEN)

typedef enum {
    MCU_UART_PACKET_DATA = 0x01,
    MCU_UART_PACKET_ACK = 0x02,
    MCU_UART_PACKET_NACK = 0x03,
    MCU_UART_PACKET_TELEMETRY = 0x10,
    MCU_UART_PACKET_HEARTBEAT = 0x11,
    MCU_UART_PACKET_ERROR = 0x7F,
} mcu_uart_packet_type_t;

typedef enum {
    MCU_UART_STATE_BOOT = 0,
    MCU_UART_STATE_IDLE,
    MCU_UART_STATE_RUN,
    MCU_UART_STATE_DEGRADED,
    MCU_UART_STATE_RECOVER,
    MCU_UART_STATE_SAFE,
} mcu_uart_state_t;

typedef enum {
    MCU_UART_ERROR_OK = 0,
    MCU_UART_ERROR_BAD_PREAMBLE = 1,
    MCU_UART_ERROR_BAD_VERSION = 2,
    MCU_UART_ERROR_BAD_TYPE = 3,
    MCU_UART_ERROR_BAD_LENGTH = 4,
    MCU_UART_ERROR_BAD_CRC = 5,
    MCU_UART_ERROR_SEQ_GAP = 6,
    MCU_UART_ERROR_DUPLICATE = 7,
    MCU_UART_ERROR_TIMEOUT = 8,
    MCU_UART_ERROR_BUFFER_OVERFLOW = 9,
    MCU_UART_ERROR_SAFE_ENTERED = 10,
} mcu_uart_error_t;

typedef struct {
    uint64_t rx_byte_count;
    uint64_t rx_packet_count;
    uint64_t rx_data_count;
    uint64_t crc_error_count;
    uint64_t seq_gap_count;
    uint64_t duplicate_count;
    uint64_t preamble_miss_count;
    uint64_t invalid_version_count;
    uint64_t invalid_type_count;
    uint64_t length_error_count;
    uint64_t rx_buffer_overflow_count;
    mcu_uart_state_t state;
    mcu_uart_error_t last_error_code;
    uint32_t last_seq;
    uint32_t expected_seq;
    bool has_sequence;
} mcu_uart_telemetry_t;

typedef struct {
    uint8_t type;
    uint32_t seq;
    uint16_t payload_len;
    uint32_t crc32;
    const uint8_t *payload;
} mcu_uart_packet_view_t;

typedef void (*mcu_uart_packet_callback_t)(const mcu_uart_packet_view_t *packet,
                                           void *user_data);

typedef struct {
    uint8_t buffer[MCU_UART_MAX_PACKET_LEN];
    size_t buffered_len;
    mcu_uart_telemetry_t telemetry;
} mcu_uart_parser_t;

uint32_t mcu_uart_crc32(const uint8_t *data, size_t len);
bool mcu_uart_packet_type_is_valid(uint8_t type);
int mcu_uart_build_packet(uint8_t type, uint32_t seq, const uint8_t *payload,
                          size_t payload_len, uint8_t *output,
                          size_t output_capacity, size_t *output_len);
void mcu_uart_parser_init(mcu_uart_parser_t *parser);
int mcu_uart_parser_feed(mcu_uart_parser_t *parser, const uint8_t *data,
                         size_t len, mcu_uart_packet_callback_t callback,
                         void *user_data);
