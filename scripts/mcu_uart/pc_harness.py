#!/usr/bin/env python3
"""MCU UART packet v1 の PC 側 dry-run/serial harness。"""

from __future__ import annotations

import argparse
import binascii
import csv
import os
import struct
import sys
import time
from dataclasses import dataclass
from pathlib import Path


PREAMBLE = 0xA55AC33C
VERSION = 1
HEADER_LEN = 16
MAX_PAYLOAD_LEN = 1024

PACKET_TYPES = {
    0x01: "DATA",
    0x02: "ACK",
    0x03: "NACK",
    0x10: "TELEMETRY",
    0x11: "HEARTBEAT",
    0x7F: "ERROR",
}

TYPE_DATA = 0x01

TX_COLUMNS = [
    "trial_id",
    "seq",
    "packet_type",
    "payload_len",
    "tx_wall_ns",
    "tx_mono_ns",
    "payload_text",
    "packet_hex",
    "crc32",
    "dry_run",
    "port",
    "baudrate",
]

RX_COLUMNS = [
    "trial_id",
    "seq",
    "packet_type",
    "payload_len",
    "rx_wall_ns",
    "rx_mono_ns",
    "payload_text",
    "packet_hex",
    "crc32",
    "crc_ok",
    "parse_error",
    "port",
    "baudrate",
]

METADATA_COLUMNS = [
    "trial_id",
    "test_name",
    "firmware_version",
    "baudrate",
    "packet_count",
    "payload_len",
    "port",
    "dry_run",
    "hardware_observed",
    "baseline_status",
    "created_wall_ns",
]


@dataclass(frozen=True)
class Packet:
    packet_type: int
    seq: int
    payload: bytes
    crc32: int
    raw: bytes


def crc32_ieee(data: bytes) -> int:
    return binascii.crc32(data) & 0xFFFFFFFF


def crc_input(packet_type: int, seq: int, payload: bytes) -> bytes:
    if len(payload) > MAX_PAYLOAD_LEN:
        raise ValueError(f"payload too large: {len(payload)} > {MAX_PAYLOAD_LEN}")
    return struct.pack(">BBIH", VERSION, packet_type, seq, len(payload)) + payload


def build_packet(packet_type: int, seq: int, payload: bytes) -> Packet:
    crc = crc32_ieee(crc_input(packet_type, seq, payload))
    raw = struct.pack(">IBBIHI", PREAMBLE, VERSION, packet_type, seq, len(payload), crc) + payload
    return Packet(packet_type=packet_type, seq=seq, payload=payload, crc32=crc, raw=raw)


def packet_type_name(packet_type: int) -> str:
    return PACKET_TYPES.get(packet_type, f"UNKNOWN_0x{packet_type:02X}")


def payload_for(seq: int, payload_len: int, trial_id: str) -> bytes:
    if payload_len > MAX_PAYLOAD_LEN:
        raise ValueError(f"payload_len must be <= {MAX_PAYLOAD_LEN}")
    base = f"{trial_id}:seq={seq:08d};".encode("ascii", errors="replace")
    if payload_len <= len(base):
        return base[:payload_len]
    return base + (b"." * (payload_len - len(base)))


def payload_text(payload: bytes) -> str:
    return payload.decode("ascii", errors="replace")


def parse_packets(buffer: bytearray) -> tuple[list[Packet], list[str]]:
    packets: list[Packet] = []
    errors: list[str] = []
    preamble_bytes = PREAMBLE.to_bytes(4, "big")

    while True:
        start = buffer.find(preamble_bytes)
        if start < 0:
            if buffer:
                errors.append(f"preamble_miss_bytes={len(buffer)}")
                buffer.clear()
            break
        if start > 0:
            errors.append(f"preamble_miss_bytes={start}")
            del buffer[:start]
        if len(buffer) < HEADER_LEN:
            break

        preamble, version, packet_type, seq, length, wire_crc = struct.unpack(">IBBIHI", buffer[:HEADER_LEN])
        if preamble != PREAMBLE:
            errors.append("bad_preamble")
            del buffer[0]
            continue
        if version != VERSION:
            errors.append(f"bad_version={version}")
            del buffer[0]
            continue
        if length > MAX_PAYLOAD_LEN:
            errors.append(f"bad_length={length}")
            del buffer[0]
            continue
        total_len = HEADER_LEN + length
        if len(buffer) < total_len:
            break

        raw = bytes(buffer[:total_len])
        payload = raw[HEADER_LEN:]
        calc_crc = crc32_ieee(crc_input(packet_type, seq, payload))
        if calc_crc != wire_crc:
            errors.append(f"bad_crc_seq={seq}")
            del buffer[0]
            continue

        packets.append(Packet(packet_type=packet_type, seq=seq, payload=payload, crc32=wire_crc, raw=raw))
        del buffer[:total_len]

    return packets, errors


def open_serial(port: str, baudrate: int, timeout: float):
    try:
        import serial  # type: ignore
    except ImportError as exc:
        raise SystemExit("pyserial がありません。実 UART 実行には `python -m pip install pyserial` が必要です。") from exc
    return serial.Serial(port=port, baudrate=baudrate, timeout=timeout)


def write_metadata(path: Path, args: argparse.Namespace) -> None:
    row = {
        "trial_id": args.trial_id,
        "test_name": args.test_name,
        "firmware_version": args.firmware_version,
        "baudrate": args.baudrate,
        "packet_count": args.packet_count,
        "payload_len": args.payload_len,
        "port": args.port or "",
        "dry_run": str(args.dry_run).lower(),
        "hardware_observed": str(not args.dry_run).lower(),
        "baseline_status": "template_only" if args.dry_run else "hardware_run",
        "created_wall_ns": time.time_ns(),
    }
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=METADATA_COLUMNS)
        writer.writeheader()
        writer.writerow(row)


def run(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    tx_path = output_dir / "pc_tx_log.csv"
    rx_path = output_dir / "pc_rx_log.csv"
    metadata_path = output_dir / "run_metadata.csv"

    serial_port = None
    if not args.dry_run:
        if not args.port:
            raise SystemExit("--port is required unless --dry-run is set")
        serial_port = open_serial(args.port, args.baudrate, args.timeout)

    write_metadata(metadata_path, args)

    rx_buffer = bytearray()
    with tx_path.open("w", newline="", encoding="utf-8") as tx_file, rx_path.open("w", newline="", encoding="utf-8") as rx_file:
        tx_writer = csv.DictWriter(tx_file, fieldnames=TX_COLUMNS)
        rx_writer = csv.DictWriter(rx_file, fieldnames=RX_COLUMNS)
        tx_writer.writeheader()
        rx_writer.writeheader()

        for seq in range(args.packet_count):
            payload = payload_for(seq, args.payload_len, args.trial_id)
            packet = build_packet(TYPE_DATA, seq, payload)
            tx_wall_ns = time.time_ns()
            tx_mono_ns = time.monotonic_ns()

            if serial_port is not None:
                serial_port.write(packet.raw)
                serial_port.flush()

            tx_writer.writerow(
                {
                    "trial_id": args.trial_id,
                    "seq": seq,
                    "packet_type": packet_type_name(packet.packet_type),
                    "payload_len": len(payload),
                    "tx_wall_ns": tx_wall_ns,
                    "tx_mono_ns": tx_mono_ns,
                    "payload_text": payload_text(payload),
                    "packet_hex": packet.raw.hex(),
                    "crc32": f"0x{packet.crc32:08X}",
                    "dry_run": str(args.dry_run).lower(),
                    "port": args.port or "",
                    "baudrate": args.baudrate,
                }
            )

            if serial_port is not None:
                deadline = time.monotonic() + args.timeout
                while time.monotonic() < deadline:
                    chunk = serial_port.read(256)
                    if not chunk:
                        break
                    rx_buffer.extend(chunk)
                    packets, errors = parse_packets(rx_buffer)
                    for parsed in packets:
                        rx_writer.writerow(
                            {
                                "trial_id": args.trial_id,
                                "seq": parsed.seq,
                                "packet_type": packet_type_name(parsed.packet_type),
                                "payload_len": len(parsed.payload),
                                "rx_wall_ns": time.time_ns(),
                                "rx_mono_ns": time.monotonic_ns(),
                                "payload_text": payload_text(parsed.payload),
                                "packet_hex": parsed.raw.hex(),
                                "crc32": f"0x{parsed.crc32:08X}",
                                "crc_ok": "true",
                                "parse_error": "",
                                "port": args.port or "",
                                "baudrate": args.baudrate,
                            }
                        )
                    for error in errors:
                        rx_writer.writerow(
                            {
                                "trial_id": args.trial_id,
                                "seq": "",
                                "packet_type": "",
                                "payload_len": "",
                                "rx_wall_ns": time.time_ns(),
                                "rx_mono_ns": time.monotonic_ns(),
                                "payload_text": "",
                                "packet_hex": "",
                                "crc32": "",
                                "crc_ok": "false",
                                "parse_error": error,
                                "port": args.port or "",
                                "baudrate": args.baudrate,
                            }
                        )
            time.sleep(args.interval_sec)

    if serial_port is not None:
        serial_port.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PC-side MCU UART packet v1 harness")
    parser.add_argument("--port", default="", help="Serial port, for example /dev/ttyUSB0 or COM5")
    parser.add_argument("--baudrate", type=int, default=115200)
    parser.add_argument("--trial-id", default=time.strftime("mcu_uart_%Y%m%d_%H%M%S"))
    parser.add_argument("--test-name", default="m0_baseline_10pkt")
    parser.add_argument("--firmware-version", default="unknown")
    parser.add_argument("--packet-count", type=int, default=10)
    parser.add_argument("--payload-len", type=int, default=16)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--timeout", type=float, default=0.2)
    parser.add_argument("--interval-sec", type=float, default=0.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.packet_count < 0:
        parser.error("--packet-count must be >= 0")
    if args.payload_len < 0 or args.payload_len > MAX_PAYLOAD_LEN:
        parser.error(f"--payload-len must be 0..{MAX_PAYLOAD_LEN}")
    if not args.output_dir:
        args.output_dir = os.path.join("logs", "mcu_uart", args.trial_id)
    return args


def main(argv: list[str] | None = None) -> int:
    run(parse_args(sys.argv[1:] if argv is None else argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
