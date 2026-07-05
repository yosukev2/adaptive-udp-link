#!/usr/bin/env python3
"""MCU UART run logs から summary.csv を生成する。"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SUMMARY_COLUMNS = [
    "trial_id",
    "test_name",
    "firmware_version",
    "baudrate",
    "packet_count_configured",
    "payload_len_configured",
    "sent_count",
    "pc_received_count",
    "mcu_received_count",
    "received_count",
    "exact_match_count",
    "crc_error_count",
    "seq_gap_count",
    "duplicate_count",
    "overflow_count",
    "buffer_miss_count",
    "recovered_count",
    "unrecovered_count",
    "safe_enter_count",
    "reset_count",
    "final_state",
    "last_error_code",
    "hardware_observed",
    "baseline_status",
    "pass_fail",
    "note",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def last_int(rows: list[dict[str, str]], key: str, default: int = 0) -> int:
    for row in reversed(rows):
        value = row.get(key, "")
        if value != "":
            try:
                return int(value)
            except ValueError:
                return default
    return default


def last_value(rows: list[dict[str, str]], key: str, default: str = "") -> str:
    for row in reversed(rows):
        value = row.get(key, "")
        if value != "":
            return value
    return default


def metadata_value(metadata: dict[str, str], key: str, default: str = "") -> str:
    value = metadata.get(key, "")
    return value if value != "" else default


def exact_match_count(tx_rows: list[dict[str, str]], rx_rows: list[dict[str, str]]) -> int:
    tx_by_seq = {row.get("seq", ""): row for row in tx_rows if row.get("seq", "") != ""}
    count = 0
    for rx in rx_rows:
        seq = rx.get("seq", "")
        if seq == "" or rx.get("crc_ok", "").lower() == "false":
            continue
        tx = tx_by_seq.get(seq)
        if not tx:
            continue
        if tx.get("payload_text", "") == rx.get("payload_text", ""):
            count += 1
    return count


def summarize(input_dir: Path, note: str) -> dict[str, str]:
    metadata_rows = read_csv_rows(input_dir / "run_metadata.csv")
    tx_rows = read_csv_rows(input_dir / "pc_tx_log.csv")
    rx_rows = read_csv_rows(input_dir / "pc_rx_log.csv")
    telemetry_rows = read_csv_rows(input_dir / "mcu_telemetry.csv")
    metadata = metadata_rows[0] if metadata_rows else {}

    sent_count = len(tx_rows)
    pc_received_count = sum(1 for row in rx_rows if row.get("seq", "") != "" and row.get("crc_ok", "").lower() != "false")
    mcu_received_count = last_int(telemetry_rows, "rx_data_count", default=0)
    received_count = mcu_received_count if telemetry_rows else pc_received_count
    match_count = exact_match_count(tx_rows, rx_rows)

    crc_error_count = last_int(telemetry_rows, "crc_error_count", default=sum(1 for row in rx_rows if row.get("parse_error", "").startswith("bad_crc")))
    seq_gap_count = last_int(telemetry_rows, "seq_gap_count", default=0)
    duplicate_count = last_int(telemetry_rows, "duplicate_count", default=0)
    overflow_count = last_int(telemetry_rows, "rx_buffer_overflow_count", default=0)
    buffer_miss_count = last_int(telemetry_rows, "rx_buffer_miss_count", default=0)
    recovered_count = last_int(telemetry_rows, "recovered_count", default=0)
    unrecovered_count = last_int(telemetry_rows, "unrecovered_count", default=0)
    safe_enter_count = last_int(telemetry_rows, "safe_enter_count", default=0)
    reset_count = last_int(telemetry_rows, "reset_count", default=0)
    final_state = last_value(telemetry_rows, "state", default="NO_MCU_TELEMETRY")
    last_error_code = last_value(telemetry_rows, "last_error_code", default="")
    hardware_observed = metadata_value(metadata, "hardware_observed", "false" if not telemetry_rows else "true")
    baseline_status = metadata_value(metadata, "baseline_status", "template_only" if hardware_observed == "false" else "hardware_run")

    if hardware_observed == "false":
        pass_fail = "TEMPLATE_ONLY"
    elif (
        sent_count > 0
        and received_count == sent_count
        and crc_error_count == 0
        and seq_gap_count == 0
        and duplicate_count == 0
        and overflow_count == 0
        and buffer_miss_count == 0
        and unrecovered_count == 0
        and safe_enter_count == 0
    ):
        pass_fail = "PASS"
    else:
        pass_fail = "FAIL"

    return {
        "trial_id": metadata_value(metadata, "trial_id", tx_rows[0].get("trial_id", "") if tx_rows else ""),
        "test_name": metadata_value(metadata, "test_name", ""),
        "firmware_version": metadata_value(metadata, "firmware_version", ""),
        "baudrate": metadata_value(metadata, "baudrate", ""),
        "packet_count_configured": metadata_value(metadata, "packet_count", ""),
        "payload_len_configured": metadata_value(metadata, "payload_len", ""),
        "sent_count": str(sent_count),
        "pc_received_count": str(pc_received_count),
        "mcu_received_count": str(mcu_received_count),
        "received_count": str(received_count),
        "exact_match_count": str(match_count),
        "crc_error_count": str(crc_error_count),
        "seq_gap_count": str(seq_gap_count),
        "duplicate_count": str(duplicate_count),
        "overflow_count": str(overflow_count),
        "buffer_miss_count": str(buffer_miss_count),
        "recovered_count": str(recovered_count),
        "unrecovered_count": str(unrecovered_count),
        "safe_enter_count": str(safe_enter_count),
        "reset_count": str(reset_count),
        "final_state": final_state,
        "last_error_code": last_error_code,
        "hardware_observed": hardware_observed,
        "baseline_status": baseline_status,
        "pass_fail": pass_fail,
        "note": note,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate MCU UART summary.csv")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--note", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output = Path(args.output) if args.output else input_dir / "summary.csv"
    row = summarize(input_dir, args.note)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerow(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
