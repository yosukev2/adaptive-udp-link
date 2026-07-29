# mcu_uart_link

Raspberry Pi Pico firmware for the MCU UART Link Control Demo.

The firmware receives packet v1 `DATA` frames from the PC harness over UART,
replies with `ACK`, and emits `mcu_telemetry.csv` rows over USB CDC.

## Layout

| File | Role |
|------|------|
| `mcu_uart_protocol.c` / `.h` | Portable packet v1 builder and stream parser. No Pico SDK dependency. |
| `main.c` | Pico application: UART setup, ACK reply, telemetry emission. |
| `test_mcu_uart_protocol.c` | Host test for the parser. See `HOST_TEST.md`. |
| `Makefile` | Host test build only. |
| `CMakeLists.txt` | Pico SDK firmware build. |

The parser is deliberately free of SDK calls so it can be tested on the host
before it ever runs on the target.

## Channels

| Channel | Wiring | Contents |
|---------|--------|----------|
| Packet link | `uart0`, GPIO0 = TX, GPIO1 = RX, 115200 8N1 | `DATA` in, `ACK` out |
| Telemetry | USB CDC | `mcu_telemetry.csv` rows |

Telemetry is kept off the packet UART so counter output can never be mistaken
for protocol bytes.

## Host Test

Run the parser tests before flashing:

```bash
make -C firmware/mcu_uart_link test
```

## Build

```bash
export PICO_SDK_PATH=/path/to/pico-sdk
cmake -G Ninja -S firmware/mcu_uart_link -B firmware/mcu_uart_link/build
cmake --build firmware/mcu_uart_link/build
```

UF2 output path:

```text
firmware/mcu_uart_link/build/mcu_uart_link.uf2
```

If a locally built `picotool` fails during the UF2 step, the ELF/BIN are still
produced; install `picotool` separately or reconfigure with
`-DMCU_UART_LINK_ENABLE_PICOTOOL=OFF` and convert the BIN yourself.

## Flash

```bash
export PICO_MOUNT=/media/$USER/RPI-RP2
cp firmware/mcu_uart_link/build/mcu_uart_link.uf2 "$PICO_MOUNT/"
```

## Run

See `docs/mcu_uart/baseline_runbook.md` for wiring, telemetry capture, and the
baseline PASS criteria.

## UART Contract

- Packet format: `docs/mcu_uart/protocol.md`
- Telemetry counters: `docs/mcu_uart/telemetry_schema.md`
- Log schema: `docs/mcu_uart/log_schema.md`

Telemetry must be saved as `logs/mcu_uart/<trial_id>/mcu_telemetry.csv`.
