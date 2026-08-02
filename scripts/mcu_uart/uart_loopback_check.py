#!/usr/bin/env python3
"""Confirm a UART port can transmit and receive by looping TX back into RX.

Short the port's TX and RX pins together before running. Routing the short
through a jumper wire puts that wire under test as well, which is how a broken
lead is told apart from a broken port.

    python3 scripts/mcu_uart/uart_loopback_check.py /dev/ttyAMA2
"""

from __future__ import annotations

import sys
import time

PAYLOAD = b"LOOPBACK0123456789"


def main(argv: list[str]) -> int:
    port = argv[1] if len(argv) > 1 else "/dev/ttyAMA2"
    baudrate = int(argv[2]) if len(argv) > 2 else 115200

    try:
        import serial  # type: ignore
    except ImportError:
        raise SystemExit("pyserial is required: python3 -m pip install pyserial")

    with serial.Serial(port, baudrate, timeout=1) as link:
        link.reset_input_buffer()
        link.write(PAYLOAD)
        link.flush()
        time.sleep(0.2)
        received = link.read(len(PAYLOAD))

    print(f"port={port} baudrate={baudrate}")
    print(f"sent={PAYLOAD!r}")
    print(f"recv={received!r}")

    if received == PAYLOAD:
        print("RESULT: PASS")
        return 0

    print(f"RESULT: FAIL ({len(received)}/{len(PAYLOAD)} bytes returned)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
