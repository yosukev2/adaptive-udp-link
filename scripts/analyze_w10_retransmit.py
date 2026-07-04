#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

KEY_VALUE_RE = re.compile(r"([A-Za-z0-9_]+)=([^\s]+)")


def parse_key_values(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in KEY_VALUE_RE.findall(text):
        out[key] = value
    return out


def parse_log(path: Path, marker: str) -> dict[str, str]:
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if marker in line:
            result.update(parse_key_values(line))
    return result


def pct(value: float) -> str:
    return f"{value * 100:.4f}%"


def to_int(row: dict[str, str], key: str) -> int:
    try:
        return int(float(row.get(key, "0")))
    except ValueError:
        return 0


def to_float(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "0"))
    except ValueError:
        return 0.0


def collect(log_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for run_dir in sorted(log_dir.glob("*_trial*")):
        m = re.match(r"(off|on)_trial(\d+)$", run_dir.name)
        if not m:
            continue
        mode = m.group(1)
        trial = int(m.group(2))
        rx = parse_log(run_dir / "rx.log", "rx summary")
        tx = parse_log(run_dir / "tx.log", "tx summary")
        row: dict[str, str] = {"mode": mode, "trial": str(trial), "run_dir": str(run_dir)}
        row.update({f"rx_{k}": v for k, v in rx.items()})
        row.update({f"tx_{k}": v for k, v in tx.items()})

        recv_ok = to_int(row, "rx_recv_ok")
        gap = to_int(row, "rx_gap_cnt")
        recovered = to_int(row, "rx_recovered_by_retransmit_count")
        effective_missing = max(0, gap - recovered)
        unique = to_int(row, "rx_unique_received_frames_total") or recv_ok
        expected_before = recv_ok + gap
        expected_after = unique + effective_missing
        row["missing_before_retransmit_total"] = str(gap)
        row["effective_missing_total"] = str(effective_missing)
        row["received_frames_total"] = str(recv_ok)
        row["final_delivered_frames_total"] = str(unique)
        row["raw_missing_rate"] = f"{(gap / expected_before) if expected_before else 0.0:.9f}"
        row["effective_missing_rate"] = f"{(effective_missing / expected_after) if expected_after else 0.0:.9f}"
        row["delivered_rate"] = f"{(unique / expected_after) if expected_after else 0.0:.9f}"
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str]], out: Path) -> None:
    fields = [
        "mode", "trial", "received_frames_total", "final_delivered_frames_total",
        "missing_before_retransmit_total", "rx_recovered_by_retransmit_count",
        "effective_missing_total", "raw_missing_rate", "effective_missing_rate", "delivered_rate",
        "rx_duplicate_frames_total", "rx_reord_cnt", "rx_avg_latency_ms", "rx_max_latency_ms",
        "tx_retransmit_requested_frames", "tx_retransmit_sent_datagrams", "tx_retransmit_sent_frames",
        "tx_retransmit_buffer_miss_count", "run_dir",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def summarize(rows: list[dict[str, str]], report: Path, summary_csv: Path) -> None:
    report.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# W10 retransmit comparison summary")
    lines.append("")
    lines.append("## 集計")
    lines.append("")
    lines.append("| mode | trials | received frames | final delivered frames | raw missing | recovered | effective missing | raw missing rate | effective missing rate | retransmit sent frames | buffer miss |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for mode in ["off", "on"]:
        rs = [row for row in rows if row["mode"] == mode]
        recv = sum(to_int(row, "received_frames_total") for row in rs)
        delivered = sum(to_int(row, "final_delivered_frames_total") for row in rs)
        raw_missing = sum(to_int(row, "missing_before_retransmit_total") for row in rs)
        recovered = sum(to_int(row, "rx_recovered_by_retransmit_count") for row in rs)
        effective = sum(to_int(row, "effective_missing_total") for row in rs)
        rtx_sent = sum(to_int(row, "tx_retransmit_sent_frames") for row in rs)
        buffer_miss = sum(to_int(row, "tx_retransmit_buffer_miss_count") for row in rs)
        raw_denom = recv + raw_missing
        eff_denom = delivered + effective
        lines.append(
            f"| {mode} | {len(rs)} | {recv} | {delivered} | {raw_missing} | {recovered} | {effective} | "
            f"{pct(raw_missing / raw_denom if raw_denom else 0.0)} | "
            f"{pct(effective / eff_denom if eff_denom else 0.0)} | {rtx_sent} | {buffer_miss} |"
        )
    lines.append("")
    lines.append("## run別")
    lines.append("")
    lines.append("| mode | trial | received | delivered | raw missing | recovered | effective missing | raw missing rate | effective missing rate | rtx sent frames | buffer miss |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in sorted(rows, key=lambda r: (r["mode"], int(r["trial"]))):
        lines.append(
            f"| {row['mode']} | {row['trial']} | {row.get('received_frames_total','')} | {row.get('final_delivered_frames_total','')} | "
            f"{row.get('missing_before_retransmit_total','')} | {row.get('rx_recovered_by_retransmit_count','')} | {row.get('effective_missing_total','')} | "
            f"{pct(to_float(row, 'raw_missing_rate'))} | {pct(to_float(row, 'effective_missing_rate'))} | "
            f"{row.get('tx_retransmit_sent_frames','')} | {row.get('tx_retransmit_buffer_miss_count','')} |"
        )
    lines.append("")
    lines.append("## 生成物")
    lines.append("")
    lines.append(f"- summary CSV: `{summary_csv}`")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", default="logs/w10/retransmit")
    parser.add_argument("--summary-csv", default="reports/w10_retransmit_comparison.csv")
    parser.add_argument("--report", default="reports/w10_retransmit_summary.md")
    args = parser.parse_args()

    rows = collect(Path(args.log_dir))
    if not rows:
        raise SystemExit(f"no run logs found under {args.log_dir}")
    summary_csv = Path(args.summary_csv)
    report = Path(args.report)
    write_csv(rows, summary_csv)
    summarize(rows, report, summary_csv)
    print(report)
    print(summary_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
