#!/usr/bin/env python3
"""Generate the W09 adaptive-rate figures embedded in the README.

Inputs:
  - reports/w09_adaptive_rate_run_summary.csv (per-trial summary, off/on x 10)
  - <data-dir>/{off,on}_run{1..10}_adaptive_log.csv (per-feedback-window log)

Outputs (reports/figures/):
  - w09_adaptive_off_on_boxplot.png
  - w09_adaptive_missing_rate_histogram.png
  - w09_adaptive_off_all_trials_missing_rate.png
  - w09_adaptive_on_all_trials_rate_missing.png
  - w09_adaptive_on_run{1..10}_missing_rate_rate_hz.png
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import japanize_matplotlib  # noqa: F401  (フォント設定のためのimport)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo", "Yu Gothic", "IPAexGothic"]

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "reports" / "figures"
RUNS = range(1, 11)
CAPTION_COLOR = "#52606D"
RATE_FORMATTER = FuncFormatter(
    lambda v, _: f"{v/1e6:g}M" if v >= 1e6 else (f"{v/1000:g}k" if v >= 1000 else f"{v:g}")
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def save_figure(fig: plt.Figure, filename: str, caption: str | None = None) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    if caption:
        fig.text(0.01, -0.03, caption, va="top", fontsize=9, color=CAPTION_COLOR)
    fig.savefig(FIGURE_DIR / filename, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def load_adaptive_logs(data_dir: Path, mode: str) -> dict[int, list[dict[str, str]]]:
    return {
        run: read_csv(data_dir / f"{mode}_run{run}_adaptive_log.csv")
        for run in RUNS
    }


def generate_boxplot(summary_path: Path) -> None:
    rows = read_csv(summary_path)
    missing = {
        mode: [
            float(row["raw_missing_rate"]) * 100.0
            for row in rows
            if row["mode"] == mode
        ]
        for mode in ("off", "on")
    }
    latency = {
        mode: [
            float(row["raw_avg_latency_ms"])
            for row in rows
            if row["mode"] == mode
        ]
        for mode in ("off", "on")
    }

    positions = [0.85, 1.15]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.boxplot(
        [missing["off"], missing["on"]],
        positions=positions,
        widths=0.18,
        tick_labels=["OFF", "ON"],
    )
    ax1.set_ylabel("欠落率 (%)")
    ax2.boxplot(
        [latency["off"], latency["on"]],
        positions=positions,
        widths=0.18,
        tick_labels=["OFF", "ON"],
    )
    ax2.set_ylabel("平均遅延 (ms)")
    for ax in (ax1, ax2):
        ax.set_xlim(0.6, 1.4)
        ax.grid(axis="y", alpha=0.3)
    fig.suptitle("Adaptive Rate OFF/ON: trial間の分布（各10 trial）")
    save_figure(fig, "w09_adaptive_off_on_boxplot.png")


def generate_histogram(off_logs, on_logs) -> None:
    off_rates = [
        float(row["missing_rate"]) * 100.0
        for log in off_logs.values()
        for row in log
    ]
    on_rates = [
        float(row["missing_rate"]) * 100.0
        for log in on_logs.values()
        for row in log
    ]
    upper = max(off_rates + on_rates + [1.0])
    bins = [x * 1.0 for x in range(int(upper) + 2)]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.hist(
        off_rates,
        bins=bins,
        label=f"OFF window数={len(off_rates)}",
        color="#9AA5B1",
        edgecolor="black",
        alpha=0.8,
    )
    ax.hist(
        on_rates,
        bins=bins,
        label=f"ON window数={len(on_rates)}",
        color="#2878B5",
        edgecolor="black",
        alpha=0.6,
    )
    ax.set_yscale("symlog")
    ax.set_title("Adaptive Rate OFF/ON: feedback window（約1秒）ごとの欠落率分布")
    ax.set_xlabel("feedback windowごとの欠落率 (%)")
    ax.set_ylabel("window数（symlog目盛）")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    save_figure(fig, "w09_adaptive_missing_rate_histogram.png")


def generate_off_all_trials(off_logs) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))
    for run, log in off_logs.items():
        ax.plot(
            [float(row["elapsed_sec"]) for row in log],
            [float(row["missing_rate"]) * 100.0 for row in log],
            marker="o",
            markersize=3,
            linewidth=1.2,
            label=f"run{run}",
        )
    ax.set_title("Adaptive Rate OFF: 全trialの欠落率推移（レート固定 120 kHz）")
    ax.set_xlabel("経過時間（秒）")
    ax.set_ylabel("欠落率 (%)")
    ax.grid(alpha=0.3)
    ax.legend(ncols=5, fontsize=9)
    save_figure(fig, "w09_adaptive_off_all_trials_missing_rate.png")


def generate_on_all_trials(on_logs) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
    for run, log in on_logs.items():
        elapsed = [float(row["elapsed_sec"]) for row in log]
        ax1.plot(
            elapsed,
            [float(row["new_rate_hz"]) for row in log],
            marker="o",
            markersize=3,
            linewidth=1.2,
            label=f"run{run}",
        )
        ax2.plot(
            elapsed,
            [float(row["missing_rate"]) * 100.0 for row in log],
            marker="o",
            markersize=3,
            linewidth=1.2,
        )
    ax1.set_title("Adaptive Rate ON: 全trialの送信レートと欠落率の推移")
    ax1.set_ylabel("送信レート (Hz)")
    ax1.yaxis.set_major_formatter(RATE_FORMATTER)
    ax2.set_xlabel("経過時間（秒）")
    ax2.set_ylabel("欠落率 (%)")
    for ax in (ax1, ax2):
        ax.grid(alpha=0.3)
    ax1.legend(ncols=5, fontsize=9)
    save_figure(fig, "w09_adaptive_on_all_trials_rate_missing.png")


def generate_on_run_figures(on_logs) -> None:
    for run, log in on_logs.items():
        elapsed = [float(row["elapsed_sec"]) for row in log]
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 6.5))
        ax1.step(
            elapsed,
            [float(row["new_rate_hz"]) for row in log],
            where="post",
            color="#2878B5",
            linewidth=1.8,
        )
        ax1.set_title(f"Adaptive Rate ON run{run}: 送信レートと欠落率の推移")
        ax1.set_ylabel("送信レート (Hz)")
        ax1.yaxis.set_major_formatter(RATE_FORMATTER)
        ax2.plot(
            elapsed,
            [float(row["missing_rate"]) * 100.0 for row in log],
            marker="o",
            markersize=4,
            color="#D1495B",
            linewidth=1.6,
        )
        ax2.set_xlabel("経過時間（秒）")
        ax2.set_ylabel("欠落率 (%)")
        for ax in (ax1, ax2):
            ax.grid(alpha=0.3)
        save_figure(fig, f"w09_adaptive_on_run{run}_missing_rate_rate_hz.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "w09" / "adaptive_rate",
        help="off/on_runN_adaptive_log.csv を含むディレクトリ",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=ROOT / "reports" / "w09_adaptive_rate_run_summary.csv",
    )
    args = parser.parse_args()

    off_logs = load_adaptive_logs(args.data_dir, "off")
    on_logs = load_adaptive_logs(args.data_dir, "on")

    generate_boxplot(args.summary_csv)
    generate_histogram(off_logs, on_logs)
    generate_off_all_trials(off_logs)
    generate_on_all_trials(on_logs)
    generate_on_run_figures(on_logs)
    print(f"Generated W09 adaptive figures in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
