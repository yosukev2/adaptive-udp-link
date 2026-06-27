#!/usr/bin/env python3
"""Validate W08 send-interval sweep CSVs and generate comparison summaries."""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
from dataclasses import dataclass
from pathlib import Path


EXPECTED_FIELDS = [
    "rcv_time_ns",
    "seq",
    "send_time_ns",
    "latency_ns",
    "missing_delta",
    "parse_status",
]

EXPECTED_TRIALS = (1, 2, 3)
EXPECTED_RATES = (50, 200, 500, 1000, 10000)


class CSVValidationError(ValueError):
    """Raised when a W08 run does not satisfy the measurement schema."""


@dataclass(frozen=True)
class RunData:
    rate_hz: int
    trial: int
    path: Path
    sample_count: int
    mean_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    max_latency_ms: float
    stddev_latency_ms: float
    last_latency_ms: float
    ok_count: int
    parse_error_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze W08 send-interval sweep CSV runs."
    )
    parser.add_argument(
        "--data-dir",
        default="data/w08/send_interval",
        help="Directory containing rate_<hz>_run<n>.csv files.",
    )
    parser.add_argument(
        "--summary-csv",
        default="data/w08/send_interval/w08_send_interval_summary.csv",
        help="Generated machine-readable summary CSV.",
    )
    parser.add_argument(
        "--report",
        default="reports/w08_send_interval_summary.md",
        help="Generated Markdown comparison report.",
    )
    return parser.parse_args()


def parse_int(value: str | None, field: str, path: Path, line_no: int) -> int:
    text = (value or "").strip()
    try:
        return int(text)
    except ValueError as exc:
        raise CSVValidationError(
            f"{path}:{line_no}: {field} must be an integer, got {text!r}"
        ) from exc


def nearest_rank(sorted_values: list[int], percentile: int) -> int:
    if not sorted_values:
        raise ValueError("percentile input is empty")
    rank = max(1, math.ceil(percentile / 100.0 * len(sorted_values)))
    return sorted_values[rank - 1]


def load_run(path: Path, rate_hz: int, trial: int) -> RunData:
    latencies_ns: list[int] = []
    ok_count = 0
    parse_error_count = 0
    previous_seq: int | None = None

    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise CSVValidationError(f"failed to open {path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        header = [field.strip() for field in reader.fieldnames or []]
        if header != EXPECTED_FIELDS:
            raise CSVValidationError(
                f"{path}: unexpected header; expected {EXPECTED_FIELDS}, got {header}"
            )

        row_count = 0
        for row_count, row in enumerate(reader, start=1):
            line_no = row_count + 1
            seq = parse_int(row.get("seq"), "seq", path, line_no)
            latency_ns = parse_int(row.get("latency_ns"), "latency_ns", path, line_no)
            missing_delta = parse_int(
                row.get("missing_delta"), "missing_delta", path, line_no
            )
            parse_status = (row.get("parse_status") or "").strip()

            expected_seq = row_count - 1
            if seq != expected_seq:
                raise CSVValidationError(
                    f"{path}:{line_no}: seq {seq} != expected {expected_seq}"
                )
            if previous_seq is not None and seq != previous_seq + 1:
                raise CSVValidationError(
                    f"{path}:{line_no}: seq {seq} is not consecutive"
                )
            if missing_delta < 0:
                raise CSVValidationError(
                    f"{path}:{line_no}: missing_delta must be non-negative"
                )

            if parse_status == "OK":
                ok_count += 1
                latencies_ns.append(latency_ns)
            else:
                parse_error_count += 1

            previous_seq = seq

    if row_count == 0:
        raise CSVValidationError(f"{path}: no data rows")

    if ok_count == 0:
        raise CSVValidationError(f"{path}: no OK rows")

    sorted_latencies = sorted(latencies_ns)
    mean_latency_ms = statistics.fmean(sorted_latencies) / 1_000_000.0
    stddev_latency_ms = (
        statistics.pstdev(sorted_latencies) / 1_000_000.0
        if len(sorted_latencies) > 1
        else 0.0
    )
    p50_latency_ms = nearest_rank(sorted_latencies, 50) / 1_000_000.0
    p95_latency_ms = nearest_rank(sorted_latencies, 95) / 1_000_000.0
    p99_latency_ms = nearest_rank(sorted_latencies, 99) / 1_000_000.0
    max_latency_ms = max(sorted_latencies) / 1_000_000.0
    last_latency_ms = latencies_ns[-1] / 1_000_000.0

    return RunData(
        rate_hz=rate_hz,
        trial=trial,
        path=path,
        sample_count=row_count,
        mean_latency_ms=mean_latency_ms,
        p50_latency_ms=p50_latency_ms,
        p95_latency_ms=p95_latency_ms,
        p99_latency_ms=p99_latency_ms,
        max_latency_ms=max_latency_ms,
        stddev_latency_ms=stddev_latency_ms,
        last_latency_ms=last_latency_ms,
        ok_count=ok_count,
        parse_error_count=parse_error_count,
    )


def discover_runs(data_dir: Path) -> list[RunData]:
    discovered: list[RunData] = []
    pattern = re.compile(r"^rate_(\d+)_run([0-9]+)\.csv$")

    for path in sorted(data_dir.glob("rate_*_run*.csv")):
        match = pattern.match(path.name)
        if match is None:
            continue
        rate_hz = int(match.group(1))
        trial = int(match.group(2))
        discovered.append(load_run(path, rate_hz, trial))

    if not discovered:
        raise CSVValidationError(f"no run CSV files found in {data_dir}")

    discovered.sort(key=lambda run: (run.rate_hz, run.trial))
    return discovered


def write_summary_csv(path: Path, runs: list[RunData]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "rate_hz",
                "trial",
                "sample_count",
                "ok_count",
                "parse_error_count",
                "mean_latency_ms",
                "p50_latency_ms",
                "p95_latency_ms",
                "p99_latency_ms",
                "max_latency_ms",
                "stddev_latency_ms",
                "last_latency_ms",
            ]
        )
        for run in runs:
            writer.writerow(
                [
                    run.rate_hz,
                    run.trial,
                    run.sample_count,
                    run.ok_count,
                    run.parse_error_count,
                    f"{run.mean_latency_ms:.6f}",
                    f"{run.p50_latency_ms:.6f}",
                    f"{run.p95_latency_ms:.6f}",
                    f"{run.p99_latency_ms:.6f}",
                    f"{run.max_latency_ms:.6f}",
                    f"{run.stddev_latency_ms:.6f}",
                    f"{run.last_latency_ms:.6f}",
                ]
            )


def build_report(runs: list[RunData]) -> str:
    lines: list[str] = []
    lines.append("# W08 send interval sweep summary")
    lines.append("")
    lines.append("## run-level summary")
    lines.append("")
    lines.append(
        "| rate_hz | trial | sample_count | mean_latency_ms | p50_ms | p95_ms | p99_ms | max_ms | stddev_ms | last_ms |"
    )
    lines.append(
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
    )
    for run in runs:
        lines.append(
            f"| {run.rate_hz} | {run.trial} | {run.sample_count} | "
            f"{run.mean_latency_ms:.6f} | {run.p50_latency_ms:.6f} | "
            f"{run.p95_latency_ms:.6f} | {run.p99_latency_ms:.6f} | "
            f"{run.max_latency_ms:.6f} | {run.stddev_latency_ms:.6f} | {run.last_latency_ms:.6f} |"
        )

    lines.append("")
    lines.append("## rate-level aggregate")
    lines.append("")
    lines.append(
        "| rate_hz | trials | mean_of_mean_ms | mean_p95_ms | mean_p99_ms | mean_max_ms |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")

    by_rate: dict[int, list[RunData]] = {}
    for run in runs:
        by_rate.setdefault(run.rate_hz, []).append(run)

    for rate_hz in sorted(by_rate):
        grouped = by_rate[rate_hz]
        mean_of_mean = statistics.fmean(run.mean_latency_ms for run in grouped)
        mean_p95 = statistics.fmean(run.p95_latency_ms for run in grouped)
        mean_p99 = statistics.fmean(run.p99_latency_ms for run in grouped)
        mean_max = statistics.fmean(run.max_latency_ms for run in grouped)
        lines.append(
            f"| {rate_hz} | {len(grouped)} | {mean_of_mean:.6f} | "
            f"{mean_p95:.6f} | {mean_p99:.6f} | {mean_max:.6f} |"
        )

    lines.append("")
    lines.append("## notes")
    lines.append("")
    lines.append("- `rate_hz` が比較変数です。")
    lines.append("- それ以外の条件は baseline に合わせて固定してください。")
    lines.append("- `last_ms` は末尾の挙動確認用の補助値です。")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    data_dir = Path(args.data_dir)
    runs = discover_runs(data_dir)

    observed_rates = sorted({run.rate_hz for run in runs})
    if observed_rates != list(EXPECTED_RATES):
        raise CSVValidationError(
            f"unexpected rate set {observed_rates}; expected {list(EXPECTED_RATES)}"
        )
    trial_counts = {
        rate: sorted(run.trial for run in runs if run.rate_hz == rate)
        for rate in EXPECTED_RATES
    }
    for rate, trials in trial_counts.items():
        if tuple(trials) != EXPECTED_TRIALS:
            raise CSVValidationError(
                f"rate {rate}: unexpected trial set {trials}; expected {list(EXPECTED_TRIALS)}"
            )

    summary_csv = Path(args.summary_csv)
    report = Path(args.report)
    write_summary_csv(summary_csv, runs)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(build_report(runs), encoding="utf-8")

    print(f"OK: analyzed {len(runs)} runs")
    print(f"wrote: {summary_csv}")
    print(f"wrote: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
