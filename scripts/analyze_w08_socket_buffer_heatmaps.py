#!/usr/bin/env python3
"""Generate W08 #131 socket buffer heatmaps.

The input summaries are per-run CSVs. This script aggregates trials by
(rate_hz, rcvbuf_requested, rcvbuf_actual), collapses kernel-ceiling actual
buffer values to one representative column, and writes heatmap PNGs.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

DEFAULT_INPUTS = [
    Path("data/w08/socket_buffer_matrix/w08_socket_buffer_matrix_summary.csv"),
    Path("data/w08/socket_buffer_matrix_lowbuf/w08_socket_buffer_matrix_lowbuf_summary.csv"),
    Path("data/w08/socket_buffer_tiny/w08_socket_buffer_tiny_summary.csv"),
]

CEILING_ACTUAL = 425984
CEILING_REP_REQUESTED = 262144


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate W08 socket buffer heatmaps.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports/figures"),
        help="Directory for heatmap PNGs.",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("reports/w08_socket_buffer_heatmap_summary.csv"),
        help="Aggregated CSV used as heatmap source.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        action="append",
        dest="inputs",
        help="Input summary CSV. Can be specified multiple times.",
    )
    return parser.parse_args()


def load_rows(paths: list[Path]) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("run_validity") != "ok":
                    continue
                requested = int(row["rcvbuf_requested"])
                actual = int(row["rcvbuf_actual"])
                if actual == CEILING_ACTUAL:
                    requested = CEILING_REP_REQUESTED
                rows.append(
                    {
                        "rate_hz": int(row["rate_hz"]),
                        "requested": requested,
                        "actual": actual,
                        "sample_count": int(row["sample_count"]),
                        "missing_delta_total": float(row["missing_delta_total"]),
                        "mean_latency_ms": float(row["mean_latency_ms"]),
                        "p99_latency_ms": float(row["p99_latency_ms"]),
                        "max_latency_ms": float(row["max_latency_ms"]),
                    }
                )
    if not rows:
        raise SystemExit("no input rows")
    return rows


def aggregate(rows: list[dict[str, float | int]]) -> list[dict[str, float | int]]:
    groups: dict[tuple[int, int, int], list[dict[str, float | int]]] = defaultdict(list)
    for row in rows:
        groups[(int(row["rate_hz"]), int(row["requested"]), int(row["actual"]))].append(row)

    summary: list[dict[str, float | int]] = []
    for (rate, requested, actual), group in sorted(groups.items()):
        n = len(group)
        summary.append(
            {
                "rate_hz": rate,
                "rcvbuf_requested": requested,
                "rcvbuf_actual": actual,
                "trials": n,
                "samples_avg": sum(float(g["sample_count"]) for g in group) / n,
                "missing_avg": sum(float(g["missing_delta_total"]) for g in group) / n,
                "mean_latency_ms_avg": sum(float(g["mean_latency_ms"]) for g in group) / n,
                "p99_latency_ms_avg": sum(float(g["p99_latency_ms"]) for g in group) / n,
                "max_latency_ms_avg": sum(float(g["max_latency_ms"]) for g in group) / n,
            }
        )
    return summary


def write_summary(path: Path, rows: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def draw_heatmap(
    rows: list[dict[str, float | int]],
    metric: str,
    title: str,
    output: Path,
    cmap: str,
) -> None:
    rates = sorted({int(row["rate_hz"]) for row in rows})
    cols = sorted(
        {(int(row["rcvbuf_requested"]), int(row["rcvbuf_actual"])) for row in rows},
        key=lambda value: (value[1], value[0]),
    )
    labels = [f"{requested}/{actual}" for requested, actual in cols]
    index = {
        (int(row["rate_hz"]), int(row["rcvbuf_requested"]), int(row["rcvbuf_actual"])): row
        for row in rows
    }

    matrix: list[list[float]] = []
    for rate in rates:
        line: list[float] = []
        for requested, actual in cols:
            row = index.get((rate, requested, actual))
            line.append(float("nan") if row is None else float(row[metric]))
        matrix.append(line)

    fig_w = max(12, len(cols) * 0.95)
    fig_h = max(4, len(rates) * 0.75)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("SO_RCVBUF requested/actual bytes")
    ax.set_ylabel("rate_hz")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks(range(len(rates)))
    ax.set_yticklabels([str(rate) for rate in rates])
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


def main() -> None:
    args = parse_args()
    inputs = args.inputs if args.inputs else DEFAULT_INPUTS
    rows = aggregate(load_rows(inputs))
    write_summary(args.summary_csv, rows)
    draw_heatmap(
        rows,
        "missing_avg",
        "W08 #131 socket buffer heatmap: missing avg",
        args.output_dir / "w08_socket_buffer_heatmap_missing_avg.png",
        "YlOrRd",
    )
    draw_heatmap(
        rows,
        "p99_latency_ms_avg",
        "W08 #131 socket buffer heatmap: p99 latency ms",
        args.output_dir / "w08_socket_buffer_heatmap_p99_latency_ms.png",
        "YlGnBu",
    )
    draw_heatmap(
        rows,
        "mean_latency_ms_avg",
        "W08 #131 socket buffer heatmap: mean latency ms",
        args.output_dir / "w08_socket_buffer_heatmap_mean_latency_ms.png",
        "YlGnBu",
    )
    print(f"wrote {args.summary_csv}")
    print(f"wrote {args.output_dir}")


if __name__ == "__main__":
    main()
