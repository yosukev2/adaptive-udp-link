#!/usr/bin/env python3
"""Analyze W08 CPU affinity matrix results.

Input files are produced by scripts/w08/run_cpu_affinity_matrix.sh:
  rate_<hz>_rxpin_<off|on>_txpin_<off|on>_run<trial>.csv

This analyzer focuses on:
- overall missing / latency aggregates
- first/last edge latency, especially last frames observed in #130
- heatmaps requested for Issue #132
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
from typing import Iterable

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
    r"rate_(?P<rate>\d+)_rxpin_(?P<rxpin>off|on)_txpin_(?P<txpin>off|on)_run(?P<trial>\d+)\.csv$"
)


@dataclass(frozen=True)
class Metadata:
    rate_hz: int
    rx_pin: str
    tx_pin: str
    trial: int
    rx_core: str | None
    tx_core: str | None
    rx_effective_core: str | None
    tx_effective_core: str | None
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None


@dataclass(frozen=True)
class RunSummary:
    rate_hz: int
    rx_pin: str
    tx_pin: str
    trial: int
    rx_core: str | None
    tx_core: str | None
    rx_effective_core: str | None
    tx_effective_core: str | None
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
    first_edge_count: int
    first_edge_mean_latency_ms: float
    first_edge_max_latency_ms: float
    last_edge_count: int
    last_edge_mean_latency_ms: float
    last_edge_max_latency_ms: float
    middle_mean_latency_ms: float
    first_edge_minus_middle_mean_ms: float
    last_edge_minus_middle_mean_ms: float
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None
    source_csv: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze W08 CPU affinity matrix results.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/w08/cpu_affinity_matrix"),
        help="Directory containing run_metadata.md and rate_*_rxpin_*_txpin_*_run*.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("reports/w08_cpu_affinity_matrix_run_summary.csv"),
    )
    parser.add_argument(
        "--aggregate-csv",
        type=Path,
        default=Path("reports/w08_cpu_affinity_matrix_aggregate.csv"),
    )
    parser.add_argument(
        "--edge-csv",
        type=Path,
        default=Path("reports/w08_cpu_affinity_matrix_edge_summary.csv"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/w08_cpu_affinity_matrix_summary.md"),
    )
    parser.add_argument("--fig-dir", type=Path, default=Path("reports/figures"))
    parser.add_argument(
        "--edge-count",
        type=int,
        default=3,
        help="Number of rows at the beginning/end used for first/last edge latency summaries.",
    )
    return parser.parse_args()


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_metadata(path: Path) -> dict[tuple[int, str, str, int], Metadata]:
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

    result: dict[tuple[int, str, str, int], Metadata] = {}
    for block in blocks:
        rate_hz = parse_int(block.get("rate_hz"))
        rx_pin = block.get("rx_pin")
        tx_pin = block.get("tx_pin")
        trial = parse_int(block.get("trial"))
        if rate_hz is None or rx_pin not in {"off", "on"} or tx_pin not in {"off", "on"} or trial is None:
            continue
        result[(rate_hz, rx_pin, tx_pin, trial)] = Metadata(
            rate_hz=rate_hz,
            rx_pin=rx_pin,
            tx_pin=tx_pin,
            trial=trial,
            rx_core=block.get("rx_core"),
            tx_core=block.get("tx_core"),
            rx_effective_core=block.get("rx_effective_core"),
            tx_effective_core=block.get("tx_effective_core"),
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


def mean(values: Iterable[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    return statistics.fmean(vals) if vals else math.nan


def analyze_csv(path: Path, metadata: Metadata | None, edge_count: int) -> RunSummary:
    match = FILENAME_RE.search(path.name)
    if not match:
        raise ValueError(f"unexpected file name: {path}")

    rate_hz = int(match.group("rate"))
    rx_pin = match.group("rxpin")
    tx_pin = match.group("txpin")
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
    n = max(edge_count, 0)
    first = latencies_ms[:n] if n else []
    last = latencies_ms[-n:] if n else []
    middle = latencies_ms[n:-n] if n and len(latencies_ms) > (2 * n) else latencies_ms[:]
    middle_mean = mean(middle)
    first_mean = mean(first)
    last_mean = mean(last)

    return RunSummary(
        rate_hz=rate_hz,
        rx_pin=rx_pin,
        tx_pin=tx_pin,
        trial=trial,
        rx_core=metadata.rx_core if metadata else None,
        tx_core=metadata.tx_core if metadata else None,
        rx_effective_core=metadata.rx_effective_core if metadata else None,
        tx_effective_core=metadata.tx_effective_core if metadata else None,
        sample_count=sample_count,
        ok_count=ok_count,
        parse_error_count=parse_error_count,
        missing_delta_total=missing_delta_total,
        missing_rate=(missing_delta_total / sample_count) if sample_count else math.nan,
        mean_latency_ms=mean(latencies_ms),
        p50_latency_ms=percentile(sorted_latencies, 0.50),
        p95_latency_ms=percentile(sorted_latencies, 0.95),
        p99_latency_ms=percentile(sorted_latencies, 0.99),
        max_latency_ms=max(latencies_ms) if latencies_ms else math.nan,
        first_edge_count=len(first),
        first_edge_mean_latency_ms=first_mean,
        first_edge_max_latency_ms=max(first) if first else math.nan,
        last_edge_count=len(last),
        last_edge_mean_latency_ms=last_mean,
        last_edge_max_latency_ms=max(last) if last else math.nan,
        middle_mean_latency_ms=middle_mean,
        first_edge_minus_middle_mean_ms=first_mean - middle_mean if not math.isnan(first_mean) and not math.isnan(middle_mean) else math.nan,
        last_edge_minus_middle_mean_ms=last_mean - middle_mean if not math.isnan(last_mean) and not math.isnan(middle_mean) else math.nan,
        tx_status=metadata.tx_status if metadata else None,
        rx_status=metadata.rx_status if metadata else None,
        copy_status=metadata.copy_status if metadata else None,
        run_validity=metadata.run_validity if metadata else None,
        source_csv=str(path),
    )


def load_runs(data_dir: Path, edge_count: int) -> list[RunSummary]:
    metadata = parse_metadata(data_dir / "run_metadata.md")
    paths = sorted(data_dir.glob("rate_*_rxpin_*_txpin_*_run*.csv"))
    if not paths:
        raise FileNotFoundError(f"no input CSV files found under {data_dir}")
    runs: list[RunSummary] = []
    for i, path in enumerate(paths, start=1):
        match = FILENAME_RE.search(path.name)
        if not match:
            continue
        key = (int(match.group("rate")), match.group("rxpin"), match.group("txpin"), int(match.group("trial")))
        runs.append(analyze_csv(path, metadata.get(key), edge_count))
        if i % 10 == 0:
            print(f"analyzed {i}/{len(paths)} files", file=sys.stderr)
    return runs


def run_to_dict(run: RunSummary) -> dict[str, object]:
    return {
        "rate_hz": run.rate_hz,
        "rx_pin": run.rx_pin,
        "tx_pin": run.tx_pin,
        "trial": run.trial,
        "rx_core": run.rx_core,
        "tx_core": run.tx_core,
        "rx_effective_core": run.rx_effective_core,
        "tx_effective_core": run.tx_effective_core,
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
        "first_edge_count": run.first_edge_count,
        "first_edge_mean_latency_ms": run.first_edge_mean_latency_ms,
        "first_edge_max_latency_ms": run.first_edge_max_latency_ms,
        "last_edge_count": run.last_edge_count,
        "last_edge_mean_latency_ms": run.last_edge_mean_latency_ms,
        "last_edge_max_latency_ms": run.last_edge_max_latency_ms,
        "middle_mean_latency_ms": run.middle_mean_latency_ms,
        "first_edge_minus_middle_mean_ms": run.first_edge_minus_middle_mean_ms,
        "last_edge_minus_middle_mean_ms": run.last_edge_minus_middle_mean_ms,
        "tx_status": run.tx_status,
        "rx_status": run.rx_status,
        "copy_status": run.copy_status,
        "run_validity": run.run_validity,
        "source_csv": run.source_csv,
    }


def aggregate(runs: list[RunSummary], keys: tuple[str, ...]) -> list[dict[str, object]]:
    groups: dict[tuple[object, ...], list[RunSummary]] = defaultdict(list)
    for run in runs:
        groups[tuple(getattr(run, key) for key in keys)].append(run)

    rows: list[dict[str, object]] = []
    for key_values, group in sorted(groups.items()):
        row: dict[str, object] = {key: value for key, value in zip(keys, key_values)}
        row.update(
            {
                "runs": len(group),
                "sample_count_avg": mean([float(g.sample_count) for g in group]),
                "missing_delta_total_avg": mean([float(g.missing_delta_total) for g in group]),
                "missing_delta_total_max": max(g.missing_delta_total for g in group),
                "missing_rate_avg": mean([g.missing_rate for g in group]),
                "mean_latency_ms_avg": mean([g.mean_latency_ms for g in group]),
                "p50_latency_ms_avg": mean([g.p50_latency_ms for g in group]),
                "p95_latency_ms_avg": mean([g.p95_latency_ms for g in group]),
                "p99_latency_ms_avg": mean([g.p99_latency_ms for g in group]),
                "max_latency_ms_avg": mean([g.max_latency_ms for g in group]),
                "max_latency_ms_max": max(g.max_latency_ms for g in group),
                "first_edge_mean_latency_ms_avg": mean([g.first_edge_mean_latency_ms for g in group]),
                "first_edge_max_latency_ms_avg": mean([g.first_edge_max_latency_ms for g in group]),
                "last_edge_mean_latency_ms_avg": mean([g.last_edge_mean_latency_ms for g in group]),
                "last_edge_max_latency_ms_avg": mean([g.last_edge_max_latency_ms for g in group]),
                "middle_mean_latency_ms_avg": mean([g.middle_mean_latency_ms for g in group]),
                "first_edge_minus_middle_mean_ms_avg": mean([g.first_edge_minus_middle_mean_ms for g in group]),
                "last_edge_minus_middle_mean_ms_avg": mean([g.last_edge_minus_middle_mean_ms for g in group]),
                "parse_error_count_total": sum(g.parse_error_count for g in group),
                "invalid_runs": sum(1 for g in group if g.run_validity != "ok"),
            }
        )
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sort_pin(value: object) -> int:
    return 0 if value == "off" else 1


def make_matrix(rows: list[dict[str, object]], y_key: str, x_key: str, metric: str) -> tuple[list[object], list[object], list[list[float]]]:
    ys = sorted({row[y_key] for row in rows}, key=lambda v: int(v) if isinstance(v, int) else sort_pin(v))
    xs = sorted({row[x_key] for row in rows}, key=lambda v: int(v) if isinstance(v, int) else sort_pin(v))
    if y_key == "rate_hz":
        ys = sorted(ys, reverse=True)
    lookup = {(row[y_key], row[x_key]): float(row[metric]) for row in rows}
    matrix = [[lookup.get((y, x), math.nan) for x in xs] for y in ys]
    return ys, xs, matrix


def annotate(ax: plt.Axes, matrix: list[list[float]], fmt: str) -> None:
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if math.isnan(value):
                text = ""
            elif fmt == "int":
                text = f"{value:.0f}"
            else:
                text = f"{value:.4f}"
            ax.text(x, y, text, ha="center", va="center", fontsize=8, color="black")


def heatmap(
    rows: list[dict[str, object]],
    *,
    y_key: str,
    x_key: str,
    metric: str,
    title: str,
    output: Path,
    cbar_label: str,
    fmt: str = "float",
) -> None:
    if not rows:
        return
    ys, xs, matrix = make_matrix(rows, y_key, x_key, metric)
    width = max(6.5, 1.4 * len(xs) + 3.0)
    height = max(4.5, 0.65 * len(ys) + 2.2)
    fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_title(title)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    ax.set_xticks(range(len(xs)), [str(x) for x in xs])
    ax.set_yticks(range(len(ys)), [str(y) for y in ys])
    annotate(ax, matrix, fmt)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(cbar_label)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def selected_rates(rows: list[dict[str, object]]) -> list[int]:
    rates = sorted({int(row["rate_hz"]) for row in rows})
    if not rates:
        return []
    return sorted({rates[0], rates[len(rates) // 2], rates[-1]})


def generate_heatmaps(rows: list[dict[str, object]], fig_dir: Path) -> list[Path]:
    outputs: list[Path] = []
    metrics = [
        ("missing_delta_total_avg", "missing_delta_total avg", "int"),
        ("p99_latency_ms_avg", "p99 latency avg [ms]", "float"),
        ("max_latency_ms_avg", "max latency avg [ms]", "float"),
        ("last_edge_mean_latency_ms_avg", "last edge mean latency avg [ms]", "float"),
        ("last_edge_minus_middle_mean_ms_avg", "last edge - middle mean [ms]", "float"),
    ]

    tx_off = [row for row in rows if row["tx_pin"] == "off"]
    for metric, label, fmt in metrics:
        output = fig_dir / f"w08_cpu_affinity_tx_off_rxpin_x_rate_{metric}.png"
        heatmap(
            tx_off,
            y_key="rate_hz",
            x_key="rx_pin",
            metric=metric,
            title=f"TX unpinned: RX pin x rate_hz ({label})",
            output=output,
            cbar_label=label,
            fmt=fmt,
        )
        outputs.append(output)

    rx_off = [row for row in rows if row["rx_pin"] == "off"]
    for metric, label, fmt in metrics:
        output = fig_dir / f"w08_cpu_affinity_rx_off_txpin_x_rate_{metric}.png"
        heatmap(
            rx_off,
            y_key="rate_hz",
            x_key="tx_pin",
            metric=metric,
            title=f"RX unpinned: TX pin x rate_hz ({label})",
            output=output,
            cbar_label=label,
            fmt=fmt,
        )
        outputs.append(output)

    for rate in selected_rates(rows):
        rate_rows = [row for row in rows if int(row["rate_hz"]) == rate]
        for metric, label, fmt in metrics:
            output = fig_dir / f"w08_cpu_affinity_rate_{rate}_rxpin_x_txpin_{metric}.png"
            heatmap(
                rate_rows,
                y_key="tx_pin",
                x_key="rx_pin",
                metric=metric,
                title=f"rate_hz={rate}: RX pin x TX pin ({label})",
                output=output,
                cbar_label=label,
                fmt=fmt,
            )
            outputs.append(output)
    return outputs


def md_table(rows: list[dict[str, object]], columns: list[tuple[str, str]], limit: int | None = None) -> str:
    selected = rows if limit is None else rows[:limit]
    lines = ["| " + " | ".join(title for _, title in columns) + " |"]
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in selected:
        values: list[str] = []
        for key, _ in columns:
            value = row.get(key, "")
            if isinstance(value, float):
                if math.isnan(value):
                    values.append("")
                elif "missing_delta" in key or key in {"runs", "invalid_runs"}:
                    values.append(f"{value:.0f}")
                else:
                    values.append(f"{value:.6f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_report(path: Path, rows: list[dict[str, object]], figures: list[Path], edge_count: int) -> None:
    missing_top = sorted(rows, key=lambda r: float(r["missing_delta_total_avg"]), reverse=True)[:10]
    p99_top = sorted(rows, key=lambda r: float(r["p99_latency_ms_avg"]), reverse=True)[:10]
    last_edge_top = sorted(rows, key=lambda r: float(r["last_edge_minus_middle_mean_ms_avg"]), reverse=True)[:10]
    first_edge_low_rate_rows = sorted(
        [row for row in rows if int(row["rate_hz"]) in (5000, 10000)],
        key=lambda r: (int(r["rate_hz"]), str(r["rx_pin"]), str(r["tx_pin"])),
    )

    md: list[str] = []
    md.append("# W08 #132 CPU affinity matrix summary")
    md.append("")
    md.append("## 目的")
    md.append("")
    md.append("- RX/TX の CPU affinity 有無と `rate_hz` の組み合わせで missing / latency がどう変わるかを見る。")
    md.append(f"- #130 で見えた先頭・末尾の latency 跳ねを確認するため、各runの先頭{edge_count}行・末尾{edge_count}行を別集計する。")
    md.append("")
    md.append("## 実験条件")
    md.append("")
    md.append("- rx_pin: `off / on`")
    md.append("- tx_pin: `off / on`")
    md.append("- rate_hz: `5000 / 10000 / 50000 / 100000 / 500000`")
    md.append("- trials: `1 / 2 / 3`")
    md.append("- default pin core: RX core 0, TX core 1")
    md.append("- socket buffer tuning: none")
    md.append("")
    md.append("## 結論・観察")
    md.append("")
    if missing_top:
        row = missing_top[0]
        md.append(
            "- missing 最大は "
            f"`rate_hz={row['rate_hz']}, rx_pin={row['rx_pin']}, tx_pin={row['tx_pin']}` の "
            f"`missing_avg={float(row['missing_delta_total_avg']):.0f}`。"
        )
    if last_edge_top:
        row = last_edge_top[0]
        md.append(
            "- 末尾 edge latency の平均との差が最大なのは "
            f"`rate_hz={row['rate_hz']}, rx_pin={row['rx_pin']}, tx_pin={row['tx_pin']}` で、"
            f"末尾平均 `{float(row['last_edge_mean_latency_ms_avg']):.6f} ms`、中央平均 "
            f"`{float(row['middle_mean_latency_ms_avg']):.6f} ms`、差分 "
            f"`{float(row['last_edge_minus_middle_mean_ms_avg']):.6f} ms`。"
        )
    if first_edge_low_rate_rows:
        row = max(first_edge_low_rate_rows, key=lambda r: float(r["first_edge_minus_middle_mean_ms_avg"]))
        md.append(
            "- rate_hz 5,000/10,000 に限定した先頭 edge latency の平均との差が最大なのは "
            f"`rate_hz={row['rate_hz']}, rx_pin={row['rx_pin']}, tx_pin={row['tx_pin']}` で、"
            f"先頭平均 `{float(row['first_edge_mean_latency_ms_avg']):.6f} ms`、中央平均 "
            f"`{float(row['middle_mean_latency_ms_avg']):.6f} ms`、差分 "
            f"`{float(row['first_edge_minus_middle_mean_ms_avg']):.6f} ms`。"
        )
    md.append("- 500,000 Hz では全pin条件で missing が大きく、CPU affinity の有無だけでは飽和を吸収できていない。")
    md.append("- 5,000〜50,000 Hz では missing は基本的に 0 だが、末尾 edge latency は条件によって中央部より大きく跳ねる。#130で見えた末尾だけ遅い現象は、このmatrixでも再現している。")
    md.append("- RX/TX の pinning は一部条件で改善するが、全指標で単調に良くなるわけではない。missing、p99、末尾edgeは分けて判断する。")
    md.append("")
    md.append("## 集計値の意味")
    md.append("")
    md.append("- `first_edge_*`: CSV先頭側の latency。")
    md.append("- `last_edge_*`: CSV末尾側の latency。")
    md.append("- `*_minus_middle_mean_ms`: 先頭/末尾 edge の平均 latency から、edgeを除いた中央部分の平均 latency を引いた値。正なら edge が中央より遅い。")
    md.append("")
    md.append("## missing 上位")
    md.append("")
    md.append(md_table(missing_top, [
        ("rate_hz", "rate_hz"),
        ("rx_pin", "rx_pin"),
        ("tx_pin", "tx_pin"),
        ("runs", "runs"),
        ("missing_delta_total_avg", "missing_avg"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("max_latency_ms_avg", "max_ms_avg"),
    ]))
    md.append("")
    md.append("## p99 latency 上位")
    md.append("")
    md.append(md_table(p99_top, [
        ("rate_hz", "rate_hz"),
        ("rx_pin", "rx_pin"),
        ("tx_pin", "tx_pin"),
        ("runs", "runs"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("missing_delta_total_avg", "missing_avg"),
        ("max_latency_ms_avg", "max_ms_avg"),
    ]))
    md.append("")
    md.append("## 末尾 edge latency 上位")
    md.append("")
    md.append(md_table(last_edge_top, [
        ("rate_hz", "rate_hz"),
        ("rx_pin", "rx_pin"),
        ("tx_pin", "tx_pin"),
        ("last_edge_mean_latency_ms_avg", "last_mean_ms"),
        ("middle_mean_latency_ms_avg", "middle_mean_ms"),
        ("last_edge_minus_middle_mean_ms_avg", "last_minus_middle_ms"),
        ("missing_delta_total_avg", "missing_avg"),
    ]))
    md.append("")
    md.append("## 先頭 edge latency: rate_hz 5,000/10,000")
    md.append("")
    md.append("rate_hz 5,000/10,000 に限定し、`rate_hz -> rx_pin -> tx_pin` の順で並べる。")
    md.append("")
    md.append(md_table(first_edge_low_rate_rows, [
        ("rate_hz", "rate_hz"),
        ("rx_pin", "rx_pin"),
        ("tx_pin", "tx_pin"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("first_edge_mean_latency_ms_avg", "first_mean_ms"),
        ("middle_mean_latency_ms_avg", "middle_mean_ms"),
        ("first_edge_minus_middle_mean_ms_avg", "first_minus_middle_ms"),
        ("missing_delta_total_avg", "missing_avg"),
    ]))
    md.append("")
    md.append("## Heatmaps")
    md.append("")
    md.append("### TX非固定: RX固定/非固定 x rate_hz")
    md.append("")
    for fig in figures:
        name = fig.name
        if "tx_off_rxpin_x_rate" in name:
            rel = fig.as_posix()
            if rel.startswith("reports/"):
                rel = rel[len("reports/"):]
            md.append(f"![{fig.stem}]({rel})")
            md.append("")
    md.append("### RX非固定: TX固定/非固定 x rate_hz")
    md.append("")
    for fig in figures:
        name = fig.name
        if "rx_off_txpin_x_rate" in name:
            rel = fig.as_posix()
            if rel.startswith("reports/"):
                rel = rel[len("reports/"):]
            md.append(f"![{fig.stem}]({rel})")
            md.append("")
    md.append("### rate_hz 最小・中間・最大: RX/TX 2軸")
    md.append("")
    for fig in figures:
        name = fig.name
        if "rxpin_x_txpin" in name:
            rel = fig.as_posix()
            if rel.startswith("reports/"):
                rel = rel[len("reports/"):]
            md.append(f"![{fig.stem}]({rel})")
            md.append("")
    md.append("## 成果物")
    md.append("")
    md.append("- run summary: `reports/w08_cpu_affinity_matrix_run_summary.csv`")
    md.append("- aggregate summary: `reports/w08_cpu_affinity_matrix_aggregate.csv`")
    md.append("- edge summary: `reports/w08_cpu_affinity_matrix_edge_summary.csv`")
    md.append("- report: `reports/w08_cpu_affinity_matrix_summary.md`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    args = parse_args()
    runs = load_runs(args.data_dir, args.edge_count)
    run_rows = [run_to_dict(run) for run in runs]
    aggregate_rows = aggregate(runs, ("rate_hz", "rx_pin", "tx_pin"))
    edge_rows = [
        {
            "rate_hz": row["rate_hz"],
            "rx_pin": row["rx_pin"],
            "tx_pin": row["tx_pin"],
            "runs": row["runs"],
            "first_edge_mean_latency_ms_avg": row["first_edge_mean_latency_ms_avg"],
            "middle_mean_latency_ms_avg": row["middle_mean_latency_ms_avg"],
            "last_edge_mean_latency_ms_avg": row["last_edge_mean_latency_ms_avg"],
            "first_edge_minus_middle_mean_ms_avg": row["first_edge_minus_middle_mean_ms_avg"],
            "last_edge_minus_middle_mean_ms_avg": row["last_edge_minus_middle_mean_ms_avg"],
            "first_edge_max_latency_ms_avg": row["first_edge_max_latency_ms_avg"],
            "last_edge_max_latency_ms_avg": row["last_edge_max_latency_ms_avg"],
            "missing_delta_total_avg": row["missing_delta_total_avg"],
        }
        for row in aggregate_rows
    ]
    write_csv(args.summary_csv, run_rows)
    write_csv(args.aggregate_csv, aggregate_rows)
    write_csv(args.edge_csv, edge_rows)
    figures = generate_heatmaps(aggregate_rows, args.fig_dir)
    write_report(args.report, aggregate_rows, figures, args.edge_count)

    print(f"runs={len(runs)}")
    print(f"aggregate_rows={len(aggregate_rows)}")
    print(f"edge_count={args.edge_count}")
    print(f"figures={len(figures)}")
    print(f"report={args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
