#!/usr/bin/env python3
"""Generate the three summary figures embedded in the top-level README."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import japanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "reports" / "figures"

NAVY = "#16324F"
BLUE = "#2878B5"
ORANGE = "#F28E2B"
RED = "#D1495B"
GREEN = "#2A9D8F"
LIGHT_GRID = "#D9E2EC"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def configure_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.edgecolor": "#9AA5B1",
            "axes.labelcolor": NAVY,
            "axes.titlecolor": NAVY,
            "axes.titleweight": "bold",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "grid.color": LIGHT_GRID,
            "grid.linewidth": 0.8,
            "xtick.color": "#52606D",
            "ytick.color": "#52606D",
        }
    )


def save_figure(fig: plt.Figure, filename: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / filename, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def generate_fsm_figure() -> None:
    state_path = (
        ROOT
        / "logs"
        / "fsm_recovery"
        / "w05_compare_baseline"
        / "mode_fsm"
        / "scenario_3000ms"
        / "trial_1"
        / "state.csv"
    )
    runs_path = (
        ROOT
        / "logs"
        / "fsm_recovery"
        / "w05_compare_baseline"
        / "compare_runs.csv"
    )
    transitions = read_csv(state_path)
    runs = read_csv(runs_path)

    segment_starts = [0.0]
    states = ["Normal"]
    for row in transitions:
        segment_starts.append(float(row["elapsed_ms"]) / 1000.0)
        states.append(row["to_state"])
    chart_end = max(9.0, segment_starts[-1] + 1.0)
    segment_ends = segment_starts[1:] + [chart_end]

    state_colors = {
        "Normal": GREEN,
        "Degraded": RED,
        "Recover": ORANGE,
    }

    fig, ax = plt.subplots(figsize=(10.4, 3.5))
    for start, end, state in zip(segment_starts, segment_ends, states):
        ax.broken_barh(
            [(start, end - start)],
            (0.25, 0.5),
            facecolors=state_colors[state],
            edgecolors="white",
            linewidth=2,
        )
        if end - start >= 0.65:
            ax.text(
                (start + end) / 2,
                0.5,
                state,
                color="white",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

    for row in transitions:
        elapsed_s = float(row["elapsed_ms"]) / 1000.0
        ax.axvline(elapsed_s, color=NAVY, linewidth=1, linestyle="--", alpha=0.7)
        ax.text(
            elapsed_s,
            0.87,
            f'{row["elapsed_ms"]} ms',
            ha="center",
            va="bottom",
            fontsize=8.5,
            color=NAVY,
        )

    short_success = {}
    for outage_ms in ("500", "1000"):
        matching = [
            row
            for row in runs
            if row["mode"] == "fsm" and row["outage_ms"] == outage_ms
        ]
        short_success[outage_ms] = sum(
            row["observed_pattern"] == "none" for row in matching
        )
    long_runs = [
        row
        for row in runs
        if row["mode"] == "fsm" and row["outage_ms"] == "3000"
    ]
    long_success = sum(
        row["observed_pattern"] == "Normal->Degraded->Recover->Normal"
        for row in long_runs
    )

    ax.text(
        0.01,
        -0.37,
        (
            f'No state flapping: 0.5 s {short_success["500"]}/3, '
            f'1.0 s {short_success["1000"]}/3   |   '
            f"Full recovery path on 3 s outage: {long_success}/3"
        ),
        transform=ax.transAxes,
        fontsize=9.5,
        color=NAVY,
        fontweight="bold",
    )
    ax.set_title("FSM状態遷移 — 3秒outageの代表trial")
    ax.set_xlabel("RX経過時間（秒）")
    ax.set_xlim(0, chart_end)
    ax.set_ylim(0.05, 1.08)
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.8)
    ax.spines[["left", "right", "top"]].set_visible(False)
    fig.tight_layout()
    save_figure(fig, "readme_fsm_recovery.png")


def generate_rtos_figure() -> None:
    rows = read_csv(ROOT / "data" / "w07" / "w07_jitter_summary.csv")
    mode_rows = {
        row["mode"]: row
        for row in rows
        if row["scope"] == "mode"
        and row["metric"] == "abs_jitter_us"
        and row["mode"] in {"baremetal", "freertos"}
    }

    metrics = ["P95", "P99", "Max"]
    columns = ["p95_us", "p99_us", "max_us"]
    baremetal = [float(mode_rows["baremetal"][column]) for column in columns]
    freertos = [float(mode_rows["freertos"][column]) for column in columns]

    x = np.arange(len(metrics))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    bare_bars = ax.bar(
        x - width / 2,
        baremetal,
        width,
        label="Bare-metal単一loop",
        color=ORANGE,
    )
    rtos_bars = ax.bar(
        x + width / 2,
        freertos,
        width,
        label="FreeRTOS task分離",
        color=BLUE,
    )

    ax.bar_label(bare_bars, labels=[f"{value:,.0f}" for value in baremetal], padding=4)
    ax.bar_label(rtos_bars, labels=[f"{value:,.0f}" for value in freertos], padding=4)
    ax.set_title("CPU負荷下におけるTXイベントのリリースジッタ")
    ax.set_ylabel("絶対ジッタ（µs、3 run統合）")
    ax.set_xticks(x, metrics)
    ax.set_ylim(0, max(baremetal) * 1.22)
    ax.grid(axis="y", alpha=0.8)
    ax.spines[["right", "top"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    ax.text(
        0.01,
        0.92,
        "P99: 1,839 → 0 µs\nQueue handoff P99: 8 µs\n3,000/3,000 events received",
        transform=ax.transAxes,
        va="top",
        fontsize=9.5,
        color=NAVY,
        bbox={
            "boxstyle": "round,pad=0.45",
            "facecolor": "#F0F7FF",
            "edgecolor": "#B8D8F0",
        },
    )
    fig.tight_layout()
    save_figure(fig, "readme_rtos_jitter.png")


def fec_aggregate(path: Path) -> dict[str, dict[str, float]]:
    rows = read_csv(path)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["fec_mode"]].append(row)

    result = {}
    for mode, mode_rows in grouped.items():
        effective_missing = sum(
            int(row["effective_missing_total"]) for row in mode_rows
        )
        unique_received = sum(
            int(row["unique_received_frames_total"]) for row in mode_rows
        )
        result[mode] = {
            "effective_missing_rate_pct": (
                100.0 * effective_missing / (effective_missing + unique_received)
            ),
            "usable_datagrams": sum(
                int(row["usable_datagrams"]) for row in mode_rows
            ),
        }
    return result


def generate_fec_figure() -> None:
    datasets = [
        (
            "1,200 frames/s",
            fec_aggregate(
                ROOT / "data" / "w09" / "fec_comparison" / "fec_comparison.csv"
            ),
        ),
        (
            "120,000 frames/s",
            fec_aggregate(
                ROOT
                / "data"
                / "w09"
                / "fec_comparison_rate_120000"
                / "fec_comparison.csv"
            ),
        ),
    ]

    labels = [label for label, _ in datasets]
    off_values = [
        values["off"]["effective_missing_rate_pct"] for _, values in datasets
    ]
    xor_values = [
        values["xor"]["effective_missing_rate_pct"] for _, values in datasets
    ]

    x = np.arange(len(labels))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    off_bars = ax.bar(x - width / 2, off_values, width, label="FECなし", color=RED)
    xor_bars = ax.bar(
        x + width / 2,
        xor_values,
        width,
        label="XOR FEC（k=4、r=1）",
        color=GREEN,
    )
    ax.bar_label(off_bars, labels=[f"{value:.2f}%" for value in off_values], padding=4)
    ax.bar_label(xor_bars, labels=[f"{value:.2f}%" for value in xor_values], padding=4)

    for index, (_, values) in enumerate(datasets):
        reduction = (
            1
            - values["xor"]["effective_missing_rate_pct"]
            / values["off"]["effective_missing_rate_pct"]
        ) * 100
        gain = (
            values["xor"]["usable_datagrams"]
            - values["off"]["usable_datagrams"]
        )
        ax.text(
            index,
            max(off_values[index], xor_values[index]) + 0.9,
            f"−{reduction:.1f}% missing\n+{gain:,} usable datagrams",
            ha="center",
            va="bottom",
            color=NAVY,
            fontsize=9.5,
            fontweight="bold",
        )

    ax.set_title("再現可能なランダムdatagram 10%欠落に対するXOR FEC")
    ax.set_ylabel("実効missing率")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 14)
    ax.grid(axis="y", alpha=0.8)
    ax.spines[["right", "top"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    ax.text(
        0.01,
        -0.2,
        "Paired seeds 101–110 · 10 trials per mode · 30 s per trial",
        transform=ax.transAxes,
        fontsize=9,
        color="#52606D",
    )
    fig.tight_layout()
    save_figure(fig, "readme_fec_effect.png")


def main() -> None:
    configure_plot_style()
    generate_fsm_figure()
    generate_rtos_figure()
    generate_fec_figure()
    print(f"Generated README figures in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
