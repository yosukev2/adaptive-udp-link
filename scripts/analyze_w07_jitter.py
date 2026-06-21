#!/usr/bin/env python3
"""Validate W07 Pico CSV runs and generate jitter comparison artifacts."""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from html import escape
from pathlib import Path

SAMPLE_COUNT = 1000
PERIOD_TARGET_US = 10000
EXPECTED_RUNS = (1, 2, 3)

BAREMETAL_FIELDS = [
    "mode",
    "board",
    "sample_index",
    "period_target_us",
    "timestamp_us",
    "delta_us",
    "jitter_us",
]
FREERTOS_FIELDS = BAREMETAL_FIELDS + [
    "queue_latency_us",
    "deadline_miss_count",
]


class CSVValidationError(ValueError):
    """Raised when a W07 run does not satisfy the measurement schema."""


@dataclass(frozen=True)
class RunData:
    mode: str
    run: int
    path: Path
    abs_jitter_us: tuple[int, ...]
    queue_latency_us: tuple[int, ...]
    queue_send_fail_count: int
    queue_not_received_count: int
    deadline_miss_count: int | None


@dataclass(frozen=True)
class MetricSummary:
    scope: str
    mode: str
    run: str
    metric: str
    sample_count: int
    p50_us: float
    p95_us: float
    p99_us: float
    max_us: float
    stddev_us: float
    queue_send_fail_count: int
    queue_not_received_count: int
    deadline_miss_count: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze W07 bare-metal and FreeRTOS jitter CSV runs."
    )
    parser.add_argument(
        "--data-dir",
        default="data/w07",
        help="Directory containing baremetal_run*.csv and freertos_run*.csv.",
    )
    parser.add_argument(
        "--summary-csv",
        default="data/w07/w07_jitter_summary.csv",
        help="Generated machine-readable summary CSV.",
    )
    parser.add_argument(
        "--report",
        default="reports/w07_rtos_jitter_summary.md",
        help="Generated Markdown comparison report.",
    )
    parser.add_argument(
        "--figures-dir",
        default="reports/figures",
        help="Directory for generated SVG distribution figures.",
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


def load_run(path: Path, mode: str, run: int) -> RunData:
    expected_fields = FREERTOS_FIELDS if mode == "freertos" else BAREMETAL_FIELDS
    abs_jitter_us: list[int] = []
    queue_latency_us: list[int] = []
    queue_send_fail_count = 0
    queue_not_received_count = 0
    deadline_values: set[int] = set()
    previous_timestamp: int | None = None

    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise CSVValidationError(f"failed to open {path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        header = [field.strip() for field in reader.fieldnames or []]
        if header != expected_fields:
            raise CSVValidationError(
                f"{path}: unexpected header; expected {expected_fields}, got {header}"
            )

        row_count = 0
        for row_count, row in enumerate(reader, start=1):
            line_no = row_count + 1
            if (row.get("mode") or "").strip() != mode:
                raise CSVValidationError(
                    f"{path}:{line_no}: mode must be {mode!r}"
                )
            if (row.get("board") or "").strip() != "pico":
                raise CSVValidationError(
                    f"{path}:{line_no}: board must be 'pico'"
                )

            sample_index = parse_int(row.get("sample_index"), "sample_index", path, line_no)
            period_us = parse_int(
                row.get("period_target_us"), "period_target_us", path, line_no
            )
            timestamp_us = parse_int(row.get("timestamp_us"), "timestamp_us", path, line_no)
            delta_us = parse_int(row.get("delta_us"), "delta_us", path, line_no)
            jitter_us = parse_int(row.get("jitter_us"), "jitter_us", path, line_no)

            if sample_index != row_count:
                raise CSVValidationError(
                    f"{path}:{line_no}: sample_index {sample_index} != {row_count}"
                )
            if period_us != PERIOD_TARGET_US:
                raise CSVValidationError(
                    f"{path}:{line_no}: period_target_us {period_us} "
                    f"!= {PERIOD_TARGET_US}"
                )

            if row_count == 1:
                if delta_us != 0 or jitter_us != 0:
                    raise CSVValidationError(
                        f"{path}:{line_no}: first sample must have delta=0 and jitter=0"
                    )
            else:
                assert previous_timestamp is not None
                expected_delta = timestamp_us - previous_timestamp
                if timestamp_us <= previous_timestamp:
                    raise CSVValidationError(
                        f"{path}:{line_no}: timestamp is not strictly increasing"
                    )
                if delta_us != expected_delta:
                    raise CSVValidationError(
                        f"{path}:{line_no}: delta_us {delta_us} != {expected_delta}"
                    )
                if jitter_us != delta_us - period_us:
                    raise CSVValidationError(
                        f"{path}:{line_no}: jitter_us {jitter_us} != "
                        f"delta_us - period_target_us ({delta_us - period_us})"
                    )
                # The first row has no preceding interval, so exclude its synthetic zero.
                abs_jitter_us.append(abs(jitter_us))

            previous_timestamp = timestamp_us

            if mode == "freertos":
                queue_latency = parse_int(
                    row.get("queue_latency_us"), "queue_latency_us", path, line_no
                )
                deadline_miss = parse_int(
                    row.get("deadline_miss_count"),
                    "deadline_miss_count",
                    path,
                    line_no,
                )
                if queue_latency == -1:
                    queue_send_fail_count += 1
                elif queue_latency == -2:
                    queue_not_received_count += 1
                elif queue_latency < 0:
                    raise CSVValidationError(
                        f"{path}:{line_no}: unsupported queue latency {queue_latency}"
                    )
                else:
                    queue_latency_us.append(queue_latency)
                if deadline_miss < 0:
                    raise CSVValidationError(
                        f"{path}:{line_no}: deadline_miss_count must be non-negative"
                    )
                deadline_values.add(deadline_miss)

    if row_count != SAMPLE_COUNT:
        raise CSVValidationError(
            f"{path}: expected {SAMPLE_COUNT} data rows, got {row_count}"
        )
    if len(abs_jitter_us) != SAMPLE_COUNT - 1:
        raise CSVValidationError(
            f"{path}: expected {SAMPLE_COUNT - 1} jitter intervals, "
            f"got {len(abs_jitter_us)}"
        )

    deadline_miss_count: int | None = None
    if mode == "freertos":
        if len(deadline_values) != 1:
            raise CSVValidationError(
                f"{path}: deadline_miss_count must be constant, got {deadline_values}"
            )
        deadline_miss_count = next(iter(deadline_values))
        if not queue_latency_us:
            raise CSVValidationError(f"{path}: no valid queue latency samples")

    return RunData(
        mode=mode,
        run=run,
        path=path,
        abs_jitter_us=tuple(abs_jitter_us),
        queue_latency_us=tuple(queue_latency_us),
        queue_send_fail_count=queue_send_fail_count,
        queue_not_received_count=queue_not_received_count,
        deadline_miss_count=deadline_miss_count,
    )


def discover_runs(data_dir: Path) -> list[RunData]:
    discovered: list[RunData] = []
    pattern = re.compile(r"^(baremetal|freertos)_run([0-9]+)\.csv$")

    for path in sorted(data_dir.glob("*_run*.csv")):
        match = pattern.match(path.name)
        if match is None:
            continue
        mode = match.group(1)
        run = int(match.group(2))
        discovered.append(load_run(path, mode, run))

    for mode in ("baremetal", "freertos"):
        runs = tuple(item.run for item in discovered if item.mode == mode)
        if runs != EXPECTED_RUNS:
            raise CSVValidationError(
                f"{data_dir}: expected {mode} runs {EXPECTED_RUNS}, got {runs}"
            )

    return discovered


def summarize_values(
    *,
    scope: str,
    mode: str,
    run: str,
    metric: str,
    values: list[int],
    queue_send_fail_count: int = 0,
    queue_not_received_count: int = 0,
    deadline_miss_count: int | None = None,
) -> MetricSummary:
    sorted_values = sorted(values)
    if not sorted_values:
        raise ValueError(f"cannot summarize empty {metric} values")
    return MetricSummary(
        scope=scope,
        mode=mode,
        run=run,
        metric=metric,
        sample_count=len(sorted_values),
        p50_us=float(nearest_rank(sorted_values, 50)),
        p95_us=float(nearest_rank(sorted_values, 95)),
        p99_us=float(nearest_rank(sorted_values, 99)),
        max_us=float(sorted_values[-1]),
        stddev_us=statistics.pstdev(sorted_values),
        queue_send_fail_count=queue_send_fail_count,
        queue_not_received_count=queue_not_received_count,
        deadline_miss_count=deadline_miss_count,
    )


def build_summaries(runs: list[RunData]) -> list[MetricSummary]:
    summaries: list[MetricSummary] = []

    for item in runs:
        summaries.append(
            summarize_values(
                scope="run",
                mode=item.mode,
                run=f"run{item.run}",
                metric="abs_jitter_us",
                values=list(item.abs_jitter_us),
                deadline_miss_count=item.deadline_miss_count,
            )
        )
        if item.mode == "freertos":
            summaries.append(
                summarize_values(
                    scope="run",
                    mode=item.mode,
                    run=f"run{item.run}",
                    metric="queue_latency_us",
                    values=list(item.queue_latency_us),
                    queue_send_fail_count=item.queue_send_fail_count,
                    queue_not_received_count=item.queue_not_received_count,
                    deadline_miss_count=item.deadline_miss_count,
                )
            )

    for mode in ("baremetal", "freertos"):
        mode_runs = [item for item in runs if item.mode == mode]
        jitter_values = [
            value for item in mode_runs for value in item.abs_jitter_us
        ]
        deadline_total = (
            sum(item.deadline_miss_count or 0 for item in mode_runs)
            if mode == "freertos"
            else None
        )
        summaries.append(
            summarize_values(
                scope="mode",
                mode=mode,
                run="all",
                metric="abs_jitter_us",
                values=jitter_values,
                deadline_miss_count=deadline_total,
            )
        )
        if mode == "freertos":
            queue_values = [
                value for item in mode_runs for value in item.queue_latency_us
            ]
            summaries.append(
                summarize_values(
                    scope="mode",
                    mode=mode,
                    run="all",
                    metric="queue_latency_us",
                    values=queue_values,
                    queue_send_fail_count=sum(
                        item.queue_send_fail_count for item in mode_runs
                    ),
                    queue_not_received_count=sum(
                        item.queue_not_received_count for item in mode_runs
                    ),
                    deadline_miss_count=deadline_total,
                )
            )

    return summaries


def write_summary_csv(path: Path, summaries: list[MetricSummary]) -> None:
    fieldnames = [
        "scope",
        "mode",
        "run",
        "metric",
        "sample_count",
        "p50_us",
        "p95_us",
        "p99_us",
        "max_us",
        "stddev_us",
        "queue_send_fail_count",
        "queue_not_received_count",
        "deadline_miss_count",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for item in summaries:
            writer.writerow(
                {
                    "scope": item.scope,
                    "mode": item.mode,
                    "run": item.run,
                    "metric": item.metric,
                    "sample_count": item.sample_count,
                    "p50_us": f"{item.p50_us:.6f}",
                    "p95_us": f"{item.p95_us:.6f}",
                    "p99_us": f"{item.p99_us:.6f}",
                    "max_us": f"{item.max_us:.6f}",
                    "stddev_us": f"{item.stddev_us:.6f}",
                    "queue_send_fail_count": item.queue_send_fail_count,
                    "queue_not_received_count": item.queue_not_received_count,
                    "deadline_miss_count": (
                        "" if item.deadline_miss_count is None else item.deadline_miss_count
                    ),
                }
            )


def find_summary(
    summaries: list[MetricSummary], *, scope: str, mode: str, run: str, metric: str
) -> MetricSummary:
    return next(
        item
        for item in summaries
        if item.scope == scope
        and item.mode == mode
        and item.run == run
        and item.metric == metric
    )


def format_reduction(baremetal: float, freertos: float) -> tuple[float, float]:
    reduction = baremetal - freertos
    percent = reduction / baremetal * 100.0 if baremetal != 0 else 0.0
    return reduction, percent


def render_discrete_distribution_svg(
    *, title: str, metric: str, values: list[int], color: str
) -> str:
    """Render an exact-value histogram with a logarithmic count axis."""
    counts = Counter(values)
    categories = sorted(counts)
    total = len(values)
    width = 960
    height = 520
    left = 90
    right = 30
    top = 75
    bottom = 105
    plot_width = width - left - right
    plot_height = height - top - bottom
    max_log = math.log10(max(counts.values()) + 1)
    slot = plot_width / len(categories)
    bar_width = min(74.0, slot * 0.68)

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="520" viewBox="0 0 960 520" role="img">',
        f"<title>{escape(title)}</title>",
        '<rect width="960" height="520" fill="#ffffff"/>',
        f'<text x="480" y="36" text-anchor="middle" font-family="sans-serif" font-size="22" font-weight="600">{escape(title)}</text>',
        f'<text x="480" y="60" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#555">n={total}; bar height uses log10(count + 1)</text>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#333"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#333"/>',
    ]

    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = top + plot_height * (1.0 - fraction)
        count_hint = round(10 ** (max_log * fraction) - 1)
        lines.extend(
            [
                f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#dddddd"/>',
                f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" font-family="sans-serif" font-size="12" fill="#555">{count_hint}</text>',
            ]
        )

    for index, value in enumerate(categories):
        count = counts[value]
        bar_height = math.log10(count + 1) / max_log * plot_height
        x = left + slot * index + (slot - bar_width) / 2
        y = top + plot_height - bar_height
        center = x + bar_width / 2
        percent = count / total * 100.0
        lines.extend(
            [
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" fill="{color}" rx="2"/>',
                f'<text x="{center:.1f}" y="{max(top - 7, y - 7):.1f}" text-anchor="middle" font-family="sans-serif" font-size="11">{count}</text>',
                f'<text x="{center:.1f}" y="{top + plot_height + 22}" text-anchor="middle" font-family="sans-serif" font-size="12">{value}</text>',
                f'<text x="{center:.1f}" y="{top + plot_height + 42}" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#555">{percent:.2f}%</text>',
            ]
        )

    lines.extend(
        [
            f'<text x="{left + plot_width / 2:.1f}" y="{height - 18}" text-anchor="middle" font-family="sans-serif" font-size="14">{escape(metric)} (us)</text>',
            f'<text x="22" y="{top + plot_height / 2:.1f}" text-anchor="middle" font-family="sans-serif" font-size="14" transform="rotate(-90 22 {top + plot_height / 2:.1f})">sample count (log scale)</text>',
            "</svg>",
        ]
    )
    return "\n".join(lines) + "\n"


def write_distribution_figures(figures_dir: Path, runs: list[RunData]) -> list[Path]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    specs = [
        (
            figures_dir / "w07_baremetal_abs_jitter_distribution.svg",
            "W07 bare-metal absolute jitter distribution",
            "abs(jitter_us)",
            [value for item in runs if item.mode == "baremetal" for value in item.abs_jitter_us],
            "#d97706",
        ),
        (
            figures_dir / "w07_freertos_abs_jitter_distribution.svg",
            "W07 FreeRTOS absolute jitter distribution",
            "abs(jitter_us)",
            [value for item in runs if item.mode == "freertos" for value in item.abs_jitter_us],
            "#2563eb",
        ),
        (
            figures_dir / "w07_freertos_queue_latency_distribution.svg",
            "W07 FreeRTOS queue latency distribution",
            "queue_latency_us",
            [value for item in runs if item.mode == "freertos" for value in item.queue_latency_us],
            "#059669",
        ),
    ]
    for path, title, metric, values, color in specs:
        path.write_text(
            render_discrete_distribution_svg(
                title=title, metric=metric, values=values, color=color
            ),
            encoding="utf-8",
        )
    return [item[0] for item in specs]


def render_report(
    runs: list[RunData],
    summaries: list[MetricSummary],
    data_dir: Path,
    figure_paths: list[Path],
    report_path: Path,
) -> str:
    baremetal = find_summary(
        summaries,
        scope="mode",
        mode="baremetal",
        run="all",
        metric="abs_jitter_us",
    )
    freertos = find_summary(
        summaries,
        scope="mode",
        mode="freertos",
        run="all",
        metric="abs_jitter_us",
    )
    queue = find_summary(
        summaries,
        scope="mode",
        mode="freertos",
        run="all",
        metric="queue_latency_us",
    )
    p95_reduction, p95_percent = format_reduction(
        baremetal.p95_us, freertos.p95_us
    )
    p99_reduction, p99_percent = format_reduction(
        baremetal.p99_us, freertos.p99_us
    )

    lines = [
        "# W07 RTOS Jitter Summary",
        "",
        "## Analysis Method",
        "",
        f"- Input directory: `{data_dir.as_posix()}`",
        "- Dataset: Raspberry Pi Pico measured CSV, bare-metal / FreeRTOS each 3 runs",
        "- Jitter metric: `abs(jitter_us)`",
        "- Jitter samples: exclude sample 1 because its `delta_us=0` and `jitter_us=0` are synthetic",
        "- Samples per jitter run: 999 intervals",
        "- Mode summary: pooled 2997 intervals from 3 runs",
        "- Percentiles: nearest-rank",
        "- Stddev: population standard deviation",
        "- Queue latency: all valid FreeRTOS events, including sample 1",
        "- Deadline miss: the run-level final counter is counted once per run",
        "",
        "## Distribution Figures",
        "",
        "Bars represent every distinct observed value. The count axis is logarithmic so rare outliers remain visible; the exact count and percentage are printed for each bar.",
        "",
    ]
    for figure_path in figure_paths:
        relative_path = figure_path.relative_to(report_path.parent).as_posix()
        lines.extend([f"![{figure_path.stem}]({relative_path})", ""])

    lines.extend(
        [
            "## Run-level abs(jitter_us)",
            "",
            "| mode | run | intervals | P50 (us) | P95 (us) | P99 (us) | max (us) | stddev (us) | deadline miss |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for mode in ("baremetal", "freertos"):
        for run in EXPECTED_RUNS:
            item = find_summary(
                summaries,
                scope="run",
                mode=mode,
                run=f"run{run}",
                metric="abs_jitter_us",
            )
            deadline = "-" if item.deadline_miss_count is None else str(item.deadline_miss_count)
            lines.append(
                f"| {mode} | run{run} | {item.sample_count} | {item.p50_us:.2f} | "
                f"{item.p95_us:.2f} | {item.p99_us:.2f} | {item.max_us:.2f} | "
                f"{item.stddev_us:.2f} | {deadline} |"
            )

    lines.extend(
        [
            "",
            "## Mode-level abs(jitter_us)",
            "",
            "| mode | intervals | P50 (us) | P95 (us) | P99 (us) | max (us) | stddev (us) |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in (baremetal, freertos):
        lines.append(
            f"| {item.mode} | {item.sample_count} | {item.p50_us:.2f} | "
            f"{item.p95_us:.2f} | {item.p99_us:.2f} | {item.max_us:.2f} | "
            f"{item.stddev_us:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Bare-metal vs FreeRTOS",
            "",
            "| metric | bare-metal (us) | FreeRTOS (us) | reduction (us) | reduction (%) |",
            "| --- | ---: | ---: | ---: | ---: |",
            f"| P95 abs jitter | {baremetal.p95_us:.2f} | {freertos.p95_us:.2f} | "
            f"{p95_reduction:.2f} | {p95_percent:.2f} |",
            f"| P99 abs jitter | {baremetal.p99_us:.2f} | {freertos.p99_us:.2f} | "
            f"{p99_reduction:.2f} | {p99_percent:.2f} |",
            "",
            "A positive reduction means that FreeRTOS has lower absolute jitter than bare-metal.",
            "",
            "## Final Interpretation",
            "",
            "Under these measurement conditions, FreeRTOS task separation reduced pooled P95 and P99 absolute TX-event release jitter by 1839 us (100%) compared with the bare-metal single loop. The result is consistent with the highest-priority `tx_task` being scheduled independently of the simulated RX workload, while the bare-metal loop can check the next TX target only after its current RX-like workload iteration completes.",
            "",
            "This is not evidence that FreeRTOS is intrinsically faster. It demonstrates that explicit priority and task separation protected this periodic event from this CPU-bound background workload. The result depends on the workload and scheduling design.",
            "",
            "The timestamp is captured when the periodic TX event starts; this firmware does not send a UDP packet. Therefore, these results establish TX-event release jitter, not UDP API latency, driver completion time, or end-to-end packet latency.",
            "A real UDP path may add queueing, task scheduling, buffer allocation, network-stack locking, and driver latency, so its ordering must be measured separately.",
            "",
            "## FreeRTOS queue_latency_us",
            "",
            "| scope | samples | P50 (us) | P95 (us) | P99 (us) | max (us) | stddev (us) | send fail | not received | deadline miss |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for run in EXPECTED_RUNS:
        item = find_summary(
            summaries,
            scope="run",
            mode="freertos",
            run=f"run{run}",
            metric="queue_latency_us",
        )
        lines.append(
            f"| run{run} | {item.sample_count} | {item.p50_us:.2f} | "
            f"{item.p95_us:.2f} | {item.p99_us:.2f} | {item.max_us:.2f} | "
            f"{item.stddev_us:.2f} | {item.queue_send_fail_count} | "
            f"{item.queue_not_received_count} | {item.deadline_miss_count} |"
        )
    lines.append(
        f"| pooled | {queue.sample_count} | {queue.p50_us:.2f} | "
        f"{queue.p95_us:.2f} | {queue.p99_us:.2f} | {queue.max_us:.2f} | "
        f"{queue.stddev_us:.2f} | {queue.queue_send_fail_count} | "
        f"{queue.queue_not_received_count} | {queue.deadline_miss_count} |"
    )

    lines.extend(
        [
            "",
            "The queue-send to `state_task` receive delta is the practical task-handoff overhead proxy in this experiment: pooled P95/P99 were 8 us and the maximum was 80 us. It includes queue operations and scheduler response, so it is not an isolated CPU context-switch measurement. A trace-based context-switch measurement was not performed.",
            "",
            "All 3000 FreeRTOS events were received, with 0 queue-send failures, 0 missing receives, and 0 deadline misses. Correct priority ordering was required: `TX=3`, `STATE=2`, `RX=1`. Before that correction, the continuously ready RX task starved the lower-priority queue consumer; that diagnostic run is excluded from the official dataset.",
            "",
            "## Experiment Conditions",
            "",
            "- Target: Raspberry Pi Pico; Raspberry Pi 5 was the build, flashing, capture, and analysis host.",
            "- Period: 10000 us; 1000 samples per run; 3 independent runs per mode.",
            "- Workload: `RX_WORKLOAD_ITERS=20000` in both firmware variants.",
            "- Bare-metal schedule: absolute `target_time_us += 10000` in a single loop.",
            "- FreeRTOS schedule: `xTaskDelayUntil()` with task priorities `TX=3`, `STATE=2`, `RX=1`.",
            "- Capture rule: store timestamps in RAM and print CSV only after all samples are captured.",
            "- Transport for results: Pico USB CDC serial; no GPIO UART wiring.",
            "- Bare-metal firmware SHA256: `78402461cfafa6d5ece5a19c43fc485e880be14f3dc1b483bc64c92eb8ffcd85`.",
            "- FreeRTOS firmware SHA256: `af028e2be0ed34e629564bcbb73c45b3d499edc0dc8438fb2bec647f40b803ee`.",
            "",
            "## Constraints And Unverified Items",
            "",
            "- UDP API, network driver, on-wire transmission, receiver arrival, and end-to-end latency were not measured.",
            "- `queue_latency_us` is a task-handoff proxy, not a direct context-switch trace.",
            "- A hardware timer/interrupt-driven bare-metal implementation was not compared.",
            "- Results may change with workload shape, compiler optimization, FreeRTOS tick rate, priority assignment, network stack, or board.",
            "- The dataset covers one Pico and three runs per mode; broader hardware and long-duration repeatability were not evaluated.",
            "",
            "## Milestone 8 Evidence Package",
            "",
            "| evidence | artifact | related PR |",
            "| --- | --- | --- |",
            "| implementation plan | [`docs/w07_plan.md`](../docs/w07_plan.md) | [#110](https://github.com/yosukev2/adaptive-udp-link/pull/110) |",
            "| firmware and build/run record | [`firmware/w07_rtos_jitter/`](../firmware/w07_rtos_jitter/) and [`docs/w07_run_log.md`](../docs/w07_run_log.md) | [#108](https://github.com/yosukev2/adaptive-udp-link/pull/108), [#117](https://github.com/yosukev2/adaptive-udp-link/pull/117) |",
            "| task architecture and priority design | [`docs/w07_task_architecture.md`](../docs/w07_task_architecture.md) | [#111](https://github.com/yosukev2/adaptive-udp-link/pull/111), [#118](https://github.com/yosukev2/adaptive-udp-link/pull/118), [#120](https://github.com/yosukev2/adaptive-udp-link/pull/120) |",
            "| bare-metal Pico captures | [`data/w07/baremetal_run1.csv`](../data/w07/baremetal_run1.csv), [`run2`](../data/w07/baremetal_run2.csv), [`run3`](../data/w07/baremetal_run3.csv) | [#119](https://github.com/yosukev2/adaptive-udp-link/pull/119) |",
            "| FreeRTOS Pico captures | [`data/w07/freertos_run1.csv`](../data/w07/freertos_run1.csv), [`run2`](../data/w07/freertos_run2.csv), [`run3`](../data/w07/freertos_run3.csv) | [#121](https://github.com/yosukev2/adaptive-udp-link/pull/121) |",
            "| validation and statistics | [`scripts/analyze_w07_jitter.py`](../scripts/analyze_w07_jitter.py) and [`data/w07/w07_jitter_summary.csv`](../data/w07/w07_jitter_summary.csv) | [#122](https://github.com/yosukev2/adaptive-udp-link/pull/122) |",
            "| final report and distributions | this report and [`reports/figures/`](figures/) | Issue [#107](https://github.com/yosukev2/adaptive-udp-link/issues/107) |",
            "",
            "## Input Runs",
            "",
        ]
    )
    for item in runs:
        lines.append(f"- `{item.path.as_posix()}`")

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    data_dir = Path(args.data_dir)
    summary_csv = Path(args.summary_csv)
    report_path = Path(args.report)
    figures_dir = Path(args.figures_dir)

    try:
        runs = discover_runs(data_dir)
        summaries = build_summaries(runs)
        write_summary_csv(summary_csv, summaries)
        figure_paths = write_distribution_figures(figures_dir, runs)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_report(runs, summaries, data_dir, figure_paths, report_path),
            encoding="utf-8",
        )
    except (CSVValidationError, OSError, ValueError, StopIteration) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] validated {len(runs)} runs")
    print(f"[INFO] wrote {summary_csv}")
    print(f"[INFO] wrote {report_path}")
    for figure_path in figure_paths:
        print(f"[INFO] wrote {figure_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
