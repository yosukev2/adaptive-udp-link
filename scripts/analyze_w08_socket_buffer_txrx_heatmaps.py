#!/usr/bin/env python3
"""Analyze W08 TX/RX socket buffer matrix and generate heatmaps.

Expected input:
- data/w08/socket_buffer_txrx_matrix/run_metadata.md
- data/w08/socket_buffer_txrx_matrix/rate_<hz>_rcvbuf_<bytes>_sndbuf_<bytes>_run<trial>.csv

Heatmap layout:
- one image per rate_hz and metric
- y-axis: SO_SNDBUF requested/actual
- x-axis: SO_RCVBUF requested/actual
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
    r"rate_(?P<rate>\d+)_rcvbuf_(?P<rcvbuf>\d+)_sndbuf_(?P<sndbuf>\d+)_run(?P<trial>\d+)\.csv$"
)


@dataclass(frozen=True)
class Metadata:
    rate_hz: int
    rcvbuf_requested: int
    sndbuf_requested: int
    trial: int
    rcvbuf_actual: int | None
    sndbuf_actual: int | None
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None


@dataclass(frozen=True)
class RunSummary:
    rate_hz: int
    rcvbuf_requested: int
    rcvbuf_actual: int | None
    sndbuf_requested: int
    sndbuf_actual: int | None
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
    source_csv: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate W08 TX/RX socket buffer heatmaps.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/w08/socket_buffer_txrx_matrix"))
    parser.add_argument("--summary-csv", type=Path, default=Path("reports/w08_socket_buffer_txrx_matrix_summary.csv"))
    parser.add_argument("--report", type=Path, default=Path("reports/w08_socket_buffer_txrx_matrix_summary.md"))
    parser.add_argument("--fig-dir", type=Path, default=Path("reports/figures"))
    return parser.parse_args()


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_metadata(path: Path) -> dict[tuple[int, int, int, int], Metadata]:
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

    result: dict[tuple[int, int, int, int], Metadata] = {}
    for block in blocks:
        rate_hz = parse_int(block.get("rate_hz"))
        rcvbuf_requested = parse_int(block.get("rcvbuf_requested"))
        sndbuf_requested = parse_int(block.get("sndbuf_requested"))
        trial = parse_int(block.get("trial"))
        if rate_hz is None or rcvbuf_requested is None or sndbuf_requested is None or trial is None:
            continue
        result[(rate_hz, rcvbuf_requested, sndbuf_requested, trial)] = Metadata(
            rate_hz=rate_hz,
            rcvbuf_requested=rcvbuf_requested,
            sndbuf_requested=sndbuf_requested,
            trial=trial,
            rcvbuf_actual=parse_int(block.get("rcvbuf_actual")),
            sndbuf_actual=parse_int(block.get("sndbuf_actual")),
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
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return sorted_values[int(pos)]
    weight = pos - lower
    return sorted_values[lower] * (1.0 - weight) + sorted_values[upper] * weight


def analyze_csv(path: Path, metadata: Metadata | None) -> RunSummary:
    match = FILENAME_RE.search(path.name)
    if not match:
        raise ValueError(f"unexpected file name: {path}")

    rate_hz = int(match.group("rate"))
    rcvbuf_requested = int(match.group("rcvbuf"))
    sndbuf_requested = int(match.group("sndbuf"))
    trial = int(match.group("trial"))

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_FIELDS:
            raise ValueError(f"unexpected CSV header in {path}: {reader.fieldnames}")
        latencies_ms: list[float] = []
        sample_count = 0
        ok_count = 0
        parse_error_count = 0
        missing_delta_total = 0
        for row in reader:
            sample_count += 1
            if row["parse_status"] == "ok":
                ok_count += 1
            else:
                parse_error_count += 1
            missing_delta_total += int(row["missing_delta"])
            latencies_ms.append(int(row["latency_ns"]) / 1_000_000.0)

    sorted_latencies = sorted(latencies_ms)
    missing_rate = missing_delta_total / sample_count if sample_count else math.nan
    return RunSummary(
        rate_hz=rate_hz,
        rcvbuf_requested=rcvbuf_requested,
        rcvbuf_actual=metadata.rcvbuf_actual if metadata else None,
        sndbuf_requested=sndbuf_requested,
        sndbuf_actual=metadata.sndbuf_actual if metadata else None,
        trial=trial,
        sample_count=sample_count,
        ok_count=ok_count,
        parse_error_count=parse_error_count,
        missing_delta_total=missing_delta_total,
        missing_rate=missing_rate,
        mean_latency_ms=statistics.fmean(latencies_ms) if latencies_ms else math.nan,
        p50_latency_ms=percentile(sorted_latencies, 0.50),
        p95_latency_ms=percentile(sorted_latencies, 0.95),
        p99_latency_ms=percentile(sorted_latencies, 0.99),
        max_latency_ms=max(latencies_ms) if latencies_ms else math.nan,
        tx_status=metadata.tx_status if metadata else None,
        rx_status=metadata.rx_status if metadata else None,
        copy_status=metadata.copy_status if metadata else None,
        run_validity=metadata.run_validity if metadata else None,
        source_csv=path,
    )


def load_runs(data_dir: Path) -> list[RunSummary]:
    metadata = parse_metadata(data_dir / "run_metadata.md")
    runs: list[RunSummary] = []
    for path in sorted(data_dir.glob("rate_*_rcvbuf_*_sndbuf_*_run*.csv")):
        match = FILENAME_RE.search(path.name)
        if not match:
            continue
        key = (
            int(match.group("rate")),
            int(match.group("rcvbuf")),
            int(match.group("sndbuf")),
            int(match.group("trial")),
        )
        runs.append(analyze_csv(path, metadata.get(key)))
    if not runs:
        raise SystemExit(f"no run CSV files found in {data_dir}")
    return runs


def write_run_summary(path: Path, runs: list[RunSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rate_hz",
            "rcvbuf_requested",
            "rcvbuf_actual",
            "sndbuf_requested",
            "sndbuf_actual",
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
            "tx_status",
            "rx_status",
            "copy_status",
            "run_validity",
            "source_csv",
        ])
        for run in runs:
            writer.writerow([
                run.rate_hz,
                run.rcvbuf_requested,
                run.rcvbuf_actual if run.rcvbuf_actual is not None else "",
                run.sndbuf_requested,
                run.sndbuf_actual if run.sndbuf_actual is not None else "",
                run.trial,
                run.sample_count,
                run.ok_count,
                run.parse_error_count,
                run.missing_delta_total,
                f"{run.missing_rate:.8f}",
                f"{run.mean_latency_ms:.9f}",
                f"{run.p50_latency_ms:.9f}",
                f"{run.p95_latency_ms:.9f}",
                f"{run.p99_latency_ms:.9f}",
                f"{run.max_latency_ms:.9f}",
                run.tx_status if run.tx_status is not None else "",
                run.rx_status if run.rx_status is not None else "",
                run.copy_status if run.copy_status is not None else "",
                run.run_validity if run.run_validity is not None else "",
                run.source_csv.as_posix(),
            ])


def aggregate(runs: list[RunSummary]) -> list[dict[str, float | int | str]]:
    groups: dict[tuple[int, int, int | None, int, int | None], list[RunSummary]] = defaultdict(list)
    for run in runs:
        groups[(run.rate_hz, run.rcvbuf_requested, run.rcvbuf_actual, run.sndbuf_requested, run.sndbuf_actual)].append(run)

    rows: list[dict[str, float | int | str]] = []
    for (rate, rcv_req, rcv_act, snd_req, snd_act), group in sorted(groups.items()):
        rows.append({
            "rate_hz": rate,
            "rcvbuf_requested": rcv_req,
            "rcvbuf_actual": rcv_act if rcv_act is not None else "",
            "sndbuf_requested": snd_req,
            "sndbuf_actual": snd_act if snd_act is not None else "",
            "trials": len(group),
            "samples_avg": statistics.fmean(run.sample_count for run in group),
            "missing_avg": statistics.fmean(run.missing_delta_total for run in group),
            "missing_rate_avg": statistics.fmean(run.missing_rate for run in group),
            "mean_latency_ms_avg": statistics.fmean(run.mean_latency_ms for run in group),
            "p95_latency_ms_avg": statistics.fmean(run.p95_latency_ms for run in group),
            "p99_latency_ms_avg": statistics.fmean(run.p99_latency_ms for run in group),
            "max_latency_ms_avg": statistics.fmean(run.max_latency_ms for run in group),
        })
    return rows


def write_aggregate_summary(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    agg_path = path.with_name(path.stem.replace("_summary", "_aggregate_summary") + path.suffix)
    with agg_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def label(requested: int, actual: int | str) -> str:
    return f"{requested}/{actual}"


def draw_heatmap(rows: list[dict[str, float | int | str]], rate: int, metric: str, title: str, output: Path, cmap: str) -> None:
    rate_rows = [row for row in rows if int(row["rate_hz"]) == rate]
    if not rate_rows:
        return

    x_cols = sorted({(int(row["rcvbuf_requested"]), int(row["rcvbuf_actual"])) for row in rate_rows}, key=lambda v: (v[1], v[0]))
    y_rows = sorted({(int(row["sndbuf_requested"]), int(row["sndbuf_actual"])) for row in rate_rows}, key=lambda v: (v[1], v[0]))
    index = {
        (int(row["rcvbuf_requested"]), int(row["rcvbuf_actual"]), int(row["sndbuf_requested"]), int(row["sndbuf_actual"])): row
        for row in rate_rows
    }

    matrix: list[list[float]] = []
    for snd_req, snd_act in y_rows:
        line: list[float] = []
        for rcv_req, rcv_act in x_cols:
            row = index.get((rcv_req, rcv_act, snd_req, snd_act))
            line.append(float("nan") if row is None else float(row[metric]))
        matrix.append(line)

    fig, ax = plt.subplots(figsize=(max(7, len(x_cols) * 1.55), max(5, len(y_rows) * 0.75)), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("SO_RCVBUF requested/actual bytes")
    ax.set_ylabel("SO_SNDBUF requested/actual bytes")
    ax.set_xticks(range(len(x_cols)))
    ax.set_xticklabels([label(req, act) for req, act in x_cols], rotation=35, ha="right")
    ax.set_yticks(range(len(y_rows)))
    ax.set_yticklabels([label(req, act) for req, act in y_rows])
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(metric)

    for y, line in enumerate(matrix):
        for x, value in enumerate(line):
            if math.isnan(value):
                continue
            text = f"{value:.1f}" if metric == "missing_avg" else f"{value:.3f}"
            ax.text(x, y, text, ha="center", va="center", fontsize=8, color="black")

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def write_report(path: Path, runs: list[RunSummary], rows: list[dict[str, float | int | str]], fig_dir: Path) -> None:
    valid = sum(1 for run in runs if run.run_validity == "ok")
    rates = sorted({run.rate_hz for run in runs})
    rcv_pairs = sorted({(run.rcvbuf_requested, run.rcvbuf_actual) for run in runs}, key=lambda v: (v[1] or -1, v[0]))
    snd_pairs = sorted({(run.sndbuf_requested, run.sndbuf_actual) for run in runs}, key=lambda v: (v[1] or -1, v[0]))
    top_missing = sorted(rows, key=lambda row: float(row["missing_avg"]), reverse=True)[:10]
    top_p99 = sorted(rows, key=lambda row: float(row["p99_latency_ms_avg"]), reverse=True)[:10]

    lines: list[str] = []
    lines.append("# W08 #131 TX/RX socket buffer matrix summary")
    lines.append("")
    lines.append("## 結論")
    lines.append("")
    lines.append(f"- total runs: {len(runs)}")
    lines.append(f"- run_validity=ok: {valid}")
    lines.append("- 縦軸を `SO_SNDBUF requested/actual`、横軸を `SO_RCVBUF requested/actual` とした heatmap を生成した。")
    lines.append("- missing と latency は別指標として確認する。")
    lines.append("")
    lines.append("## 条件")
    lines.append("")
    lines.append(f"- rate_hz: `{' / '.join(map(str, rates))}`")
    lines.append(f"- SO_RCVBUF requested/actual: `{', '.join(label(req, act or '') for req, act in rcv_pairs)}`")
    lines.append(f"- SO_SNDBUF requested/actual: `{', '.join(label(req, act or '') for req, act in snd_pairs)}`")
    lines.append("- fixed: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none")
    lines.append("")
    lines.append("## missing 上位")
    lines.append("")
    lines.append("| rate_hz | rcv requested/actual | snd requested/actual | trials | missing_avg | p99_ms | max_ms |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in top_missing:
        lines.append(
            f"| {row['rate_hz']} | {row['rcvbuf_requested']}/{row['rcvbuf_actual']} | "
            f"{row['sndbuf_requested']}/{row['sndbuf_actual']} | {row['trials']} | "
            f"{float(row['missing_avg']):.1f} | {float(row['p99_latency_ms_avg']):.6f} | {float(row['max_latency_ms_avg']):.6f} |"
        )
    lines.append("")
    lines.append("## p99 latency 上位")
    lines.append("")
    lines.append("| rate_hz | rcv requested/actual | snd requested/actual | trials | p99_ms | missing_avg | max_ms |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in top_p99:
        lines.append(
            f"| {row['rate_hz']} | {row['rcvbuf_requested']}/{row['rcvbuf_actual']} | "
            f"{row['sndbuf_requested']}/{row['sndbuf_actual']} | {row['trials']} | "
            f"{float(row['p99_latency_ms_avg']):.6f} | {float(row['missing_avg']):.1f} | {float(row['max_latency_ms_avg']):.6f} |"
        )
    lines.append("")
    lines.append("## heatmaps")
    lines.append("")
    for rate in rates:
        for suffix, label_text in [
            ("missing_avg", "missing avg"),
            ("p99_latency_ms", "p99 latency ms"),
            ("mean_latency_ms", "mean latency ms"),
        ]:
            fig = fig_dir / f"w08_socket_buffer_txrx_rate_{rate}_{suffix}.png"
            lines.append(f"![rate {rate} {label_text}]({fig.as_posix().replace('reports/', '')})")
            lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    runs = load_runs(args.data_dir)
    write_run_summary(args.summary_csv, runs)
    rows = aggregate(runs)
    write_aggregate_summary(args.summary_csv, rows)

    for rate in sorted({run.rate_hz for run in runs}):
        draw_heatmap(
            rows,
            rate,
            "missing_avg",
            f"W08 TX/RX socket buffer rate={rate}: missing avg",
            args.fig_dir / f"w08_socket_buffer_txrx_rate_{rate}_missing_avg.png",
            "YlOrRd",
        )
        draw_heatmap(
            rows,
            rate,
            "p99_latency_ms_avg",
            f"W08 TX/RX socket buffer rate={rate}: p99 latency ms",
            args.fig_dir / f"w08_socket_buffer_txrx_rate_{rate}_p99_latency_ms.png",
            "YlGnBu",
        )
        draw_heatmap(
            rows,
            rate,
            "mean_latency_ms_avg",
            f"W08 TX/RX socket buffer rate={rate}: mean latency ms",
            args.fig_dir / f"w08_socket_buffer_txrx_rate_{rate}_mean_latency_ms.png",
            "YlGnBu",
        )
    write_report(args.report, runs, rows, args.fig_dir)
    print(f"OK: analyzed {len(runs)} runs")
    print(f"wrote: {args.summary_csv}")
    print(f"wrote: {args.summary_csv.with_name(args.summary_csv.stem.replace('_summary', '_aggregate_summary') + args.summary_csv.suffix)}")
    print(f"wrote: {args.report}")
    print(f"wrote figures under: {args.fig_dir}")


if __name__ == "__main__":
    main()
