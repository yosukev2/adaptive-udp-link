# MCU UART Telemetry Schema

## Purpose

Telemetry counters make MCU UART tests measurable. The counters below are the minimum set required to judge normal reception, error detection, recovery behavior, memory pressure, and safe-state transitions.

All counters are unsigned monotonically increasing values within one MCU boot unless explicitly stated otherwise.

## State Values

| State | Meaning |
|-------|---------|
| `BOOT` | Firmware initialized but UART parser is not ready |
| `IDLE` | Parser is ready and waiting for packets |
| `RUN` | Valid packets are being processed |
| `DEGRADED` | Link timeout or repeated errors detected |
| `RECOVER` | Valid traffic observed after degraded state |
| `SAFE` | Parser or buffer fault requires manual or watchdog recovery |

## Error Codes

| Code | Name | Meaning |
|-----:|------|---------|
| 0 | `OK` | No error |
| 1 | `BAD_PREAMBLE` | Preamble search skipped bytes |
| 2 | `BAD_VERSION` | Unsupported packet version |
| 3 | `BAD_TYPE` | Unknown packet type |
| 4 | `BAD_LENGTH` | Payload length exceeded max or frame was truncated |
| 5 | `BAD_CRC` | CRC mismatch |
| 6 | `SEQ_GAP` | Sequence gap detected |
| 7 | `DUPLICATE` | Duplicate sequence observed |
| 8 | `TIMEOUT` | UART receive timeout |
| 9 | `BUFFER_OVERFLOW` | RX buffer could not accept more bytes |
| 10 | `SAFE_ENTERED` | Firmware entered safe state |

## Counter Definitions

| Counter | Meaning | Increment Condition | Summary Column |
|---------|---------|---------------------|----------------|
| `rx_byte_count` | UART bytes received | Every byte read from UART | `rx_byte_count` |
| `rx_packet_count` | Complete valid packets accepted | Header, length, and CRC are valid | `received_count` |
| `rx_data_count` | Valid `DATA` packets accepted | Accepted packet type is `DATA` | `received_data_count` |
| `tx_packet_count` | Packets sent by MCU | ACK/NACK/telemetry/heartbeat written to UART | `mcu_tx_packet_count` |
| `ack_sent_count` | ACK packets sent | Valid packet requires ACK | `ack_sent_count` |
| `nack_sent_count` | NACK packets sent | Invalid packet produces NACK | `nack_sent_count` |
| `telemetry_sent_count` | Telemetry snapshots sent | MCU emits `TELEMETRY` packet or CSV row | `telemetry_sent_count` |
| `heartbeat_sent_count` | HEARTBEAT packets sent | Periodic heartbeat transmission | `heartbeat_sent_count` |
| `crc_error_count` | CRC failures | Recomputed CRC differs from wire CRC | `crc_error_count` |
| `seq_gap_count` | Estimated missing sequence count | Accepted `seq` is greater than expected `seq` | `seq_gap_count` |
| `duplicate_count` | Duplicate accepted/candidate packet count | Packet `seq` already observed in current trial | `duplicate_count` |
| `timeout_count` | Receive or parser timeouts | Partial packet or idle receive exceeds configured timeout | `timeout_count` |
| `preamble_miss_count` | Bytes skipped before preamble match | Parser discards a byte while searching for preamble | `preamble_miss_count` |
| `invalid_version_count` | Unsupported version packets | Header version is not `1` | `invalid_version_count` |
| `invalid_type_count` | Unknown packet types | Type is not in packet type table | `invalid_type_count` |
| `length_error_count` | Length validation failures | `length > 1024` or packet truncated | `length_error_count` |
| `rx_buffer_overflow_count` | RX buffer overflow events | Incoming byte cannot be stored | `overflow_count` |
| `rx_buffer_miss_count` | Parser could not read expected buffered byte | Ring buffer underflow/miss in parser path | `buffer_miss_count` |
| `recover_enter_count` | Recovery attempts started | State transitions to `RECOVER` | `recover_enter_count` |
| `recovered_count` | Recovery completed | State returns from `RECOVER` or `DEGRADED` to `RUN`/`IDLE` | `recovered_count` |
| `unrecovered_count` | Recovery failed | Timeout/error threshold sends state to `SAFE` | `unrecovered_count` |
| `safe_enter_count` | Safe-state entries | State transitions to `SAFE` | `safe_enter_count` |
| `reset_count` | Firmware resets observed | Boot counter value increments or startup telemetry reports reset | `reset_count` |

## Snapshot Fields

Telemetry rows and telemetry packets should include the current values of these non-counter fields:

| Field | Type | Meaning | Summary Column |
|-------|------|---------|----------------|
| `trial_id` | string | Current trial identifier | `trial_id` |
| `mono_ms` | `uint32` or `uint64` | MCU monotonic milliseconds since boot | latest telemetry reference |
| `state` | enum string or integer | Current link state | `final_state` |
| `last_error_code` | integer | Most recent error code | `last_error_code` |
| `last_seq` | `uint32` | Last accepted sequence | `last_seq` |
| `expected_seq` | `uint32` | Next expected sequence | `expected_seq` |
| `rx_buffer_used` | integer bytes | Current RX buffer occupancy | `rx_buffer_used_max` |
| `rx_buffer_capacity` | integer bytes | RX buffer capacity | `rx_buffer_capacity` |

## Event-to-Counter Matrix

| Event | Counters that must increase |
|-------|-----------------------------|
| Valid `DATA` seq 0 | `rx_byte_count`, `rx_packet_count`, `rx_data_count`, optionally `ack_sent_count` |
| Valid `DATA` seq jumps from 0 to 3 | `rx_packet_count`, `rx_data_count`, `seq_gap_count += 2` |
| Duplicate `DATA` seq 3 | `duplicate_count`, optionally `rx_packet_count` if accepted |
| Payload bit flip | `crc_error_count`, optionally `nack_sent_count` |
| Unsupported type `0x55` | `invalid_type_count`, optionally `nack_sent_count` |
| Length `2048` | `length_error_count`, optionally `nack_sent_count` |
| UART idle timeout while receiving partial packet | `timeout_count` |
| Ring buffer full | `rx_buffer_overflow_count`, `last_error_code=BUFFER_OVERFLOW` |
| Link returns to healthy traffic after degraded state | `recover_enter_count`, then `recovered_count` |
| Repeated errors force safe mode | `unrecovered_count`, `safe_enter_count`, `state=SAFE` |

## CSV Mapping

`mcu_telemetry.csv` should store one row per telemetry snapshot. `summary.csv` should use the last row in the trial for final counter values unless a column is an aggregate such as max buffer usage.

| `mcu_telemetry.csv` Column | `summary.csv` Column | Rule |
|----------------------------|----------------------|------|
| `rx_packet_count` | `received_count` | Last value |
| `rx_data_count` | `received_data_count` | Last value |
| `crc_error_count` | `crc_error_count` | Last value |
| `seq_gap_count` | `seq_gap_count` | Last value |
| `duplicate_count` | `duplicate_count` | Last value |
| `rx_buffer_overflow_count` | `overflow_count` | Last value |
| `rx_buffer_miss_count` | `buffer_miss_count` | Last value |
| `recovered_count` | `recovered_count` | Last value |
| `unrecovered_count` | `unrecovered_count` | Last value |
| `safe_enter_count` | `safe_enter_count` | Last value |
| `reset_count` | `reset_count` | Last value |
| `state` | `final_state` | Last value |
| `last_error_code` | `last_error_code` | Last value |
| `rx_buffer_used` | `rx_buffer_used_max` | Maximum value in trial |

## Normal Baseline Expectations

For the M0 10-packet baseline with no fault injection:

| Counter | Expected |
|---------|----------|
| `rx_data_count` | 10 |
| `crc_error_count` | 0 |
| `seq_gap_count` | 0 |
| `duplicate_count` | 0 |
| `timeout_count` | 0 after run starts, except allowed post-run idle timeout if documented |
| `rx_buffer_overflow_count` | 0 |
| `rx_buffer_miss_count` | 0 |
| `unrecovered_count` | 0 |
| `safe_enter_count` | 0 |
| `state` | `RUN` or `IDLE` |
