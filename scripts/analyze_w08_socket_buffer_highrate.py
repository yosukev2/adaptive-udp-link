#!/usr/bin/env python3
"""Analyze W08 high-rate socket buffer matrix results.

Inputs are copied from Raspberry Pi 5, typically:
  C:/tmp/adaptive-udp-link-issue-131-highrate/data/socket_buffer_txrx_highrate

This script supports both file families produced by run_socket_buffer_txrx_highrate_matrix.sh:
- rate_<hz>_rcvbuf_<bytes>_sndbuf_<bytes>_run<trial>.csv
- rate_<hz>_rcvbuf_<bytes>_sndbuf_default_run<trial>.csv

Outputs:
- per-run summary CSV
- aggregate summary CSVs
- heatmaps
- Markdown report
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
    r"rate_(?P<rate>\d+)_rcvbuf_(?P<rcvbuf>\d+)_sndbuf_(?P<sndbuf>\d+|default)_run(?P<trial>\d+)\.csv$"
)


@dataclass(frozen=True)
class Metadata:
    rate_hz: int
    rcvbuf_requested: int
    sndbuf_requested: str
    trial: int
    rcvbuf_actual: int | None
    sndbuf_actual: str | None
    tx_status: int | None
    rx_status: int | None
    copy_status: int | None
    run_validity: str | None


@dataclass(frozen=True)
class RunSummary:
    rate_hz: int
    rcvbuf_requested: int
    rcvbuf_actual: int | None
    sndbuf_requested: str
    sndbuf_actual: str | None
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
    parser = argparse.ArgumentParser(description="Analyze W08 high-rate socket buffer matrix.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(r"C:/tmp/adaptive-udp-link-issue-131-highrate/data/socket_buffer_txrx_highrate"),
    )
    parser.add_argument("--summary-csv", type=Path, default=Path("reports/w08_socket_buffer_highrate_run_summary.csv"))
    parser.add_argument(
        "--default-aggregate-csv",
        type=Path,
        default=Path("reports/w08_socket_buffer_highrate_default_sndbuf_aggregate.csv"),
    )
    parser.add_argument(
        "--txrx-aggregate-csv",
        type=Path,
        default=Path("reports/w08_socket_buffer_highrate_txrx_aggregate.csv"),
    )
    parser.add_argument("--report", type=Path, default=Path("reports/w08_socket_buffer_highrate_summary.md"))
    parser.add_argument("--fig-dir", type=Path, default=Path("reports/figures"))
    return parser.parse_args()


def parse_int(value: str | None) -> int | None:
    if value is None or value == "" or value == "default":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_metadata(path: Path) -> dict[tuple[int, int, str, int], Metadata]:
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

    result: dict[tuple[int, int, str, int], Metadata] = {}
    for block in blocks:
        rate_hz = parse_int(block.get("rate_hz"))
        rcvbuf_requested = parse_int(block.get("rcvbuf_requested"))
        sndbuf_requested = block.get("sndbuf_requested")
        trial = parse_int(block.get("trial"))
        if rate_hz is None or rcvbuf_requested is None or not sndbuf_requested or trial is None:
            continue
        result[(rate_hz, rcvbuf_requested, sndbuf_requested, trial)] = Metadata(
            rate_hz=rate_hz,
            rcvbuf_requested=rcvbuf_requested,
            sndbuf_requested=sndbuf_requested,
            trial=trial,
            rcvbuf_actual=parse_int(block.get("rcvbuf_actual")),
            sndbuf_actual=block.get("sndbuf_actual"),
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
    sndbuf_requested = match.group("sndbuf")
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
        source_csv=str(path),
    )


def load_runs(data_dir: Path) -> list[RunSummary]:
    metadata = parse_metadata(data_dir / "run_metadata.md")
    paths = sorted(data_dir.glob("rate_*_rcvbuf_*_sndbuf_*_run*.csv"))
    if not paths:
        raise FileNotFoundError(f"no input CSV files found under {data_dir}")

    runs: list[RunSummary] = []
    for index, path in enumerate(paths, start=1):
        match = FILENAME_RE.search(path.name)
        if not match:
            continue
        key = (
            int(match.group("rate")),
            int(match.group("rcvbuf")),
            match.group("sndbuf"),
            int(match.group("trial")),
        )
        runs.append(analyze_csv(path, metadata.get(key)))
        if index % 10 == 0:
            print(f"analyzed {index}/{len(paths)} files", file=sys.stderr)
    return runs


def fmean(values: Iterable[float]) -> float:
    vals = [v for v in values if not math.isnan(v)]
    return statistics.fmean(vals) if vals else math.nan


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
                "sample_count_avg": fmean(r.sample_count for r in group),
                "missing_delta_total_avg": fmean(r.missing_delta_total for r in group),
                "missing_delta_total_max": max(r.missing_delta_total for r in group),
                "missing_rate_avg": fmean(r.missing_rate for r in group),
                "mean_latency_ms_avg": fmean(r.mean_latency_ms for r in group),
                "p50_latency_ms_avg": fmean(r.p50_latency_ms for r in group),
                "p95_latency_ms_avg": fmean(r.p95_latency_ms for r in group),
                "p99_latency_ms_avg": fmean(r.p99_latency_ms for r in group),
                "max_latency_ms_avg": fmean(r.max_latency_ms for r in group),
                "max_latency_ms_max": max(r.max_latency_ms for r in group),
                "parse_error_count_total": sum(r.parse_error_count for r in group),
                "invalid_runs": sum(1 for r in group if r.run_validity != "ok"),
            }
        )
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_to_dict(run: RunSummary) -> dict[str, object]:
    return {
        "rate_hz": run.rate_hz,
        "rcvbuf_requested": run.rcvbuf_requested,
        "rcvbuf_actual": run.rcvbuf_actual,
        "sndbuf_requested": run.sndbuf_requested,
        "sndbuf_actual": run.sndbuf_actual,
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


def label_buf(requested: object, actual: object) -> str:
    if actual is None or actual == "" or actual == "default":
        return str(requested)
    return f"{requested}/{actual}"


def make_matrix(rows: list[dict[str, object]], y_key: str, x_key: str, metric: str) -> tuple[list[object], list[object], list[list[float]]]:
    ys = sorted({row[y_key] for row in rows}, key=lambda v: (isinstance(v, str), v))
    xs = sorted({row[x_key] for row in rows}, key=lambda v: (isinstance(v, str), v))
    lookup = {(row[y_key], row[x_key]): float(row[metric]) for row in rows}
    matrix = [[lookup.get((y, x), math.nan) for x in xs] for y in ys]
    return ys, xs, matrix


def annotate_heatmap(ax: plt.Axes, matrix: list[list[float]], fmt: str) -> None:
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if math.isnan(value):
                text = ""
            elif fmt == "int":
                text = f"{value:.0f}"
            elif fmt == "rate":
                text = f"{value:.3f}"
            else:
                text = f"{value:.4f}"
            ax.text(x, y, text, ha="center", va="center", fontsize=7, color="black")


def save_heatmap(
    rows: list[dict[str, object]],
    *,
    y_key: str,
    x_key: str,
    metric: str,
    y_label_map: dict[object, str],
    x_label_map: dict[object, str],
    title: str,
    output: Path,
    colorbar_label: str,
    fmt: str,
) -> None:
    if not rows:
        return
    ys, xs, matrix = make_matrix(rows, y_key, x_key, metric)
    width = max(7.0, 1.25 * len(xs) + 2.5)
    height = max(4.8, 0.7 * len(ys) + 2.0)
    fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(xs)), [x_label_map.get(x, str(x)) for x in xs], rotation=35, ha="right")
    ax.set_yticks(range(len(ys)), [y_label_map.get(y, str(y)) for y in ys])
    ax.set_title(title)
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    annotate_heatmap(ax, matrix, fmt)
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(colorbar_label)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)


def generate_heatmaps(default_rows: list[dict[str, object]], txrx_rows: list[dict[str, object]], fig_dir: Path) -> list[Path]:
    outputs: list[Path] = []

    # Default-send-buffer: y=rate_hz, x=rx buffer.
    rx_label_map = {
        row["rcvbuf_requested"]: label_buf(row["rcvbuf_requested"], row.get("rcvbuf_actual"))
        for row in default_rows
    }
    rate_label_map = {row["rate_hz"]: str(row["rate_hz"]) for row in default_rows}
    for metric, label, fmt in [
        ("missing_delta_total_avg", "missing_delta_total average", "int"),
        ("p99_latency_ms_avg", "p99 latency average [ms]", "float"),
        ("max_latency_ms_avg", "max latency average [ms]", "float"),
    ]:
        output = fig_dir / f"w08_socket_buffer_highrate_default_sndbuf_rxbuf_x_rate_{metric}.png"
        save_heatmap(
            default_rows,
            y_key="rate_hz",
            x_key="rcvbuf_requested",
            metric=metric,
            y_label_map=rate_label_map,
            x_label_map=rx_label_map,
            title=f"default SO_SNDBUF: RX buffer x rate_hz ({label})",
            output=output,
            colorbar_label=label,
            fmt=fmt,
        )
        outputs.append(output)

    # Explicit TX/RX buffer matrix: y=tx buffer, x=rx buffer, one set per rate.
    for rate in sorted({row["rate_hz"] for row in txrx_rows}):
        rows = [row for row in txrx_rows if row["rate_hz"] == rate]
        rx_label_map = {
            row["rcvbuf_requested"]: label_buf(row["rcvbuf_requested"], row.get("rcvbuf_actual"))
            for row in rows
        }
        tx_label_map = {
            row["sndbuf_requested"]: label_buf(row["sndbuf_requested"], row.get("sndbuf_actual"))
            for row in rows
        }
        for metric, label, fmt in [
            ("missing_delta_total_avg", "missing_delta_total average", "int"),
            ("p99_latency_ms_avg", "p99 latency average [ms]", "float"),
            ("max_latency_ms_avg", "max latency average [ms]", "float"),
        ]:
            output = fig_dir / f"w08_socket_buffer_highrate_txrx_rate_{rate}_{metric}.png"
            save_heatmap(
                rows,
                y_key="sndbuf_requested",
                x_key="rcvbuf_requested",
                metric=metric,
                y_label_map=tx_label_map,
                x_label_map=rx_label_map,
                title=f"rate_hz={rate}: RX buffer x TX buffer ({label})",
                output=output,
                colorbar_label=label,
                fmt=fmt,
            )
            outputs.append(output)
    return outputs


def md_table(rows: list[dict[str, object]], columns: list[tuple[str, str]], limit: int | None = None) -> str:
    selected = rows if limit is None else rows[:limit]
    lines = []
    lines.append("| " + " | ".join(title for _, title in columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for row in selected:
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


def write_report(
    path: Path,
    runs: list[RunSummary],
    default_rows: list[dict[str, object]],
    txrx_rows: list[dict[str, object]],
    figures: list[Path],
) -> None:
    valid_runs = sum(1 for r in runs if r.run_validity == "ok")
    invalid_runs = len(runs) - valid_runs
    default_run_count = sum(1 for r in runs if r.sndbuf_requested == "default")
    txrx_run_count = len(runs) - default_run_count

    top_default_missing = sorted(default_rows, key=lambda r: float(r["missing_delta_total_avg"]), reverse=True)[:10]
    top_txrx_missing = sorted(txrx_rows, key=lambda r: float(r["missing_delta_total_avg"]), reverse=True)[:10]
    top_default_latency = sorted(default_rows, key=lambda r: float(r["p99_latency_ms_avg"]), reverse=True)[:10]
    top_txrx_latency = sorted(txrx_rows, key=lambda r: float(r["p99_latency_ms_avg"]), reverse=True)[:10]

    md = []
    md.append("# W08 #131 highrate socket buffer summary")
    md.append("")
    md.append("## 目的")
    md.append("")
    md.append("- 以前の socket buffer matrix は `rate_hz` が1桁低かったため、highrate 条件で再評価する。")
    md.append("- 送信側 default のまま `SO_RCVBUF × rate_hz` を見る。")
    md.append("- 送信側 `SO_SNDBUF` も明示した条件で `SO_RCVBUF × SO_SNDBUF` を見る。")
    md.append("")
    md.append("## 実験データ")
    md.append("")
    md.append(f"- total runs: {len(runs)}")
    md.append(f"- run_validity=ok: {valid_runs}")
    md.append(f"- invalid runs: {invalid_runs}")
    md.append(f"- default SO_SNDBUF runs: {default_run_count}")
    md.append(f"- explicit SO_SNDBUF runs: {txrx_run_count}")
    md.append("- fixed: loopback `127.0.0.1:9000`, payload_len `48`, tx 10 sec, rx 12 sec, recovery_mode `fsm`, CPU affinity none")
    md.append("")
    md.append("## 結論・観察")
    md.append("")
    if top_default_missing:
        row = top_default_missing[0]
        md.append(
            "- 送信buffer default 条件では、missing 最大は "
            f"`rate_hz={row['rate_hz']}, rcvbuf={row['rcvbuf_requested']}/{row['rcvbuf_actual']}` の "
            f"`missing_avg={float(row['missing_delta_total_avg']):.0f}`。"
        )
    if top_default_latency:
        row = top_default_latency[0]
        md.append(
            "- 送信buffer default 条件の p99 latency 最大は "
            f"`rate_hz={row['rate_hz']}, rcvbuf={row['rcvbuf_requested']}/{row['rcvbuf_actual']}` の "
            f"`p99={float(row['p99_latency_ms_avg']):.6f} ms`。"
        )
    if top_txrx_missing:
        row = top_txrx_missing[0]
        md.append(
            "- TX/RX 明示条件では、missing 最大は "
            f"`rate_hz={row['rate_hz']}, rcvbuf={row['rcvbuf_requested']}/{row['rcvbuf_actual']}, "
            f"sndbuf={row['sndbuf_requested']}/{row['sndbuf_actual']}` の "
            f"`missing_avg={float(row['missing_delta_total_avg']):.0f}`。"
        )
    if top_txrx_latency:
        row = top_txrx_latency[0]
        md.append(
            "- TX/RX 明示条件の p99 latency 最大は "
            f"`rate_hz={row['rate_hz']}, rcvbuf={row['rcvbuf_requested']}/{row['rcvbuf_actual']}, "
            f"sndbuf={row['sndbuf_requested']}/{row['sndbuf_actual']}` の "
            f"`p99={float(row['p99_latency_ms_avg']):.6f} ms`。"
        )
    md.append("- missing と p99 latency は同じ条件で最大化していない。gap 発生量と通常受信時の tail latency は分けて見る必要がある。")
    md.append("- `SO_RCVBUF` を大きくすれば常に改善する、または小さくすれば常に悪化する、という単調な傾向はこの highrate 結果からは言えない。")
    md.append("- `rate_hz=500000` 以上では missing が大きく出る条件が増え、buffer size よりも処理飽和・スケジューリング・送受信処理の競合が支配的になっている可能性が高い。")
    md.append("")
    md.append("## 主要な見方")
    md.append("")
    md.append("- `missing_delta_total_avg` は3試行平均。値が大きいほど受信側で sequence gap が多い。")
    md.append("- `p99_latency_ms_avg` は各試行の p99 latency を平均した値。")
    md.append("- `max_latency_ms_avg` は外れ値を見るための補助指標。")
    md.append("- heatmap の buffer ラベルは `requested/actual`。`default` は送信側 buffer を明示指定していない条件。")
    md.append("")

    md.append("## 送信buffer default: missing 上位")
    md.append("")
    md.append(md_table(top_default_missing, [
        ("rate_hz", "rate_hz"),
        ("rcvbuf_requested", "rcvbuf_req"),
        ("rcvbuf_actual", "rcvbuf_actual"),
        ("runs", "runs"),
        ("missing_delta_total_avg", "missing_avg"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("max_latency_ms_avg", "max_ms_avg"),
    ]))
    md.append("")

    md.append("## 送信buffer default: p99 latency 上位")
    md.append("")
    md.append(md_table(top_default_latency, [
        ("rate_hz", "rate_hz"),
        ("rcvbuf_requested", "rcvbuf_req"),
        ("rcvbuf_actual", "rcvbuf_actual"),
        ("runs", "runs"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("missing_delta_total_avg", "missing_avg"),
        ("max_latency_ms_avg", "max_ms_avg"),
    ]))
    md.append("")

    md.append("## TX/RX明示: missing 上位")
    md.append("")
    md.append(md_table(top_txrx_missing, [
        ("rate_hz", "rate_hz"),
        ("rcvbuf_requested", "rcvbuf_req"),
        ("rcvbuf_actual", "rcvbuf_actual"),
        ("sndbuf_requested", "sndbuf_req"),
        ("sndbuf_actual", "sndbuf_actual"),
        ("runs", "runs"),
        ("missing_delta_total_avg", "missing_avg"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("max_latency_ms_avg", "max_ms_avg"),
    ]))
    md.append("")

    md.append("## TX/RX明示: p99 latency 上位")
    md.append("")
    md.append(md_table(top_txrx_latency, [
        ("rate_hz", "rate_hz"),
        ("rcvbuf_requested", "rcvbuf_req"),
        ("rcvbuf_actual", "rcvbuf_actual"),
        ("sndbuf_requested", "sndbuf_req"),
        ("sndbuf_actual", "sndbuf_actual"),
        ("runs", "runs"),
        ("p99_latency_ms_avg", "p99_ms_avg"),
        ("missing_delta_total_avg", "missing_avg"),
        ("max_latency_ms_avg", "max_ms_avg"),
    ]))
    md.append("")

    md.append("## Heatmaps")
    md.append("")
    for fig in figures:
        rel = fig.as_posix()
        if rel.startswith("reports/"):
            rel = rel[len("reports/"):]
        md.append(f"![{fig.stem}]({rel})")
        md.append("")

    md.append("## 成果物")
    md.append("")
    md.append("- run summary: `reports/w08_socket_buffer_highrate_run_summary.csv`")
    md.append("- default SO_SNDBUF aggregate: `reports/w08_socket_buffer_highrate_default_sndbuf_aggregate.csv`")
    md.append("- explicit TX/RX aggregate: `reports/w08_socket_buffer_highrate_txrx_aggregate.csv`")
    md.append("- report: `reports/w08_socket_buffer_highrate_summary.md`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    args = parse_args()
    runs = load_runs(args.data_dir)

    run_rows = [run_to_dict(run) for run in runs]
    write_csv(args.summary_csv, run_rows)

    default_runs = [run for run in runs if run.sndbuf_requested == "default"]
    txrx_runs = [run for run in runs if run.sndbuf_requested != "default"]

    default_rows = aggregate(default_runs, ("rate_hz", "rcvbuf_requested", "rcvbuf_actual", "sndbuf_requested", "sndbuf_actual"))
    txrx_rows = aggregate(
        txrx_runs,
        ("rate_hz", "rcvbuf_requested", "rcvbuf_actual", "sndbuf_requested", "sndbuf_actual"),
    )

    write_csv(args.default_aggregate_csv, default_rows)
    write_csv(args.txrx_aggregate_csv, txrx_rows)

    figures = generate_heatmaps(default_rows, txrx_rows, args.fig_dir)
    write_report(args.report, runs, default_rows, txrx_rows, figures)

    print(f"runs={len(runs)}")
    print(f"default_sndbuf_runs={len(default_runs)}")
    print(f"explicit_txrx_runs={len(txrx_runs)}")
    print(f"figures={len(figures)}")
    print(f"report={args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

