#!/usr/bin/env python3
"""Validate W08 send-interval sweep CSVs and generate comparison summaries."""

from __future__ import annotations

import argparse
import csv
import math
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path


csv.field_size_limit(sys.maxsize)

EXPECTED_FIELDS = [
    "rcv_time_ns",
    "seq",
    "send_time_ns",
    "latency_ns",
    "missing_delta",
    "parse_status",
]

EXPECTED_TRIALS = (1, 2, 3)


class CSVValidationError(ValueError):
    """Raised when a W08 run does not satisfy the measurement schema."""


@dataclass(frozen=True)
class RunData:
    rate_hz: int
    trial: int
    path: Path
    sample_count: int
    mean_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    max_latency_ms: float
    stddev_latency_ms: float
    last_latency_ms: float
    ok_count: int
    parse_error_count: int
    missing_delta_total: int
    first_seq: int
    last_seq: int
    rx_1sec_rows: int
    rx_pps_mean: float | None
    rx_pps_max: float | None
    rx_cpu_pct_mean: float | None
    rx_cpu_pct_max: float | None
    tx_stats_rows: int
    tx_pps_mean: float | None
    tx_pps_max: float | None
    tx_cpu_pct_mean: float | None
    tx_cpu_pct_max: float | None

    @property
    def observed_span(self) -> int:
        return self.last_seq + 1

    @property
    def missing_rate(self) -> float:
        return self.missing_delta_total / self.observed_span if self.observed_span else 0.0

    @property
    def parse_error_rate(self) -> float:
        return self.parse_error_count / self.sample_count if self.sample_count else 0.0

    @property
    def effective_rx_hz(self) -> float:
        # W08 send interval sweeps use tx duration 10 s.
        return self.sample_count / 10.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze W08 send-interval sweep CSV runs."
    )
    parser.add_argument(
        "--data-dir",
        default="data/w08/send_interval",
        help="Directory containing rate_<hz>_run<n>.csv files. Subdirectories are searched recursively.",
    )
    parser.add_argument(
        "--summary-csv",
        default="data/w08/send_interval/w08_send_interval_summary.csv",
        help="Generated machine-readable summary CSV.",
    )
    parser.add_argument(
        "--report",
        default="reports/w08_send_interval_summary.md",
        help="Generated Markdown comparison report.",
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


def mean_or_none(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def max_or_none(values: list[float]) -> float | None:
    return max(values) if values else None


def format_optional(value: float | None, digits: int = 6) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def aux_group_for_rate(rate_hz: int) -> str:
    return "send_interval" if rate_hz in {50, 200, 500, 1000, 10000} else "send_interval_high"


@dataclass(frozen=True)
class AuxMetrics:
    rx_1sec_rows: int
    rx_pps_mean: float | None
    rx_pps_max: float | None
    rx_cpu_pct_mean: float | None
    rx_cpu_pct_max: float | None
    tx_stats_rows: int
    tx_pps_mean: float | None
    tx_pps_max: float | None
    tx_cpu_pct_mean: float | None
    tx_cpu_pct_max: float | None


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def read_rx_1sec_metrics(data_dir: Path, rate_hz: int, trial: int) -> tuple[int, list[float], list[float]]:
    group = aux_group_for_rate(rate_hz)
    path = data_dir / "raw_logs" / group / f"rate_{rate_hz}_trial{trial}" / "rx_1sec.csv"
    if not path.exists():
        path = data_dir / "raw_1sec" / group / f"rate_{rate_hz}_trial{trial}" / "rx_1sec.csv"
    if not path.exists():
        return 0, [], []

    pps_values: list[float] = []
    cpu_values: list[float] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            pps = parse_float(row.get("pps"))
            cpu_pct = parse_float(row.get("cpu_pct"))
            if pps is not None:
                pps_values.append(pps)
            if cpu_pct is not None:
                cpu_values.append(cpu_pct)
    return max(len(pps_values), len(cpu_values)), pps_values, cpu_values


def read_tx_log_metrics(data_dir: Path, rate_hz: int, trial: int) -> tuple[int, list[float], list[float]]:
    group = aux_group_for_rate(rate_hz)
    path = data_dir / "raw_logs" / group / f"rate_{rate_hz}_trial{trial}" / "tx.log"
    if not path.exists():
        return 0, [], []

    pps_values: list[float] = []
    cpu_values: list[float] = []
    pattern = re.compile(r"tx_stats .*?\bpps=([0-9.]+)\s+cpu_pct=([0-9.]+)")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = pattern.search(line)
        if match is None:
            continue
        pps_values.append(float(match.group(1)))
        cpu_values.append(float(match.group(2)))
    return len(pps_values), pps_values, cpu_values


def load_aux_metrics(data_dir: Path, rate_hz: int, trial: int) -> AuxMetrics:
    rx_rows, rx_pps_values, rx_cpu_values = read_rx_1sec_metrics(data_dir, rate_hz, trial)
    tx_rows, tx_pps_values, tx_cpu_values = read_tx_log_metrics(data_dir, rate_hz, trial)
    return AuxMetrics(
        rx_1sec_rows=rx_rows,
        rx_pps_mean=mean_or_none(rx_pps_values),
        rx_pps_max=max_or_none(rx_pps_values),
        rx_cpu_pct_mean=mean_or_none(rx_cpu_values),
        rx_cpu_pct_max=max_or_none(rx_cpu_values),
        tx_stats_rows=tx_rows,
        tx_pps_mean=mean_or_none(tx_pps_values),
        tx_pps_max=max_or_none(tx_pps_values),
        tx_cpu_pct_mean=mean_or_none(tx_cpu_values),
        tx_cpu_pct_max=max_or_none(tx_cpu_values),
    )


def load_run(path: Path, rate_hz: int, trial: int, data_dir: Path) -> RunData:
    latencies_ns: list[int] = []
    ok_count = 0
    parse_error_count = 0
    missing_delta_total = 0
    previous_seq: int | None = None
    first_seq: int | None = None
    last_seq: int | None = None

    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise CSVValidationError(f"failed to open {path}: {exc}") from exc

    with handle:
        reader = csv.DictReader(handle)
        header = [field.strip() for field in reader.fieldnames or []]
        if header != EXPECTED_FIELDS:
            raise CSVValidationError(
                f"{path}: unexpected header; expected {EXPECTED_FIELDS}, got {header}"
            )

        row_count = 0
        for row_count, row in enumerate(reader, start=1):
            line_no = row_count + 1
            seq = parse_int(row.get("seq"), "seq", path, line_no)
            latency_ns = parse_int(row.get("latency_ns"), "latency_ns", path, line_no)
            missing_delta = parse_int(
                row.get("missing_delta"), "missing_delta", path, line_no
            )
            parse_status = (row.get("parse_status") or "").strip()

            if seq < 0:
                raise CSVValidationError(f"{path}:{line_no}: seq must be non-negative")
            if previous_seq is not None and seq <= previous_seq:
                raise CSVValidationError(
                    f"{path}:{line_no}: seq {seq} is not strictly increasing"
                )
            if missing_delta < 0:
                raise CSVValidationError(
                    f"{path}:{line_no}: missing_delta must be non-negative"
                )

            if first_seq is None:
                first_seq = seq
            last_seq = seq

            observed_gap = seq if previous_seq is None else seq - previous_seq - 1
            if missing_delta != observed_gap:
                raise CSVValidationError(
                    f"{path}:{line_no}: missing_delta {missing_delta} != observed gap {observed_gap}"
                )
            missing_delta_total += missing_delta

            if parse_status == "OK":
                ok_count += 1
                latencies_ns.append(latency_ns)
            else:
                parse_error_count += 1

            previous_seq = seq

    if row_count == 0:
        raise CSVValidationError(f"{path}: no data rows")

    if ok_count == 0:
        raise CSVValidationError(f"{path}: no OK rows")
    if first_seq is None or last_seq is None:
        raise CSVValidationError(f"{path}: could not infer sequence range")

    sorted_latencies = sorted(latencies_ns)
    mean_latency_ms = statistics.fmean(sorted_latencies) / 1_000_000.0
    stddev_latency_ms = (
        statistics.pstdev(sorted_latencies) / 1_000_000.0
        if len(sorted_latencies) > 1
        else 0.0
    )
    p50_latency_ms = nearest_rank(sorted_latencies, 50) / 1_000_000.0
    p95_latency_ms = nearest_rank(sorted_latencies, 95) / 1_000_000.0
    p99_latency_ms = nearest_rank(sorted_latencies, 99) / 1_000_000.0
    max_latency_ms = max(sorted_latencies) / 1_000_000.0
    last_latency_ms = latencies_ns[-1] / 1_000_000.0
    aux = load_aux_metrics(data_dir, rate_hz, trial)

    return RunData(
        rate_hz=rate_hz,
        trial=trial,
        path=path,
        sample_count=row_count,
        mean_latency_ms=mean_latency_ms,
        p50_latency_ms=p50_latency_ms,
        p95_latency_ms=p95_latency_ms,
        p99_latency_ms=p99_latency_ms,
        max_latency_ms=max_latency_ms,
        stddev_latency_ms=stddev_latency_ms,
        last_latency_ms=last_latency_ms,
        ok_count=ok_count,
        parse_error_count=parse_error_count,
        missing_delta_total=missing_delta_total,
        first_seq=first_seq,
        last_seq=last_seq,
        rx_1sec_rows=aux.rx_1sec_rows,
        rx_pps_mean=aux.rx_pps_mean,
        rx_pps_max=aux.rx_pps_max,
        rx_cpu_pct_mean=aux.rx_cpu_pct_mean,
        rx_cpu_pct_max=aux.rx_cpu_pct_max,
        tx_stats_rows=aux.tx_stats_rows,
        tx_pps_mean=aux.tx_pps_mean,
        tx_pps_max=aux.tx_pps_max,
        tx_cpu_pct_mean=aux.tx_cpu_pct_mean,
        tx_cpu_pct_max=aux.tx_cpu_pct_max,
    )


def discover_runs(data_dir: Path) -> list[RunData]:
    discovered: list[RunData] = []
    run_pattern = re.compile(r"^rate_(\d+)_run([0-9]+)\.csv$")
    trial_dir_pattern = re.compile(r"^rate_(\d+)_trial([0-9]+)$")
    seen: set[tuple[int, int]] = set()

    for path in sorted(data_dir.glob("raw_logs/*/rate_*_trial*/rx_by_1recv.csv")):
        match = trial_dir_pattern.match(path.parent.name)
        if match is None:
            continue
        rate_hz = int(match.group(1))
        trial = int(match.group(2))
        key = (rate_hz, trial)
        seen.add(key)
        discovered.append(load_run(path, rate_hz, trial, data_dir))

    for path in sorted(data_dir.rglob("rate_*_run*.csv")):
        match = run_pattern.match(path.name)
        if match is None:
            continue
        rate_hz = int(match.group(1))
        trial = int(match.group(2))
        if (rate_hz, trial) in seen:
            continue
        discovered.append(load_run(path, rate_hz, trial, data_dir))

    if not discovered:
        raise CSVValidationError(f"no run CSV files found in {data_dir}")

    discovered.sort(key=lambda run: (run.rate_hz, run.trial))
    return discovered


def write_summary_csv(path: Path, runs: list[RunData]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "rate_hz",
                "trial",
                "sample_count",
                "ok_count",
                "parse_error_count",
                "missing_delta_total",
                "first_seq",
                "last_seq",
                "observed_span",
                "missing_rate",
                "parse_error_rate",
                "effective_rx_hz",
                "rx_1sec_rows",
                "rx_pps_mean",
                "rx_pps_max",
                "rx_cpu_pct_mean",
                "rx_cpu_pct_max",
                "tx_stats_rows",
                "tx_pps_mean",
                "tx_pps_max",
                "tx_cpu_pct_mean",
                "tx_cpu_pct_max",
                "mean_latency_ms",
                "p50_latency_ms",
                "p95_latency_ms",
                "p99_latency_ms",
                "max_latency_ms",
                "stddev_latency_ms",
                "last_latency_ms",
            ]
        )
        for run in runs:
            writer.writerow(
                [
                    run.rate_hz,
                    run.trial,
                    run.sample_count,
                    run.ok_count,
                    run.parse_error_count,
                    run.missing_delta_total,
                    run.first_seq,
                    run.last_seq,
                    run.observed_span,
                    f"{run.missing_rate:.8f}",
                    f"{run.parse_error_rate:.8f}",
                    f"{run.effective_rx_hz:.3f}",
                    run.rx_1sec_rows,
                    format_optional(run.rx_pps_mean, 3),
                    format_optional(run.rx_pps_max, 3),
                    format_optional(run.rx_cpu_pct_mean, 3),
                    format_optional(run.rx_cpu_pct_max, 3),
                    run.tx_stats_rows,
                    format_optional(run.tx_pps_mean, 3),
                    format_optional(run.tx_pps_max, 3),
                    format_optional(run.tx_cpu_pct_mean, 3),
                    format_optional(run.tx_cpu_pct_max, 3),
                    f"{run.mean_latency_ms:.6f}",
                    f"{run.p50_latency_ms:.6f}",
                    f"{run.p95_latency_ms:.6f}",
                    f"{run.p99_latency_ms:.6f}",
                    f"{run.max_latency_ms:.6f}",
                    f"{run.stddev_latency_ms:.6f}",
                    f"{run.last_latency_ms:.6f}",
                ]
            )


def build_report(runs: list[RunData]) -> str:
    lines: list[str] = []
    lines.append("# W08 send interval sweep summary")
    lines.append("")
    lines.append("## 結論")
    lines.append("")
    lines.append("- 50 Hz から 100,000 Hz までは欠落なしで安定している。")
    lines.append("- 120,000 Hz は欠落なしだが、tail latency の外れ値が出始めている。")
    lines.append("- 140,000 Hz 以降で `missing_delta_total` が発生し、受信側が全 frame を追えない trial が出る。")
    lines.append("- 500,000 Hz では欠落と p99 latency が明確に悪化し、今回条件では飽和側のデータとして扱う。")
    lines.append("- 1,000,000 Hz は実効受信数が期待値から大きく外れ、測定条件自体が崩れ始めている可能性が高い。")
    lines.append("")

    lines.append("## 実行コマンド")
    lines.append("")
    lines.append("```bash")
    lines.append("scripts/w08/run_send_interval_sweep.sh")
    lines.append("scripts/w08/run_send_interval_high_sweep.sh")
    lines.append("python scripts/analyze_w08_send_interval.py --data-dir data/w08/send_interval --summary-csv data/w08/send_interval/w08_send_interval_summary.csv --report reports/w08_send_interval_summary.md")
    lines.append("```")
    lines.append("")
    lines.append("## 固定条件")
    lines.append("")
    lines.append("- loopback: `127.0.0.1`")
    lines.append("- port: `9000`")
    lines.append("- payload_len: `48`")
    lines.append("- tx duration: `10 sec`")
    lines.append("- rx duration: `12 sec`")
    lines.append("- recovery_mode: `fsm`")
    lines.append("- socket buffer tuning: none")
    lines.append("- CPU affinity: none")
    lines.append("")
    lines.append("Issue 本文では `run1.csv`〜`run3.csv` を成果物としていたが、今回は send interval sweep と high-rate sweep に拡張したため、成果物パスは次の形式に拡張した。")
    lines.append("")
    lines.append("- `data/w08/send_interval/raw_logs/send_interval/rate_<hz>_trial<trial>/rx_by_1recv.csv`")
    lines.append("- `data/w08/send_interval/raw_logs/send_interval_high/rate_<hz>_trial<trial>/rx_by_1recv.csv`")
    lines.append("")
    lines.append("## rate-level aggregate: load / loss")
    lines.append("")
    lines.append(
        "| rate_hz | trials | samples(avg) | rx_hz(avg) | missing(avg) | missing_rate | parse_err | 判定 |"
    )
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")

    aggregate_rows: list[dict[str, float | int | str | None]] = []

    by_rate: dict[int, list[RunData]] = {}
    for run in runs:
        by_rate.setdefault(run.rate_hz, []).append(run)

    for rate_hz in sorted(by_rate):
        grouped = by_rate[rate_hz]
        mean_of_mean = statistics.fmean(run.mean_latency_ms for run in grouped)
        mean_p95 = statistics.fmean(run.p95_latency_ms for run in grouped)
        mean_p99 = statistics.fmean(run.p99_latency_ms for run in grouped)
        mean_max = statistics.fmean(run.max_latency_ms for run in grouped)
        mean_samples = statistics.fmean(run.sample_count for run in grouped)
        mean_missing = statistics.fmean(run.missing_delta_total for run in grouped)
        mean_missing_rate = statistics.fmean(run.missing_rate for run in grouped)
        mean_effective_rx_hz = statistics.fmean(run.effective_rx_hz for run in grouped)
        parse_errors = sum(run.parse_error_count for run in grouped)
        rx_cpu_mean_values = [run.rx_cpu_pct_mean for run in grouped if run.rx_cpu_pct_mean is not None]
        rx_cpu_max_values = [run.rx_cpu_pct_max for run in grouped if run.rx_cpu_pct_max is not None]
        tx_cpu_mean_values = [run.tx_cpu_pct_mean for run in grouped if run.tx_cpu_pct_mean is not None]
        tx_cpu_max_values = [run.tx_cpu_pct_max for run in grouped if run.tx_cpu_pct_max is not None]
        rx_cpu_mean = mean_or_none(rx_cpu_mean_values)
        rx_cpu_max = max_or_none(rx_cpu_max_values)
        tx_cpu_mean = mean_or_none(tx_cpu_mean_values)
        tx_cpu_max = max_or_none(tx_cpu_max_values)
        if mean_missing == 0 and mean_p99 < 0.02:
            judgment = "安定・欠落なし"
        elif mean_missing == 0:
            judgment = "欠落なし・tail確認"
        elif mean_missing < 1_000:
            judgment = "欠落少量"
        elif mean_missing < 20_000:
            judgment = "欠落あり"
        else:
            judgment = "飽和傾向"
        aggregate_rows.append(
            {
                "rate_hz": rate_hz,
                "trials": len(grouped),
                "mean_samples": mean_samples,
                "mean_effective_rx_hz": mean_effective_rx_hz,
                "mean_missing": mean_missing,
                "mean_missing_rate": mean_missing_rate,
                "parse_errors": parse_errors,
                "rx_cpu_mean": rx_cpu_mean,
                "rx_cpu_max": rx_cpu_max,
                "tx_cpu_mean": tx_cpu_mean,
                "tx_cpu_max": tx_cpu_max,
                "mean_of_mean": mean_of_mean,
                "mean_p95": mean_p95,
                "mean_p99": mean_p99,
                "mean_max": mean_max,
                "judgment": judgment,
            }
        )
        lines.append(
            f"| {rate_hz} | {len(grouped)} | {mean_samples:.1f} | "
            f"{mean_effective_rx_hz:.1f} | {mean_missing:.1f} | "
            f"{mean_missing_rate:.8f} | {parse_errors} | {judgment} |"
        )

    lines.append("")
    lines.append("## rate-level aggregate: CPU / latency")
    lines.append("")
    lines.append(
        "| rate_hz | rx_cpu_mean | rx_cpu_max | tx_cpu_mean | tx_cpu_max | mean_ms | p95_ms | p99_ms | max_ms |"
    )
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['rate_hz']} | {format_optional(row['rx_cpu_mean'], 3)} | "
            f"{format_optional(row['rx_cpu_max'], 3)} | "
            f"{format_optional(row['tx_cpu_mean'], 3)} | "
            f"{format_optional(row['tx_cpu_max'], 3)} | "
            f"{float(row['mean_of_mean']):.6f} | {float(row['mean_p95']):.6f} | "
            f"{float(row['mean_p99']):.6f} | {float(row['mean_max']):.6f} |"
        )

    anomaly_runs = [
        run
        for run in runs
        if run.missing_delta_total > 0 or run.parse_error_count > 0 or run.max_latency_ms >= 10.0
    ]
    lines.append("")
    lines.append("## anomaly / boundary runs")
    lines.append("")
    lines.append("全 run 表は CSV に出力し、Markdown では欠落・parse error・10 ms 以上の max latency がある run だけを載せる。")
    lines.append("")
    lines.append(
        "| rate_hz | trial | sample_count | effective_rx_hz | missing_delta_total | missing_rate | parse_errors | max_latency_ms | last_latency_ms |"
    )
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for run in anomaly_runs:
        lines.append(
            f"| {run.rate_hz} | {run.trial} | {run.sample_count} | {run.effective_rx_hz:.1f} | "
            f"{run.missing_delta_total} | {run.missing_rate:.8f} | {run.parse_error_count} | "
            f"{run.max_latency_ms:.6f} | {run.last_latency_ms:.6f} |"
        )

    lines.append("")
    lines.append("## raw data / generated files")
    lines.append("")
    lines.append("- 1recv ごとの生データ、1秒窓の受信データ、tx/rx log: `data/w08/send_interval/raw_logs/`")
    lines.append("- run-level の全指標: `data/w08/send_interval/w08_send_interval_summary.csv`")
    lines.append("- Markdown では同じ表の重複を避け、rate-level aggregate と anomaly / boundary runs に絞る。")
    lines.append("")
    lines.append("## 指標メモ")
    lines.append("")
    lines.append("- `sample_count`: CSV に記録された受信 row 数。")
    lines.append("- `effective_rx_hz`: `sample_count / 10 sec`。今回の tx duration は 10 秒。")
    lines.append("- `missing_delta_total`: CSV 内で観測された seq gap の合計。高 rate での欠落・取りこぼしを見る。")
    lines.append("- `missing_rate`: `missing_delta_total / (last_seq + 1)`。")
    lines.append("- `parse_errors`: `parse_status != OK` の合計。")
    lines.append("- `rx_cpu_*`: `rx_1sec.csv` の `cpu_pct`。1秒窓の受信 process CPU 使用率。")
    lines.append("- `tx_cpu_*`: `tx.log` の `tx_stats ... cpu_pct`。1秒窓の送信 process CPU 使用率。")
    lines.append("- latency 系指標は `parse_status=OK` の row から計算する。")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    data_dir = Path(args.data_dir)
    runs = discover_runs(data_dir)

    observed_rates = sorted({run.rate_hz for run in runs})
    trial_counts = {
        rate: sorted(run.trial for run in runs if run.rate_hz == rate)
        for rate in observed_rates
    }
    for rate, trials in trial_counts.items():
        if tuple(trials) != EXPECTED_TRIALS:
            raise CSVValidationError(
                f"rate {rate}: unexpected trial set {trials}; expected {list(EXPECTED_TRIALS)}"
            )

    summary_csv = Path(args.summary_csv)
    report = Path(args.report)
    write_summary_csv(summary_csv, runs)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(build_report(runs), encoding="utf-8")

    print(f"OK: analyzed {len(runs)} runs")
    print(f"wrote: {summary_csv}")
    print(f"wrote: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
