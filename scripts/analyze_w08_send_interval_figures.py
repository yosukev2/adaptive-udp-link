#!/usr/bin/env python3
"""Generate the W08 send-interval sweep figure embedded in the README.

Input:  data/w08/send_interval/w08_send_interval_summary.csv
Output: reports/figures/w08_send_interval_missing_p99.png
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import japanize_matplotlib  # noqa: F401  (フォント設定のためのimport)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo", "Yu Gothic", "IPAexGothic"]
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "reports" / "figures"

SERIES = "#2a78d6"
TEXT = "#0b0b0b"
TEXT2 = "#52514e"
SURFACE = "#ffffff"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=ROOT / "data" / "w08" / "send_interval" / "w08_send_interval_summary.csv",
    )
    args = parser.parse_args()

    rows = defaultdict(list)
    with args.summary_csv.open(encoding="utf-8", newline="") as handle:
        for r in csv.DictReader(handle):
            rows[int(r["rate_hz"])].append(
                (float(r["missing_rate"]) * 100.0, float(r["p99_latency_ms"]))
            )

    rates = sorted(rows)
    miss_mean = [sum(v[0] for v in rows[r]) / len(rows[r]) for r in rates]
    p99_mean = [sum(v[1] for v in rows[r]) / len(rows[r]) for r in rates]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, sharex=True, figsize=(8, 5.4), dpi=150, facecolor=SURFACE
    )

    for ax, mean, label in (
        (ax1, miss_mean, "欠落率 (%)"),
        (ax2, p99_mean, "P99遅延 (ms)"),
    ):
        ax.set_facecolor(SURFACE)
        for r in rates:
            vals = rows[r]
            idx = 0 if ax is ax1 else 1
            ax.plot([r] * len(vals), [v[idx] for v in vals], "o",
                    color=SERIES, alpha=0.25, markersize=5, markeredgewidth=0)
        ax.plot(rates, mean, "-o", color=SERIES, linewidth=2, markersize=6,
                markeredgecolor=SURFACE, markeredgewidth=1)
        ax.set_ylabel(label, color=TEXT, fontsize=10)
        ax.grid(True, which="major", axis="both", color="#000000", alpha=0.08,
                linewidth=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#c9c8c2")
        ax.tick_params(colors=TEXT2, labelsize=9)
        ax.axvline(120_000, color=TEXT2, linewidth=1, linestyle=(0, (4, 3)),
                   alpha=0.6)

    ax1.set_title("送信レートを上げたときの欠落率とP99遅延（loopback、trial平均）",
                  color=TEXT, fontsize=11, pad=12)
    ax1.annotate("120 kHzまで欠落なし", xy=(120_000, 0.05), xytext=(3_000, 1.6),
                 color=TEXT2, fontsize=9,
                 arrowprops=dict(arrowstyle="-", color=TEXT2, alpha=0.5))
    i500 = rates.index(500_000)
    ax1.annotate(f"500 kHzで{miss_mean[i500]:.2f}%",
                 xy=(500_000, miss_mean[i500]),
                 xytext=(140_000, miss_mean[i500] + 1.2), color=TEXT, fontsize=9,
                 arrowprops=dict(arrowstyle="-", color=TEXT2, alpha=0.5))
    ax2.annotate(f"500 kHzで{p99_mean[i500]:.3f} ms",
                 xy=(500_000, p99_mean[i500]),
                 xytext=(110_000, p99_mean[i500] * 3), color=TEXT, fontsize=9,
                 arrowprops=dict(arrowstyle="-", color=TEXT2, alpha=0.5))

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("送信レート (Hz、対数軸)", color=TEXT, fontsize=10)
    ax2.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{v/1e6:g}M" if v >= 1e6
        else (f"{v/1000:g}k" if v >= 1000 else f"{v:g}")))

    i1m = rates.index(1_000_000)
    ax1.annotate("1 MHzは受信数が期待値から乖離し\n測定として信頼できない領域",
                 xy=(1_000_000, miss_mean[i1m]),
                 xytext=(1_000_000, 2.75), color=TEXT2, fontsize=8.5,
                 ha="right",
                 arrowprops=dict(arrowstyle="-", color=TEXT2, alpha=0.5))

    fig.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURE_DIR / "w08_send_interval_missing_p99.png",
                facecolor=SURFACE, bbox_inches="tight")
    print(f"Generated send-interval figure in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
