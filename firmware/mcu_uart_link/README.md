# mcu_uart_link

This directory is the fixed location for MCU firmware used by the MCU UART Link Control Demo.

The default target is a Raspberry Pi Pico SDK style CMake project. Firmware source files are intentionally not fully implemented in M0; later issues can add `CMakeLists.txt`, UART parser code, and telemetry emission here without changing documented paths.

## Expected Build

```bash
export PICO_SDK_PATH=/path/to/pico-sdk
cmake -G Ninja -S firmware/mcu_uart_link -B firmware/mcu_uart_link/build
cmake --build firmware/mcu_uart_link/build
```

Expected UF2 path after firmware is added:

```text
firmware/mcu_uart_link/build/mcu_uart_link.uf2
```

## Expected Flash

```bash
export PICO_MOUNT=/media/$USER/RPI-RP2
cp firmware/mcu_uart_link/build/mcu_uart_link.uf2 "$PICO_MOUNT/"
```

## UART Contract

- Packet format: `docs/mcu_uart/protocol.md`
- Telemetry counters: `docs/mcu_uart/telemetry_schema.md`
- Log schema: `docs/mcu_uart/log_schema.md`

The firmware must emit telemetry that can be saved as `logs/mcu_uart/<trial_id>/mcu_telemetry.csv`.
