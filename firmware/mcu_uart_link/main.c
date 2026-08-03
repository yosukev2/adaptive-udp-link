/*
 * MCU UART Link Control Demo firmware.
 *
 * Packet link : uart0 on GPIO0 (TX) / GPIO1 (RX), 115200 8N1.
 *               Receives DATA packets from the PC harness and replies with ACK.
 * Telemetry   : USB CDC, emitted as mcu_telemetry.csv rows so the capture side
 *               can store it directly next to pc_tx_log.csv / pc_rx_log.csv.
 *
 * Contracts:
 *   docs/mcu_uart/protocol.md
 *   docs/mcu_uart/log_schema.md
 *   docs/mcu_uart/telemetry_schema.md
 */

#include <stdio.h>
#include <string.h>

#include "pico/stdlib.h"
#include "hardware/uart.h"

#include "mcu_uart_protocol.h"

#define LINK_UART uart0
#define LINK_BAUDRATE 115200

/*
 * uart0 can be routed to GP0/GP1, GP12/GP13, or GP16/GP17 on RP2040. The pins
 * are overridable so a board with damaged pads can be moved to a spare pair
 * without editing this file.
 */
#ifndef LINK_UART_TX_PIN
#define LINK_UART_TX_PIN 0
#endif
#ifndef LINK_UART_RX_PIN
#define LINK_UART_RX_PIN 1
#endif
#define TELEMETRY_PERIOD_MS 200

#ifndef MCU_TRIAL_ID
#define MCU_TRIAL_ID "mcu_uart_link"
#endif

/*
 * HEARTBEAT emission period in milliseconds; 0 disables it. Off by default so a
 * baseline run records only DATA and ACK traffic. Enabling it makes the board
 * transmit without being asked, which isolates the MCU-to-PC direction when the
 * link does not come up.
 */
#ifndef MCU_UART_HEARTBEAT_MS
#define MCU_UART_HEARTBEAT_MS 0
#endif

/*
 * Counters the shared parser does not own. The parser tracks RX-side packet
 * validity; these track TX side and link state, which log_schema.md also
 * requires in mcu_telemetry.csv.
 */
typedef struct {
    uint64_t tx_packet_count;
    uint64_t ack_sent_count;
    uint64_t nack_sent_count;
    uint64_t telemetry_sent_count;
    uint64_t heartbeat_sent_count;
    uint64_t timeout_count;
    uint64_t rx_buffer_miss_count;
    uint64_t recover_enter_count;
    uint64_t recovered_count;
    uint64_t unrecovered_count;
    uint64_t safe_enter_count;
    uint64_t reset_count;
} app_counters_t;

static mcu_uart_parser_t g_parser;
static app_counters_t g_counters;
static uint8_t g_tx_buffer[MCU_UART_MAX_PACKET_LEN];

static const char *state_name(mcu_uart_state_t state)
{
    switch (state) {
    case MCU_UART_STATE_BOOT:
        return "BOOT";
    case MCU_UART_STATE_IDLE:
        return "IDLE";
    case MCU_UART_STATE_RUN:
        return "RUN";
    case MCU_UART_STATE_DEGRADED:
        return "DEGRADED";
    case MCU_UART_STATE_RECOVER:
        return "RECOVER";
    case MCU_UART_STATE_SAFE:
        return "SAFE";
    default:
        return "UNKNOWN";
    }
}

static bool send_packet(uint8_t type, uint32_t seq, const uint8_t *payload,
                        size_t payload_len)
{
    size_t packet_len = 0;

    if (mcu_uart_build_packet(type, seq, payload, payload_len, g_tx_buffer,
                              sizeof(g_tx_buffer), &packet_len) != 0) {
        return false;
    }
    uart_write_blocking(LINK_UART, g_tx_buffer, packet_len);
    g_counters.tx_packet_count++;
    return true;
}

/*
 * The payload pointer is parser-owned and valid only inside this callback,
 * so the ACK is built and pushed to the UART before returning.
 */
static void on_packet(const mcu_uart_packet_view_t *packet, void *user_data)
{
    (void)user_data;

    if (packet->type != MCU_UART_PACKET_DATA) {
        return;
    }
    /* Echo the payload so the PC side can verify an exact round-trip match. */
    if (send_packet(MCU_UART_PACKET_ACK, packet->seq, packet->payload,
                    packet->payload_len)) {
        g_counters.ack_sent_count++;
    }
}

/*
 * Reports the pins the build actually compiled in, so a run can be attributed to
 * a known configuration instead of an assumed one. Bring-up on this board moved
 * the link off GP0/GP1, which makes the pins part of what a trial has to record.
 * Prefixed with # so readers can skip it as a comment.
 */
static void print_link_configuration(void)
{
    printf("# uart0 tx=GP%u rx=GP%u baudrate=%u heartbeat_ms=%u\n",
           (unsigned int)LINK_UART_TX_PIN,
           (unsigned int)LINK_UART_RX_PIN,
           (unsigned int)LINK_BAUDRATE,
           (unsigned int)MCU_UART_HEARTBEAT_MS);
}

static void print_telemetry_header(void)
{
    printf("trial_id,mono_ms,state,last_error_code,last_seq,expected_seq,"
           "rx_byte_count,rx_packet_count,rx_data_count,tx_packet_count,"
           "ack_sent_count,nack_sent_count,telemetry_sent_count,"
           "heartbeat_sent_count,crc_error_count,seq_gap_count,duplicate_count,"
           "timeout_count,preamble_miss_count,invalid_version_count,"
           "invalid_type_count,length_error_count,rx_buffer_overflow_count,"
           "rx_buffer_miss_count,recover_enter_count,recovered_count,"
           "unrecovered_count,safe_enter_count,reset_count,rx_buffer_used,"
           "rx_buffer_capacity\n");
}

static void print_telemetry_row(void)
{
    const mcu_uart_telemetry_t *t = &g_parser.telemetry;
    uint64_t mono_ms = to_ms_since_boot(get_absolute_time());

    printf("%s,%llu,%s,%u,%lu,%lu,"
           "%llu,%llu,%llu,%llu,"
           "%llu,%llu,%llu,"
           "%llu,%llu,%llu,%llu,"
           "%llu,%llu,%llu,"
           "%llu,%llu,%llu,"
           "%llu,%llu,%llu,"
           "%llu,%llu,%llu,%llu,"
           "%llu\n",
           MCU_TRIAL_ID,
           (unsigned long long)mono_ms,
           state_name(t->state),
           (unsigned int)t->last_error_code,
           (unsigned long)t->last_seq,
           (unsigned long)t->expected_seq,
           (unsigned long long)t->rx_byte_count,
           (unsigned long long)t->rx_packet_count,
           (unsigned long long)t->rx_data_count,
           (unsigned long long)g_counters.tx_packet_count,
           (unsigned long long)g_counters.ack_sent_count,
           (unsigned long long)g_counters.nack_sent_count,
           (unsigned long long)g_counters.telemetry_sent_count,
           (unsigned long long)g_counters.heartbeat_sent_count,
           (unsigned long long)t->crc_error_count,
           (unsigned long long)t->seq_gap_count,
           (unsigned long long)t->duplicate_count,
           (unsigned long long)g_counters.timeout_count,
           (unsigned long long)t->preamble_miss_count,
           (unsigned long long)t->invalid_version_count,
           (unsigned long long)t->invalid_type_count,
           (unsigned long long)t->length_error_count,
           (unsigned long long)t->rx_buffer_overflow_count,
           (unsigned long long)g_counters.rx_buffer_miss_count,
           (unsigned long long)g_counters.recover_enter_count,
           (unsigned long long)g_counters.recovered_count,
           (unsigned long long)g_counters.unrecovered_count,
           (unsigned long long)g_counters.safe_enter_count,
           (unsigned long long)g_counters.reset_count,
           (unsigned long long)g_parser.buffered_len,
           (unsigned long long)sizeof(g_parser.buffer));
}

static void link_uart_init(void)
{
    uart_init(LINK_UART, LINK_BAUDRATE);
    gpio_set_function(LINK_UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(LINK_UART_RX_PIN, GPIO_FUNC_UART);
    uart_set_hw_flow(LINK_UART, false, false);
    uart_set_format(LINK_UART, 8, 1, UART_PARITY_NONE);
    uart_set_fifo_enabled(LINK_UART, true);
}

/*
 * On RX buffer overflow the parser cannot make progress, so its byte buffer is
 * reset while the accumulated telemetry counters are preserved. Losing the
 * counters here would hide the very event being recorded.
 */
static void recover_from_overflow(void)
{
    mcu_uart_telemetry_t saved = g_parser.telemetry;

    mcu_uart_parser_init(&g_parser);
    g_parser.telemetry = saved;
    g_counters.rx_buffer_miss_count++;
}

/*
 * The CSV header is emitted on the rising edge of the USB CDC connection rather
 * than once at boot. A capture started at any time therefore receives the column
 * names, instead of only the runs that attach within a fixed window after reset.
 *
 * A header cannot land mid-file: losing the connection removes the CDC device,
 * which ends the capturing reader and closes its file, so a reconnect always
 * writes into a new one.
 */
static bool telemetry_host_attached(void)
{
    static bool was_connected;
    bool connected = stdio_usb_connected();
    bool attached = connected && !was_connected;

    was_connected = connected;
    return attached;
}

int main(void)
{
    absolute_time_t next_telemetry;
#if MCU_UART_HEARTBEAT_MS > 0
    absolute_time_t next_heartbeat;
    uint32_t heartbeat_seq = 0;
#endif

    stdio_init_all();
    link_uart_init();

    mcu_uart_parser_init(&g_parser);
    memset(&g_counters, 0, sizeof(g_counters));

    next_telemetry = make_timeout_time_ms(TELEMETRY_PERIOD_MS);
#if MCU_UART_HEARTBEAT_MS > 0
    next_heartbeat = make_timeout_time_ms(MCU_UART_HEARTBEAT_MS);
#endif

    for (;;) {
        while (uart_is_readable(LINK_UART)) {
            uint8_t byte = (uint8_t)uart_getc(LINK_UART);
            if (mcu_uart_parser_feed(&g_parser, &byte, 1, on_packet, NULL) != 0) {
                recover_from_overflow();
            }
        }

#if MCU_UART_HEARTBEAT_MS > 0
        if (absolute_time_diff_us(get_absolute_time(), next_heartbeat) <= 0) {
            if (send_packet(MCU_UART_PACKET_HEARTBEAT, heartbeat_seq, NULL, 0)) {
                heartbeat_seq++;
                g_counters.heartbeat_sent_count++;
            }
            next_heartbeat = make_timeout_time_ms(MCU_UART_HEARTBEAT_MS);
        }
#endif

        if (telemetry_host_attached()) {
            print_link_configuration();
            print_telemetry_header();
            next_telemetry = make_timeout_time_ms(TELEMETRY_PERIOD_MS);
        }

        /*
         * Counters are cumulative and are never reset on reconnect, so a capture
         * that starts late still reports totals for the whole run.
         */
        if (stdio_usb_connected() &&
            absolute_time_diff_us(get_absolute_time(), next_telemetry) <= 0) {
            print_telemetry_row();
            g_counters.telemetry_sent_count++;
            next_telemetry = make_timeout_time_ms(TELEMETRY_PERIOD_MS);
        }

        tight_loop_contents();
    }
}
