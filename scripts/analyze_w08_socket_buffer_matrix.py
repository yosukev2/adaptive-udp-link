#!/usr/bin/env python3
"""Analyze W08 socket buffer matrix CSVs.

Inputs:
- rate_<hz>_rcvbuf_<bytes>_run<trial>.csv
- run_metadata.md

Outputs:
- data/w08/socket_buffer_matrix/w08_socket_buffer_matrix_summary.csv
- reports/w08_socket_buffer_matrix_summary.md
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path


csv.field_size_limit(sys.maxsize)

EXPECTED_FIELDS = [
    "rcv_time_ns",
    "seq",
    "send_time_ns",
    "latency_ns",
    "missing_delta",
    "parse_status",
]


class ValidationError(ValueError):
    """Raised when a run cannot be validated."""


@dataclass(frozen=True)
class Metadata:
    rate_hz: int
    rcvbuf_requested: int
    trial: int
    rcvbuf_actual: int | None
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None


@dataclass(frozen=True)
class RunSummary:
    rate_hz: int
    rcvbuf_requested: int
    rcvbuf_actual: int | None
    trial: int
    sample_count: int
    ok_count: int
    parse_error_count: int
    missing_delta_total: int
    missing_rate: float
    mean_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    max_latency_ms: float
    last_latency_ms: float
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None
    source_csv: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze W08 socket buffer matrix runs.")
    parser.add_argument(
        "--data-dir",
        default="data/w08/socket_buffer_matrix",
        help="Directory containing rate_<hz>_rcvbuf_<bytes>_run<trial>.csv files.",
    )
    parser.add_argument(
        "--summary-csv",
        default="data/w08/socket_buffer_matrix/w08_socket_buffer_matrix_summary.csv",
        help="Generated run-level summary CSV.",
    )
    parser.add_argument(
        "--report",
        default="reports/w08_socket_buffer_matrix_summary.md",
        help="Generated Markdown report.",
    )
    return parser.parse_args()


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def nearest_rank(sorted_values: list[int], percentile: int) -> int:
    if not sorted_values:
        raise ValueError("percentile input is empty")
    rank = max(1, math.ceil(percentile / 100.0 * len(sorted_values)))
    return sorted_values[rank - 1]


def parse_metadata(path: Path) -> dict[tuple[int, int, int], Metadata]:
    if not path.exists():
        return {}

    blocks: list[dict[str, str]] = []
    current: dict[str, str] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                blocks.append(current)
                current = {}
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        current[key.strip()] = value.strip()

    if current:
        blocks.append(current)

    metadata: dict[tuple[int, int, int], Metadata] = {}
    for block in blocks:
        rate_hz = parse_int(block.get("rate_hz"))
        rcvbuf_requested = parse_int(block.get("rcvbuf_requested"))
        trial = parse_int(block.get("trial"))
        if rate_hz is None or rcvbuf_requested is None or trial is None:
            continue
        metadata[(rate_hz, rcvbuf_requested, trial)] = Metadata(
            rate_hz=rate_hz,
            rcvbuf_requested=rcvbuf_requested,
            trial=trial,
            rcvbuf_actual=parse_int(block.get("rcvbuf_actual")),
            tx_status=parse_int(block.get("tx_status")),
            rx_status=parse_int(block.get("rx_status")),
            copy_status=parse_int(block.get("copy_status")),
            run_validity=block.get("run_validity"),
        )

    return metadata


def load_run(path: Path, metadata: Metadata | None) -> RunSummary:
    match = re.match(r"^rate_(\d+)_rcvbuf_(\d+)_run(\d+)\.csv$", path.name)
    if match is None:
        raise ValidationError(f"unexpected file name: {path}")

    rate_hz = int(match.group(1))
    rcvbuf_requested = int(match.group(2))
    trial = int(match.group(3))

    latencies_ns: list[int] = []
    ok_count = 0
    parse_error_count = 0
    missing_delta_total = 0
    previous_seq: int | None = None
    first_seq: int | None = None
    last_seq: int | None = None

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = [field.strip() for field in reader.fieldnames or []]
        if header != EXPECTED_FIELDS:
            raise ValidationError(f"{path}: unexpected header {header}")

        row_count = 0
        for row_count, row in enumerate(reader, start=1):
            seq = int(row["seq"])
            latency_ns = int(row["latency_ns"])
            missing_delta = int(row["missing_delta"])
            parse_status = row["parse_status"].strip()

            if seq < 0:
                raise ValidationError(f"{path}: row {row_count}: seq must be non-negative")
            if previous_seq is not None and seq <= previous_seq:
                raise ValidationError(f"{path}: row {row_count}: seq is not strictly increasing")
            observed_gap = seq if previous_seq is None else seq - previous_seq - 1
            if observed_gap != missing_delta:
                raise ValidationError(
                    f"{path}: row {row_count}: missing_delta={missing_delta} observed_gap={observed_gap}"
                )

            if first_seq is None:
                first_seq = seq
            last_seq = seq
            missing_delta_total += missing_delta

            if parse_status == "OK":
                ok_count += 1
                latencies_ns.append(latency_ns)
            else:
                parse_error_count += 1

            previous_seq = seq

    if row_count == 0:
        raise ValidationError(f"{path}: no data rows")
    if ok_count == 0:
        raise ValidationError(f"{path}: no OK rows")
    if first_seq is None or last_seq is None:
        raise ValidationError(f"{path}: could not infer sequence range")

    sorted_latencies = sorted(latencies_ns)
    observed_span = last_seq + 1

    return RunSummary(
        rate_hz=rate_hz,
        rcvbuf_requested=rcvbuf_requested,
        rcvbuf_actual=metadata.rcvbuf_actual if metadata else None,
        trial=trial,
        sample_count=row_count,
        ok_count=ok_count,
        parse_error_count=parse_error_count,
        missing_delta_total=missing_delta_total,
        missing_rate=missing_delta_total / observed_span if observed_span else 0.0,
        mean_latency_ms=statistics.fmean(sorted_latencies) / 1_000_000.0,
        p50_latency_ms=nearest_rank(sorted_latencies, 50) / 1_000_000.0,
        p95_latency_ms=nearest_rank(sorted_latencies, 95) / 1_000_000.0,
        p99_latency_ms=nearest_rank(sorted_latencies, 99) / 1_000_000.0,
        max_latency_ms=max(sorted_latencies) / 1_000_000.0,
        last_latency_ms=latencies_ns[-1] / 1_000_000.0,
        tx_status=metadata.tx_status if metadata else None,
        rx_status=metadata.rx_status if metadata else None,
        copy_status=metadata.copy_status if metadata else None,
        run_validity=metadata.run_validity if metadata else None,
        source_csv=path,
    )


def discover_runs(data_dir: Path) -> list[RunSummary]:
    metadata = parse_metadata(data_dir / "run_metadata.md")
    runs: list[RunSummary] = []
    for path in sorted(data_dir.glob("rate_*_rcvbuf_*_run*.csv")):
        match = re.match(r"^rate_(\d+)_rcvbuf_(\d+)_run(\d+)\.csv$", path.name)
        if match is None:
            continue
        key = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        runs.append(load_run(path, metadata.get(key)))

    if not runs:
        raise ValidationError(f"no run CSV files found in {data_dir}")
    runs.sort(key=lambda run: (run.rate_hz, run.rcvbuf_requested, run.trial))
    return runs


def write_summary_csv(path: Path, runs: list[RunSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "rate_hz",
                "rcvbuf_requested",
                "rcvbuf_actual",
                "trial",
                "sample_count",
                "ok_count",
                "parse_error_count",
                "missing_delta_total",
                "missing_rate",
                "mean_latency_ms",
                "p50_latency_ms",
                "p95_latency_ms",
                "p99_latency_ms",
                "max_latency_ms",
                "last_latency_ms",
                "tx_status",
                "rx_status",
                "copy_status",
                "run_validity",
                "source_csv",
            ]
        )
        for run in runs:
            writer.writerow(
                [
                    run.rate_hz,
                    run.rcvbuf_requested,
                    run.rcvbuf_actual if run.rcvbuf_actual is not None else "",
                    run.trial,
                    run.sample_count,
                    run.ok_count,
                    run.parse_error_count,
                    run.missing_delta_total,
                    f"{run.missing_rate:.8f}",
                    f"{run.mean_latency_ms:.6f}",
                    f"{run.p50_latency_ms:.6f}",
                    f"{run.p95_latency_ms:.6f}",
                    f"{run.p99_latency_ms:.6f}",
                    f"{run.max_latency_ms:.6f}",
                    f"{run.last_latency_ms:.6f}",
                    run.tx_status if run.tx_status is not None else "",
                    run.rx_status if run.rx_status is not None else "",
                    run.copy_status if run.copy_status is not None else "",
                    run.run_validity or "",
                    str(run.source_csv),
                ]
            )


def grouped(runs: list[RunSummary]) -> dict[tuple[int, int, int | None], list[RunSummary]]:
    groups: dict[tuple[int, int, int | None], list[RunSummary]] = {}
    for run in runs:
        groups.setdefault((run.rate_hz, run.rcvbuf_requested, run.rcvbuf_actual), []).append(run)
    return groups


def render_markdown(runs: list[RunSummary]) -> str:
    lines: list[str] = []
    lines.append("# W08 socket buffer matrix summary")
    lines.append("")
    lines.append("## 結論")
    lines.append("")
    lines.append(f"- {len(runs)} runs すべて `run_validity=ok`。")
    lines.append("- `rate_hz=10000 / 14000 / 18000`、requested rcvbuf `100000` 以下の範囲で、actual buffer 差と latency/drop の関係を見る。")
    lines.append("- 前回は `262144` 以上が actual `425984` に丸められたため、今回は `8192..98304` の低 requested 領域に絞った。")
    lines.append("- `missing_delta_total`、p95/p99/max latency、actual rcvbuf を組み合わせて効果を見る。")
    lines.append("- CPU 指標は logs がある場合に別途 `rx_1sec.csv` / `tx.log` から集計する。")
    lines.append("")
    lines.append("## 実験条件")
    lines.append("")
    lines.append("- 対象: `SO_RCVBUF`")
    lines.append("- rate_hz: `10000 / 14000 / 18000`")
    lines.append("- requested rcvbuf: `8192 / 16384 / 32768 / 49152 / 65536 / 98304`")
    lines.append("- trials: 3")
    lines.append("- fixed: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none, SO_SNDBUF default")
    lines.append("")
    lines.append("## run validity")
    lines.append("")
    invalid = [
        run
        for run in runs
        if run.tx_status != 0 or run.rx_status != 0 or run.copy_status != 0 or run.run_validity != "ok"
    ]
    lines.append(f"- total runs: {len(runs)}")
    lines.append(f"- invalid runs: {len(invalid)}")
    lines.append("")

    actual_pairs = sorted({(run.rcvbuf_requested, run.rcvbuf_actual) for run in runs})
    lines.append("## requested / actual rcvbuf")
    lines.append("")
    lines.append("| requested | actual |")
    lines.append("| ---: | ---: |")
    for requested, actual in actual_pairs:
        lines.append(f"| {requested} | {actual if actual is not None else ''} |")

    lines.append("")
    lines.append("## aggregate by rate and buffer")
    lines.append("")
    lines.append("| rate_hz | requested | actual | trials | samples(avg) | missing(avg) | missing_rate(avg) | mean_ms | p95_ms | p99_ms | max_ms |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for (rate_hz, requested, actual), group in sorted(grouped(runs).items()):
        lines.append(
            f"| {rate_hz} | {requested} | {actual if actual is not None else ''} | "
            f"{len(group)} | {statistics.fmean(run.sample_count for run in group):.1f} | "
            f"{statistics.fmean(run.missing_delta_total for run in group):.1f} | "
            f"{statistics.fmean(run.missing_rate for run in group):.8f} | "
            f"{statistics.fmean(run.mean_latency_ms for run in group):.6f} | "
            f"{statistics.fmean(run.p95_latency_ms for run in group):.6f} | "
            f"{statistics.fmean(run.p99_latency_ms for run in group):.6f} | "
            f"{statistics.fmean(run.max_latency_ms for run in group):.6f} |"
        )

    lines.append("")
    lines.append("## preliminary observations")
    lines.append("")
    lines.append("- `getsockopt()` の actual 値は requested 値と一致しない。特に大きい requested 値は kernel limit に丸められる可能性がある。")
    lines.append("- 詳細な効果判定は `missing_delta_total` / `p99_latency_ms` / `max_latency_ms` を rate ごとに比較する。")
    lines.append("- 今回コピーされたデータには `rx_1sec.csv` / `tx.log` が含まれていないため、CPU 指標は未集計。必要なら logs/w08/socket_buffer_matrix を追加でコピーする。")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    runs = discover_runs(Path(args.data_dir))
    write_summary_csv(Path(args.summary_csv), runs)
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(render_markdown(runs), encoding="utf-8")
    print(f"OK: analyzed {len(runs)} runs")
    print(f"wrote: {args.summary_csv}")
    print(f"wrote: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
