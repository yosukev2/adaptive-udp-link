#!/usr/bin/env python3
"""Analyze W08 rate_hz x SO_RCVBUF matrix results.

Expected input:
  data/socket_buffer_rate_rcvbuf_matrix copied from Pi5

Input files:
  rate_<hz>_rcvbuf_<bytes>_sndbuf_default_run<trial>.csv

Outputs:
  - per-run summary CSV
  - aggregate CSV
  - heatmaps for missing / p99 latency / max latency
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import japanize_matplotlib  # noqa: F401  (registers Japanese font)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo", "Yu Gothic", "IPAexGothic"]

csv.field_size_limit(sys.maxsize)

EXPECTED_FIELDS = [
    "rcv_time_ns",
    "seq",
    "send_time_ns",
    "latency_ns",
    "missing_delta",
    "parse_status",
]

FILENAME_RE = re.compile(
    r"rate_(?P<rate>\d+)_rcvbuf_(?P<rcvbuf>\d+)_sndbuf_default_run(?P<trial>\d+)\.csv$"
)


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
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None
    source_csv: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze W08 rate_hz x SO_RCVBUF matrix.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(r"C:/tmp/adaptive-udp-link-issue-131-rate-rcvbuf/data/socket_buffer_rate_rcvbuf_matrix"),
    )
    parser.add_argument("--run-summary-csv", type=Path, default=Path("reports/w08_socket_buffer_rate_rcvbuf_run_summary.csv"))
    parser.add_argument("--aggregate-csv", type=Path, default=Path("reports/w08_socket_buffer_rate_rcvbuf_aggregate.csv"))
    parser.add_argument("--fig-dir", type=Path, default=Path("reports/figures"))
    return parser.parse_args()


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_metadata(path: Path) -> dict[tuple[int, int, int], Metadata]:
    if not path.exists():
        return {}
    blocks: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                blocks.append(current)
                current = {}
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        current[key] = value
    if current:
        blocks.append(current)

    result: dict[tuple[int, int, int], Metadata] = {}
    for block in blocks:
        rate_hz = parse_int(block.get("rate_hz"))
        rcvbuf_requested = parse_int(block.get("rcvbuf_requested"))
        trial = parse_int(block.get("trial"))
        if rate_hz is None or rcvbuf_requested is None or trial is None:
            continue
        result[(rate_hz, rcvbuf_requested, trial)] = Metadata(
            rate_hz=rate_hz,
            rcvbuf_requested=rcvbuf_requested,
            trial=trial,
            rcvbuf_actual=parse_int(block.get("rcvbuf_actual")),
            tx_status=parse_int(block.get("tx_status")),
            rx_status=parse_int(block.get("rx_status")),
            copy_status=parse_int(block.get("copy_status")),
            run_validity=block.get("run_validity"),
        )
    return result


def percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return math.nan
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * pct
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_values[int(pos)]
    weight = pos - lo
    return sorted_values[lo] * (1.0 - weight) + sorted_values[hi] * weight


def analyze_csv(path: Path, metadata: Metadata | None) -> RunSummary:
    match = FILENAME_RE.search(path.name)
    if not match:
        raise ValueError(f"unexpected file name: {path}")
    rate_hz = int(match.group("rate"))
    rcvbuf_requested = int(match.group("rcvbuf"))
    trial = int(match.group("trial"))

    latencies_ms: list[float] = []
    sample_count = 0
    ok_count = 0
    parse_error_count = 0
    missing_delta_total = 0
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_FIELDS:
            raise ValueError(f"unexpected CSV header in {path}: {reader.fieldnames}")
        for row in reader:
            sample_count += 1
            if row["parse_status"].upper() == "OK":
                ok_count += 1
            else:
                parse_error_count += 1
            missing_delta_total += int(row["missing_delta"])
            latencies_ms.append(int(row["latency_ns"]) / 1_000_000.0)

    sorted_latencies = sorted(latencies_ms)
    return RunSummary(
        rate_hz=rate_hz,
        rcvbuf_requested=rcvbuf_requested,
        rcvbuf_actual=metadata.rcvbuf_actual if metadata else None,
        trial=trial,
        sample_count=sample_count,
        ok_count=ok_count,
        parse_error_count=parse_error_count,
        missing_delta_total=missing_delta_total,
        missing_rate=(missing_delta_total / sample_count) if sample_count else math.nan,
        mean_latency_ms=statistics.fmean(latencies_ms) if latencies_ms else math.nan,
        p50_latency_ms=percentile(sorted_latencies, 0.50),
        p95_latency_ms=percentile(sorted_latencies, 0.95),
        p99_latency_ms=percentile(sorted_latencies, 0.99),
        max_latency_ms=max(latencies_ms) if latencies_ms else math.nan,
        tx_status=metadata.tx_status if metadata else None,
        rx_status=metadata.rx_status if metadata else None,
        copy_status=metadata.copy_status if metadata else None,
        run_validity=metadata.run_validity if metadata else None,
        source_csv=str(path),
    )


def load_runs(data_dir: Path) -> list[RunSummary]:
    metadata = parse_metadata(data_dir / "run_metadata.md")
    paths = sorted(data_dir.glob("rate_*_rcvbuf_*_sndbuf_default_run*.csv"))
    if not paths:
        raise FileNotFoundError(f"no input CSV files found under {data_dir}")
    runs: list[RunSummary] = []
    for i, path in enumerate(paths, 1):
        match = FILENAME_RE.search(path.name)
        if not match:
            continue
        key = (int(match.group("rate")), int(match.group("rcvbuf")), int(match.group("trial")))
        runs.append(analyze_csv(path, metadata.get(key)))
        if i % 10 == 0:
            print(f"analyzed {i}/{len(paths)} files", file=sys.stderr)
    return runs


def fmean(values: list[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    return statistics.fmean(vals) if vals else math.nan


def run_to_dict(run: RunSummary) -> dict[str, object]:
    return {
        "rate_hz": run.rate_hz,
        "rcvbuf_requested": run.rcvbuf_requested,
        "rcvbuf_actual": run.rcvbuf_actual,
        "trial": run.trial,
        "sample_count": run.sample_count,
        "ok_count": run.ok_count,
        "parse_error_count": run.parse_error_count,
        "missing_delta_total": run.missing_delta_total,
        "missing_rate": run.missing_rate,
        "mean_latency_ms": run.mean_latency_ms,
        "p50_latency_ms": run.p50_latency_ms,
        "p95_latency_ms": run.p95_latency_ms,
        "p99_latency_ms": run.p99_latency_ms,
        "max_latency_ms": run.max_latency_ms,
        "tx_status": run.tx_status,
        "rx_status": run.rx_status,
        "copy_status": run.copy_status,
        "run_validity": run.run_validity,
        "source_csv": run.source_csv,
    }


def aggregate(runs: list[RunSummary]) -> list[dict[str, object]]:
    groups: dict[tuple[int, int, int | None], list[RunSummary]] = defaultdict(list)
    for run in runs:
        groups[(run.rate_hz, run.rcvbuf_requested, run.rcvbuf_actual)].append(run)
    rows: list[dict[str, object]] = []
    for (rate_hz, rcvbuf_requested, rcvbuf_actual), group in sorted(groups.items()):
        rows.append(
            {
                "rate_hz": rate_hz,
                "rcvbuf_requested": rcvbuf_requested,
                "rcvbuf_actual": rcvbuf_actual,
                "runs": len(group),
                "sample_count_avg": fmean([float(g.sample_count) for g in group]),
                "missing_delta_total_avg": fmean([float(g.missing_delta_total) for g in group]),
                "missing_delta_total_max": max(g.missing_delta_total for g in group),
                "missing_rate_avg": fmean([g.missing_rate for g in group]),
                "mean_latency_ms_avg": fmean([g.mean_latency_ms for g in group]),
                "p50_latency_ms_avg": fmean([g.p50_latency_ms for g in group]),
                "p95_latency_ms_avg": fmean([g.p95_latency_ms for g in group]),
                "p99_latency_ms_avg": fmean([g.p99_latency_ms for g in group]),
                "max_latency_ms_avg": fmean([g.max_latency_ms for g in group]),
                "max_latency_ms_max": max(g.max_latency_ms for g in group),
                "parse_error_count_total": sum(g.parse_error_count for g in group),
                "invalid_runs": sum(1 for g in group if g.run_validity != "ok"),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def format_si(value: object) -> str:
    """Format 140000 -> 140k, 1000000 -> 1M, 4608 -> 4.6k; non-numeric passes through."""
    try:
        v = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return str(value)
    if v >= 1_000_000:
        scaled, unit = v / 1_000_000, "M"
    elif v >= 1_000:
        scaled, unit = v / 1_000, "k"
    else:
        return f"{v:g}"
    if scaled == int(scaled):
        return f"{int(scaled)}{unit}"
    return f"{scaled:.1f}{unit}"


def label_buf(requested: object, actual: object) -> str:
    return f"{format_si(requested)}/{format_si(actual)}" if actual not in (None, "") else format_si(requested)


def make_heatmap(rows: list[dict[str, object]], metric: str, output: Path, title: str, cbar_label: str, fmt: str) -> None:
    rates = sorted({int(row["rate_hz"]) for row in rows}, reverse=True)
    rcvbufs = sorted({int(row["rcvbuf_requested"]) for row in rows})
    labels = {
        int(row["rcvbuf_requested"]): label_buf(row["rcvbuf_requested"], row.get("rcvbuf_actual"))
        for row in rows
    }
    lookup = {(int(row["rate_hz"]), int(row["rcvbuf_requested"])): float(row[metric]) for row in rows}
    matrix = [[lookup.get((rate, rcvbuf), math.nan) for rcvbuf in rcvbufs] for rate in rates]

    fig, ax = plt.subplots(figsize=(9.5, 5.5), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap="Blues")
    ax.set_title(title, fontsize=17, pad=14)
    ax.set_xlabel("受信バッファ（要求値/実効値、byte）", fontsize=14, labelpad=10)
    ax.set_ylabel("送信レート (Hz)", fontsize=14, labelpad=10)
    ax.set_xticks(
        range(len(rcvbufs)),
        [labels[v] for v in rcvbufs],
        rotation=35,
        ha="right",
        fontsize=11,
    )
    ax.set_yticks(range(len(rates)), [format_si(v) for v in rates], fontsize=11)
    finite = [v for row in matrix for v in row if not math.isnan(v)]
    vmin = min(finite) if finite else 0.0
    vmax = max(finite) if finite else 1.0
    span = vmax - vmin
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if math.isnan(value):
                continue
            if fmt == "int":
                text = f"{value:.0f}"
            else:
                text = f"{value:.4f}"
            norm = (value - vmin) / span if span else 0.0
            color = "white" if norm > 0.6 else "black"
            ax.text(x, y, text, ha="center", va="center", fontsize=9, color=color)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(cbar_label, fontsize=13, labelpad=10)
    cbar.ax.tick_params(labelsize=11)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def markdown_table(rows: list[dict[str, object]], columns: list[tuple[str, str]]) -> str:
    lines = ["| " + " | ".join(title for _, title in columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in rows:
        values: list[str] = []
        for key, _ in columns:
            value = row.get(key, "")
            if isinstance(value, float):
                if math.isnan(value):
                    values.append("")
                elif "latency" in key or key.endswith("rate"):
                    values.append(f"{value:.6f}")
                else:
                    values.append(f"{value:.2f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    runs = load_runs(args.data_dir)
    rows = aggregate(runs)
    write_csv(args.run_summary_csv, [run_to_dict(r) for r in runs])
    write_csv(args.aggregate_csv, rows)

    figures = [
        args.fig_dir / "w08_socket_buffer_rate_rcvbuf_missing_delta_total_avg.png",
        args.fig_dir / "w08_socket_buffer_rate_rcvbuf_p99_latency_ms_avg.png",
        args.fig_dir / "w08_socket_buffer_rate_rcvbuf_max_latency_ms_avg.png",
    ]
    make_heatmap(rows, "missing_delta_total_avg", figures[0], "受信バッファ単独sweepの欠落合計（3回平均）", "欠落合計（3回平均）", "int")
    make_heatmap(rows, "p99_latency_ms_avg", figures[1], "受信バッファ単独sweepのP99遅延（3回平均）[ms]", "P99遅延（3回平均）[ms]", "float")
    make_heatmap(rows, "max_latency_ms_avg", figures[2], "受信バッファ単独sweepの最大遅延（3回平均）[ms]", "最大遅延（3回平均）[ms]", "float")

    print(f"runs={len(runs)}")
    print(f"aggregate_rows={len(rows)}")
    print(f"figures={len(figures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
