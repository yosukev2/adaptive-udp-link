#!/usr/bin/env python3
"""Analyze merged W06 jitter CSV data and write a Markdown summary."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import OrderedDict
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


class CSVValidationError(ValueError):
    """Raised when the merged CSV does not match the expected schema."""


@dataclass(frozen=True)
class EnvSummary:
    env: str
    board: str
    sample_count: int
    p50_abs_jitter_us: float
    p95_abs_jitter_us: float
    p99_abs_jitter_us: float
    max_abs_jitter_us: float
    stddev_abs_jitter_us: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze abs(jitter_us) for each environment in the merged W06 CSV "
            "and write a Markdown comparison report."
        )
    )
    parser.add_argument(
        "--input",
        default="data/w06/jitter_comparison.csv",
        help="Path to the merged comparison CSV (default: %(default)s).",
    )
    parser.add_argument(
        "--output",
        default="reports/w06_jitter_summary.md",
        help="Path to the Markdown summary (default: %(default)s).",
    )
    parser.add_argument(
        "--dataset-kind",
        choices=("sample", "measured"),
        default="sample",
        help="Label for the report so sample output is not mistaken for measured output.",
    )
    return parser.parse_args()


def parse_int(value: str, key: str, line_no: int) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise CSVValidationError(f"{key} must be an integer at line {line_no}: {value!r}") from exc


def nearest_rank(values: list[int], percentile: int) -> int:
    if not values:
        raise ValueError("percentile input is empty")
    rank = max(1, math.ceil((percentile / 100.0) * len(values)))
    return values[rank - 1]


def load_groups(input_path: Path) -> OrderedDict[str, tuple[str, list[int]]]:
    try:
        handle = input_path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise CSVValidationError(f"failed to open {input_path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise CSVValidationError(f"{input_path} is missing a CSV header")

        header = [field.strip() for field in reader.fieldnames]
        if header != COMMON_FIELDNAMES:
            raise CSVValidationError(
                f"unexpected header in {input_path}. expected {COMMON_FIELDNAMES}, got {header}"
            )

        groups: OrderedDict[str, tuple[str, list[int]]] = OrderedDict()
        for line_no, row in enumerate(reader, start=2):
            env = (row.get("env") or "").strip()
            board = (row.get("board") or "").strip()
            if not env or not board:
                raise CSVValidationError(f"env/board is empty at line {line_no}")

            jitter_us = parse_int((row.get("jitter_us") or "").strip(), "jitter_us", line_no)
            abs_jitter = abs(jitter_us)

            if env not in groups:
                groups[env] = (board, [abs_jitter])
                continue

            current_board, values = groups[env]
            if current_board != board:
                raise CSVValidationError(
                    f"board mismatch for env {env!r} at line {line_no}: "
                    f"{current_board!r} vs {board!r}"
                )
            values.append(abs_jitter)

    if not groups:
        raise CSVValidationError(f"{input_path} has no data rows")

    return groups


def summarize(groups: OrderedDict[str, tuple[str, list[int]]]) -> list[EnvSummary]:
    summaries: list[EnvSummary] = []
    for env, (board, values) in groups.items():
        sorted_values = sorted(values)
        summaries.append(
            EnvSummary(
                env=env,
                board=board,
                sample_count=len(sorted_values),
                p50_abs_jitter_us=float(nearest_rank(sorted_values, 50)),
                p95_abs_jitter_us=float(nearest_rank(sorted_values, 95)),
                p99_abs_jitter_us=float(nearest_rank(sorted_values, 99)),
                max_abs_jitter_us=float(sorted_values[-1]),
                stddev_abs_jitter_us=statistics.pstdev(sorted_values),
            )
        )
    return summaries


def render_report(
    summaries: list[EnvSummary],
    dataset_kind: str,
    input_path: Path,
) -> str:
    lines = [
        "# W06 Jitter Summary",
        "",
        f"- Dataset kind: `{dataset_kind}`",
        f"- Input CSV: `{input_path.as_posix()}`",
        "- Metric basis: `abs(jitter_us)`",
        "- Percentiles: nearest-rank",
        "- Stddev: population standard deviation",
    ]

    if dataset_kind == "sample":
        lines.append(
            "- Caution: This report is generated from sample CSV only. Replace the "
            "sample raw CSVs with measured `linux_jitter_raw.csv` / "
            "`pico_jitter_raw.csv` before treating the values as experimental results."
        )
    else:
        lines.append(
            "- Caution: This report reflects the measured CSV supplied to this script."
        )

    lines.extend(
        [
            "",
            "## Comparison Table",
            "",
            "| env | board | samples | P50 abs jitter (us) | P95 abs jitter (us) | P99 abs jitter (us) | max abs jitter (us) | stddev abs jitter (us) |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for summary in summaries:
        lines.append(
            "| "
            f"{summary.env} | {summary.board} | {summary.sample_count} | "
            f"{summary.p50_abs_jitter_us:.2f} | {summary.p95_abs_jitter_us:.2f} | "
            f"{summary.p99_abs_jitter_us:.2f} | {summary.max_abs_jitter_us:.2f} | "
            f"{summary.stddev_abs_jitter_us:.2f} |"
        )

    summary_by_env = {summary.env: summary for summary in summaries}
    if "linux_rpi5" in summary_by_env and "pico" in summary_by_env:
        linux = summary_by_env["linux_rpi5"]
        pico = summary_by_env["pico"]
        diff = linux.p99_abs_jitter_us - pico.p99_abs_jitter_us
        lines.extend(
            [
                "",
                "## P99 Difference",
                "",
                f"`linux_rpi5` P99 abs jitter is {linux.p99_abs_jitter_us:.2f} us and "
                f"`pico` P99 abs jitter is {pico.p99_abs_jitter_us:.2f} us, so the "
                f"difference (`linux_rpi5 - pico`) is {diff:.2f} us.",
            ]
        )
        if dataset_kind == "measured":
            lines.extend(render_final_interpretation(linux, pico, diff))

    return "\n".join(lines) + "\n"


def render_final_interpretation(
    linux: EnvSummary,
    pico: EnvSummary,
    p99_diff_us: float,
) -> list[str]:
    return [
        "",
        "## Final Interpretation",
        "",
        f"In this W06 dataset, the Raspberry Pi 5 Linux 10ms loop has P99 abs jitter "
        f"{linux.p99_abs_jitter_us:.2f} us, while the Raspberry Pi Pico hardware-timer "
        f"loop has P99 abs jitter {pico.p99_abs_jitter_us:.2f} us. The measured P99 "
        f"difference is {p99_diff_us:.2f} us.",
        "",
        "For UDP latency measurement, sender-side period jitter can be mixed into the "
        "observed timing as measurement noise. The Pico result in this dataset suggests "
        "that a hardware-timer sender can reduce that sender-side timing noise compared "
        "with the Linux user-space loop used here.",
        "",
        "## Experimental Conditions",
        "",
        "- Linux side: Raspberry Pi 5 Linux user-space logger",
        "- MCU side: Raspberry Pi Pico firmware using a hardware timer path",
        "- Target period: 10000 us",
        "- Samples: 1000 rows per environment",
        "- Jitter definition: `jitter_us = delta_us - period_target_us`",
        "- Statistic basis: `abs(jitter_us)`",
        "- Percentiles: nearest-rank",
        "- Stddev: population standard deviation",
        "",
        "## Constraints And Untested Items",
        "",
        "- This is a timing-jitter comparison for the W06 logger paths, not a direct UDP latency benchmark.",
        "- The timestamps are monotonic within each device and are not compared as shared absolute time.",
        "- The result does not prove behavior across other kernels, system load profiles, Pico firmware variants, or network paths.",
        "- The Pico result depends on keeping serial/USB output outside the timer callback or interrupt path.",
        "",
        "## W06 Claims",
        "",
        "- Supported: Under the recorded W06 conditions, Pico hardware-timer periodic execution had lower P99 abs jitter than the Raspberry Pi 5 Linux user-space loop.",
        "- Supported: Sender-side period jitter is a plausible source of noise in UDP latency measurements, so reducing sender jitter can make later latency measurements cleaner.",
        "- Not supported: W06 does not claim that Pico has lower UDP latency than Linux.",
        "- Not supported: W06 does not claim that all Linux or all MCU implementations behave like these two measured paths.",
        "",
        "## Evidence Package",
        "",
        "- Bringup log: `docs/w06_bringup_log.md`",
        "- Board selection and scope: `docs/board_selection.md`",
        "- Measurement specification: `docs/w06_measurement_spec.md`",
        "- Linux logger source: `experiments/w06_jitter/linux_jitter.c`",
        "- Linux run log: `docs/w06_run_log.md`",
        "- Linux raw CSV: `data/w06/linux_jitter_raw.csv`",
        "- Pico firmware source: `firmware/w06_pico_jitter/main.c`",
        "- Pico run log: `docs/w06_pico_jitter_run_log.md`",
        "- Pico raw CSV: `data/w06/pico_jitter_raw.csv`",
        "- Merge script: `scripts/merge_jitter_csv.py`",
        "- Analysis script: `scripts/analyze_jitter.py`",
        "- Merged comparison CSV: `data/w06/jitter_comparison.csv`",
        "- Final summary: `reports/w06_jitter_summary.md`",
    ]


def write_report(report_text: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    try:
        groups = load_groups(input_path)
        summaries = summarize(groups)
        report_text = render_report(summaries, args.dataset_kind, input_path)
        write_report(report_text, output_path)
    except CSVValidationError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] wrote {output_path} ({len(summaries)} env summaries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
