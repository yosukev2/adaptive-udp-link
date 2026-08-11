#!/usr/bin/env python3
"""Generate the W08 CPU-affinity per-run timeseries figures embedded in the README.

Inputs:
  <data-dir>/rate_{rate}_rxpin_on_txpin_off_run3.csv
  (columns: rcv_time_ns,seq,send_time_ns,latency_ns,missing_delta,parse_status)

Outputs (reports/figures/):
  w08_cpu_affinity_rate_{rate}_rxpin_on_txpin_off_run3_timeseries.png
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import japanize_matplotlib  # noqa: F401  (フォント設定のためのimport)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo", "Yu Gothic", "IPAexGothic"]

ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "reports" / "figures"
TARGETS = [(100000, 3), (50000, 3)]


def generate_timeseries(data_dir: Path, rate: int, run: int) -> None:
    path = data_dir / f"rate_{rate}_rxpin_on_txpin_off_run{run}.csv"
    seq: list[int] = []
    latency_ms: list[float] = []
    missing_delta: list[int] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            seq.append(int(row["seq"]))
            latency_ms.append(int(row["latency_ns"]) / 1e6)
            missing_delta.append(int(row["missing_delta"]))

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(12, 8))
    ax1.plot(seq, latency_ms, linewidth=0.5, color="#2878B5", rasterized=True)
    ax1.set_yscale("log")
    ax1.set_title(
        f"CPU affinity rate={rate:,} Hz・RX固定のみ（run{run}）: 遅延の時系列（log目盛）"
    )
    ax1.set_ylabel("遅延 (ms、log目盛)")
    ax2.plot(seq, missing_delta, linewidth=0.8, color="#D1495B", rasterized=True)
    ax2.set_title("欠落数（missing_delta）の時系列")
    ax2.set_xlabel("sequence番号")
    ax2.set_ylabel("欠落数（件）")
    for ax in (ax1, ax2):
        ax.grid(alpha=0.3)
    fig.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        FIGURE_DIR
        / f"w08_cpu_affinity_rate_{rate}_rxpin_on_txpin_off_run{run}_timeseries.png",
        dpi=150,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "w08" / "cpu_affinity_matrix",
        help="rate_*_rxpin_on_txpin_off_run*.csv を含むディレクトリ",
    )
    args = parser.parse_args()
    for rate, run in TARGETS:
        generate_timeseries(args.data_dir, rate, run)
    print(f"Generated W08 CPU-affinity timeseries figures in {FIGURE_DIR}")


if __name__ == "__main__":
    main()
