#!/usr/bin/env python3
"""Merge Linux/Pico jitter CSV files into one normalized comparison CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

COMMON_FIELDNAMES = [
    "env",
    "board",
    "sample_index",
    "period_target_us",
    "timestamp_us",
    "delta_us",
    "jitter_us",
]
PARTIAL_FIELDNAMES = COMMON_FIELDNAMES[2:]
ENV_METADATA = {
    "linux": ("linux_rpi5", "raspberry_pi_5"),
    "pico": ("pico", "raspberry_pi_pico"),
}


class CSVValidationError(ValueError):
    """Raised when a CSV row or header does not match the expected schema."""


@dataclass(frozen=True)
class InputSpec:
    label: str
    path: Path
    env: str
    board: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Merge Linux/Pico raw jitter CSV files and normalize them to the "
            "W06 comparison schema."
        )
    )
    parser.add_argument(
        "--linux-input",
        default="data/w06/linux_jitter_raw.csv",
        help="Path to the Linux raw CSV (default: %(default)s).",
    )
    parser.add_argument(
        "--pico-input",
        default="data/w06/pico_jitter_raw.csv",
        help="Path to the Pico raw CSV (default: %(default)s).",
    )
    parser.add_argument(
        "--output",
        default="data/w06/jitter_comparison.csv",
        help="Path to the merged comparison CSV (default: %(default)s).",
    )
    return parser.parse_args()


def nonempty_lines(handle):
    for line in handle:
        if line.strip():
            yield line


def required_value(row: dict[str, str | None], key: str, line_no: int) -> str:
    raw = row.get(key)
    value = "" if raw is None else raw.strip()
    if not value:
        raise CSVValidationError(f"{key} is empty at {line_no}")
    return value


def parse_int(value: str, key: str, line_no: int) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise CSVValidationError(f"{key} must be an integer at {line_no}: {value!r}") from exc


def detect_header(fieldnames: list[str]) -> bool:
    fields = set(fieldnames)
    if fields == set(COMMON_FIELDNAMES):
        return True
    if fields == set(PARTIAL_FIELDNAMES):
        return False

    raise CSVValidationError(
        "unexpected header. expected one of "
        f"{COMMON_FIELDNAMES} or {PARTIAL_FIELDNAMES}, got {fieldnames}"
    )


def normalize_row(
    row: dict[str, str | None],
    line_no: int,
    spec: InputSpec,
    has_identity_columns: bool,
) -> dict[str, str]:
    normalized = {
        "env": spec.env,
        "board": spec.board,
    }

    if has_identity_columns:
        env_value = required_value(row, "env", line_no)
        board_value = required_value(row, "board", line_no)
        if env_value != spec.env:
            raise CSVValidationError(
                f"env mismatch at {line_no}: expected {spec.env!r}, got {env_value!r}"
            )
        if board_value != spec.board:
            raise CSVValidationError(
                f"board mismatch at {line_no}: expected {spec.board!r}, got {board_value!r}"
            )

    for key in PARTIAL_FIELDNAMES:
        value = parse_int(required_value(row, key, line_no), key, line_no)
        normalized[key] = str(value)

    return normalized


def validate_rows(rows: list[dict[str, str]], spec: InputSpec) -> None:
    if not rows:
        raise CSVValidationError(f"{spec.path} has no data rows")

    previous_timestamp: int | None = None
    for offset, row in enumerate(rows, start=1):
        line_no = offset + 1
        sample_index = int(row["sample_index"])
        period_target_us = int(row["period_target_us"])
        timestamp_us = int(row["timestamp_us"])
        delta_us = int(row["delta_us"])
        jitter_us = int(row["jitter_us"])

        if sample_index != offset:
            raise CSVValidationError(
                f"sample_index must be sequential from 1 at {line_no}: got {sample_index}"
            )
        if period_target_us <= 0:
            raise CSVValidationError(f"period_target_us must be > 0 at {line_no}")
        if timestamp_us <= 0:
            raise CSVValidationError(f"timestamp_us must be > 0 at {line_no}")
        if delta_us <= 0:
            raise CSVValidationError(f"delta_us must be > 0 at {line_no}")
        if jitter_us != delta_us - period_target_us:
            raise CSVValidationError(
                f"jitter_us must equal delta_us - period_target_us at {line_no}"
            )

        if previous_timestamp is not None and timestamp_us - previous_timestamp != delta_us:
            raise CSVValidationError(
                "timestamp_us must advance by delta_us at "
                f"{line_no}: previous={previous_timestamp}, current={timestamp_us}, "
                f"delta_us={delta_us}"
            )
        previous_timestamp = timestamp_us


def load_rows(spec: InputSpec) -> list[dict[str, str]]:
    try:
        handle = spec.path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise CSVValidationError(f"failed to open {spec.path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(nonempty_lines(handle))
        if reader.fieldnames is None:
            raise CSVValidationError(f"{spec.path} is missing a CSV header")

        fieldnames = [field.strip() for field in reader.fieldnames]
        has_identity_columns = detect_header(fieldnames)

        rows: list[dict[str, str]] = []
        for line_no, row in enumerate(reader, start=2):
            rows.append(normalize_row(row, line_no, spec, has_identity_columns))

    validate_rows(rows, spec)
    return rows


def write_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COMMON_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    specs = [
        InputSpec("linux", Path(args.linux_input), *ENV_METADATA["linux"]),
        InputSpec("pico", Path(args.pico_input), *ENV_METADATA["pico"]),
    ]

    try:
        merged_rows: list[dict[str, str]] = []
        counts: dict[str, int] = {}
        for spec in specs:
            rows = load_rows(spec)
            merged_rows.extend(rows)
            counts[spec.label] = len(rows)
        write_rows(merged_rows, Path(args.output))
    except CSVValidationError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(
        f"[INFO] wrote {args.output} "
        f"(linux_rows={counts['linux']}, pico_rows={counts['pico']}, total_rows={len(merged_rows)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
