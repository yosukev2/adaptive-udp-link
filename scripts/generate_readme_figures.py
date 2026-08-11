#!/usr/bin/env python3
"""Generate the three summary figures embedded in the top-level README."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import japanize_matplotlib  # noqa: F401  (IPAexGothicのfallback登録)
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo", "Yu Gothic", "IPAexGothic"]


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "reports" / "figures"

NAVY = "#16324F"
BLUE = "#2878B5"
LIGHT_BLUE = "#A8CCEA"
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
            f'短時間outageでの誤検知なし: 0.5 s {short_success["500"]}/3、'
            f'1.0 s {short_success["1000"]}/3   ｜   '
            f"3 s outageでの完全復旧経路: {long_success}/3"
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
    run_rows = [
        row
        for row in rows
        if row["scope"] == "run"
        and row["metric"] == "abs_jitter_us"
        and row["mode"] in {"baremetal", "freertos"}
    ]

    metrics = ["P95", "P99", "Max"]
    columns = ["p95_us", "p99_us", "max_us"]
    values = {
        mode: [
            [
                float(row[column])
                for row in sorted(run_rows, key=lambda item: item["run"])
                if row["mode"] == mode
            ]
            for column in columns
        ]
        for mode in ("baremetal", "freertos")
    }

    means = {
        mode: [float(np.mean(metric_values)) for metric_values in mode_values]
        for mode, mode_values in values.items()
    }

    x = np.arange(len(metrics))
    width = 0.30
    offset = 0.18
    bare_positions = x - offset
    rtos_positions = x + offset
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    bare_bars = ax.bar(
        bare_positions,
        means["baremetal"],
        width,
        color=ORANGE,
        label="Bare-metal",
    )
    rtos_bars = ax.bar(
        rtos_positions,
        means["freertos"],
        width,
        color=BLUE,
        label="FreeRTOS",
    )

    run_offsets = np.array([-0.065, 0.0, 0.065])
    for metric_index in range(len(metrics)):
        for position, mode in (
            (bare_positions[metric_index], "baremetal"),
            (rtos_positions[metric_index], "freertos"),
        ):
            ax.scatter(
                position + run_offsets,
                values[mode][metric_index],
                s=31,
                facecolor="white",
                edgecolor=NAVY,
                linewidth=1.0,
                zorder=3,
                clip_on=False,
            )

    def format_mean(value: float) -> str:
        return f"{value:,.0f}" if value.is_integer() else f"{value:,.1f}"

    for bars, mode in ((bare_bars, "baremetal"), (rtos_bars, "freertos")):
        ax.bar_label(
            bars,
            labels=[format_mean(value) for value in means[mode]],
            padding=5,
            fontsize=9,
        )

    ax.set_title("周期TX開始時刻のずれ")
    ax.set_ylabel("開始時刻のずれ [µs]（3 run平均）")
    positions = np.column_stack((bare_positions, rtos_positions)).ravel()
    ax.set_xticks(positions, ["Bare-metal", "FreeRTOS"] * len(metrics))
    for position, metric in zip(x, metrics):
        ax.text(
            position,
            -0.13,
            metric,
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
            color=NAVY,
        )
    upper = max(value for mode_values in values.values() for dataset in mode_values for value in dataset) * 1.22
    ax.set_ylim(-upper * 0.04, upper)
    ax.set_xlim(-0.42, len(metrics) - 0.58)
    ax.grid(axis="y", alpha=0.8)
    ax.spines[["right", "top"]].set_visible(False)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    save_figure(fig, "readme_rtos_jitter.png")


def generate_linux_pico_figure() -> None:
    rows = read_csv(ROOT / "data" / "w06" / "jitter_comparison.csv")
    samples: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        samples[row["env"]].append(abs(int(row["jitter_us"])))

    def nearest_rank(values: list[int], pct: float) -> int:
        ordered = sorted(values)
        rank = max(1, int(np.ceil(pct / 100.0 * len(ordered))))
        return ordered[rank - 1]

    metrics = ["P95", "P99", "Max"]
    linux = [
        nearest_rank(samples["linux_rpi5"], 95),
        nearest_rank(samples["linux_rpi5"], 99),
        max(samples["linux_rpi5"]),
    ]
    pico = [
        nearest_rank(samples["pico"], 95),
        nearest_rank(samples["pico"], 99),
        max(samples["pico"]),
    ]

    x = np.arange(len(metrics))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    linux_bars = ax.bar(
        x - width / 2,
        linux,
        width,
        label="Pi 5 Linux user-space loop",
        color=LIGHT_BLUE,
    )
    pico_bars = ax.bar(
        x + width / 2,
        pico,
        width,
        label="Pico hardware-timer loop",
        color=BLUE,
    )
    ax.bar_label(linux_bars, labels=[f"{value:,}" for value in linux], padding=4)
    ax.bar_label(pico_bars, labels=[f"{value:,}" for value in pico], padding=4)
    ax.set_title("Linuxを比較基準にしたPicoの周期jitter（10 ms周期、各1,000 sample）")
    ax.set_ylabel("絶対jitter（μs）")
    ax.set_xticks(x, metrics)
    ax.set_ylim(0, max(linux) * 1.22)
    ax.grid(axis="y", alpha=0.8)
    ax.spines[["right", "top"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    save_figure(fig, "readme_linux_pico_jitter.png")


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
            "1.2k frames/s",
            fec_aggregate(
                ROOT / "data" / "w09" / "fec_comparison" / "fec_comparison.csv"
            ),
        ),
        (
            "120k frames/s",
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
    off_bars = ax.bar(x - width / 2, off_values, width, label="FECなし", color=LIGHT_BLUE)
    xor_bars = ax.bar(
        x + width / 2,
        xor_values,
        width,
        label="XOR FEC（k=4、r=1）",
        color=BLUE,
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
            f"欠落 −{reduction:.1f}%\n有効なデータグラム +{gain:,}件",
            ha="center",
            va="bottom",
            color=ORANGE,
            fontsize=9.5,
            fontweight="bold",
        )

    ax.set_title("ランダムdatagram 10%欠落に対するXOR FEC")
    ax.set_ylabel("実効欠落率")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 14)
    ax.grid(axis="y", alpha=0.8)
    ax.spines[["right", "top"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    ax.text(
        0.01,
        -0.2,
        "同一seed 101–110・各mode 10 trial・1 trial 30秒",
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
    generate_linux_pico_figure()
    generate_fec_figure()
    print(f"Generated README figures in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
