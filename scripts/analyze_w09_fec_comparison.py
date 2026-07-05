#!/usr/bin/env python3
import argparse
import csv
import re
import statistics
from pathlib import Path

KEY_VALUE_RE = re.compile(r"([A-Za-z0-9_]+)=([^\s]+)")


def parse_key_values(text: str) -> dict[str, str]:
    return {key: value for key, value in KEY_VALUE_RE.findall(text)}


def pct(value: float) -> str:
    return f"{value * 100:.4f}%"


def to_int(row: dict[str, object], key: str) -> int:
    try:
        return int(float(row.get(key, 0) or 0))
    except (TypeError, ValueError):
        return 0


def to_float(row: dict[str, object], key: str) -> float:
    try:
        return float(row.get(key, 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def parse_log(path: Path, marker: str) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if marker in line:
            result.update(parse_key_values(line))
    return result


def parse_rx_1sec(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        rows.extend(csv.DictReader(f))
    if not rows:
        return {}
    recv = sum(int(float(r.get("ok_recv_cnt") or 0)) for r in rows)
    avg_latency = (
        sum(float(r.get("avg_latency_ms") or 0) * int(float(r.get("ok_recv_cnt") or 0)) for r in rows) / recv
        if recv else 0.0
    )
    return {
        "rx_1sec_rows": len(rows),
        "rx_1sec_recv_ok": recv,
        "rx_1sec_gap_cnt": sum(int(float(r.get("gap_cnt") or 0)) for r in rows),
        "rx_1sec_avg_latency_ms": avg_latency,
        "rx_1sec_max_latency_ms": max(float(r.get("max_latency_ms") or 0) for r in rows),
        "rx_1sec_avg_cpu_pct": statistics.mean(float(r.get("cpu_pct") or 0) for r in rows),
    }


def discover_runs(log_dir: Path) -> list[tuple[str, int, Path]]:
    runs: list[tuple[str, int, Path]] = []
    for run_dir in sorted(log_dir.glob("fec_*_trial*")):
        match = re.match(r"fec_(off|xor)_trial(\d+)$", run_dir.name)
        if match:
            runs.append((match.group(1), int(match.group(2)), run_dir))
    return runs


def collect(log_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for fec_mode, trial, run_dir in discover_runs(log_dir):
        rx = parse_log(run_dir / "rx.log", "rx summary")
        tx = parse_log(run_dir / "tx.log", "tx summary")
        trial_summary = parse_log(run_dir / "rx.log", "trial_summary")
        row: dict[str, object] = {
            "trial": trial,
            "fec_mode": fec_mode,
            "drop_rate": "",
            "drop_seed": "",
            "run_dir": str(run_dir),
        }
        row.update({f"rx_{k}": v for k, v in rx.items()})
        row.update({f"tx_{k}": v for k, v in tx.items()})
        row.update({f"trial_{k}": v for k, v in trial_summary.items()})
        row.update(parse_rx_1sec(run_dir / "rx_1sec.csv"))

        # tx summary の dropped_* はrandom_drop適用後の実測値。
        raw_missing_total = to_int(row, "rx_fec_raw_missing_frames") if fec_mode == "xor" else to_int(row, "rx_gap_cnt")
        recovered_count = to_int(row, "rx_recovered_by_fec_count") if fec_mode == "xor" else 0
        unrecovered_count = to_int(row, "rx_unrecovered_by_fec_count") if fec_mode == "xor" else raw_missing_total
        effective_missing_total = (
            to_int(row, "rx_fec_effective_missing_total")
            if fec_mode == "xor"
            else to_int(row, "rx_effective_missing_total")
        )
        unique_received_frames = to_int(row, "rx_unique_received_frames_total") or to_int(row, "rx_recv_ok")
        usable_datagrams = unique_received_frames // 3
        total_datagrams_after_effective_loss = (unique_received_frames + effective_missing_total) // 3
        effective_missing_rate = (
            effective_missing_total / (unique_received_frames + effective_missing_total)
            if (unique_received_frames + effective_missing_total) else 0.0
        )
        raw_missing_rate = (
            raw_missing_total / (unique_received_frames + raw_missing_total)
            if (unique_received_frames + raw_missing_total) else 0.0
        )

        row.update({
            "raw_missing_total": raw_missing_total,
            "recovered_count": recovered_count,
            "unrecovered_count": unrecovered_count,
            "effective_missing_total": effective_missing_total,
            "effective_missing_rate": effective_missing_rate,
            "raw_missing_rate": raw_missing_rate,
            "unique_received_frames_total": unique_received_frames,
            "usable_datagrams": usable_datagrams,
            "total_datagrams_after_effective_loss": total_datagrams_after_effective_loss,
            "usable_datagram_rate": (
                usable_datagrams / total_datagrams_after_effective_loss
                if total_datagrams_after_effective_loss else 0.0
            ),
            "p99_latency_ms": to_float(row, "trial_latency_p99_ms"),
            "avg_latency_ms": to_float(row, "rx_avg_latency_ms"),
            "max_latency_ms": to_float(row, "rx_max_latency_ms"),
            "dropped_datagrams": to_int(row, "tx_dropped_datagrams"),
            "dropped_frames": to_int(row, "tx_dropped_frames"),
            "fec_recovered_datagrams": to_int(row, "rx_fec_recovered_datagrams"),
            "fec_unrecovered_datagrams": to_int(row, "rx_fec_unrecovered_datagrams"),
            "fec_parity_datagrams": to_int(row, "tx_fec_parity_datagrams"),
            "fec_data_datagrams": to_int(row, "tx_fec_data_datagrams"),
            "tx_sent_datagrams": to_int(row, "tx_sent"),
            "rx_status": 0 if (run_dir / "rx.log").exists() else 1,
            "tx_status": 0 if (run_dir / "tx.log").exists() else 1,
        })
        rows.append(row)
    return sorted(rows, key=lambda r: (str(r["fec_mode"]), int(r["trial"])))


def add_metadata(rows: list[dict[str, object]], metadata_path: Path) -> None:
    if not metadata_path.exists():
        return
    text = metadata_path.read_text(encoding="utf-8", errors="replace")
    meta = parse_key_values(text.replace(": ", "="))
    drop_rate = meta.get("drop_rate", "")
    rate_hz = meta.get("rate_hz", "")
    tx_duration = meta.get("tx_duration_sec", "")
    rx_duration = meta.get("rx_duration_sec", "")
    seeds = re.search(r"- drop_seeds: (.+)", text)
    seed_list = seeds.group(1).split() if seeds else []
    for row in rows:
        row["drop_rate"] = drop_rate
        row["rate_hz"] = rate_hz
        row["tx_duration_sec"] = tx_duration
        row["rx_duration_sec"] = rx_duration
        trial = int(row["trial"])
        if 1 <= trial <= len(seed_list):
            row["drop_seed"] = seed_list[trial - 1]


def aggregate(rows: list[dict[str, object]], fec_mode: str) -> dict[str, object]:
    selected = [r for r in rows if r["fec_mode"] == fec_mode]

    def s(key: str) -> int:
        return sum(to_int(r, key) for r in selected)

    unique = s("unique_received_frames_total")
    effective = s("effective_missing_total")
    raw = s("raw_missing_total")
    total_datagrams = (unique + effective) // 3
    usable_datagrams = unique // 3
    return {
        "fec_mode": fec_mode,
        "trials": len(selected),
        "unique_received_frames_total": unique,
        "usable_datagrams": usable_datagrams,
        "total_datagrams_after_effective_loss": total_datagrams,
        "raw_missing_total": raw,
        "recovered_count": s("recovered_count"),
        "unrecovered_count": s("unrecovered_count"),
        "effective_missing_total": effective,
        "raw_missing_rate": raw / (unique + raw) if unique + raw else 0.0,
        "effective_missing_rate": effective / (unique + effective) if unique + effective else 0.0,
        "usable_datagram_rate": usable_datagrams / total_datagrams if total_datagrams else 0.0,
        "fec_recovered_datagrams": s("fec_recovered_datagrams"),
        "fec_unrecovered_datagrams": s("fec_unrecovered_datagrams"),
        "dropped_datagrams": s("dropped_datagrams"),
        "dropped_frames": s("dropped_frames"),
        "avg_latency_ms": statistics.mean(to_float(r, "avg_latency_ms") for r in selected) if selected else 0.0,
        "p99_latency_ms": statistics.mean(to_float(r, "p99_latency_ms") for r in selected) if selected else 0.0,
        "max_latency_ms": max((to_float(r, "max_latency_ms") for r in selected), default=0.0),
        "avg_cpu_pct": statistics.mean(to_float(r, "rx_1sec_avg_cpu_pct") for r in selected) if selected else 0.0,
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    fields = [
        "trial",
        "drop_rate",
        "drop_seed",
        "rate_hz",
        "fec_mode",
        "tx_status",
        "rx_status",
        "tx_sent_datagrams",
        "dropped_datagrams",
        "dropped_frames",
        "fec_data_datagrams",
        "fec_parity_datagrams",
        "raw_missing_total",
        "recovered_count",
        "unrecovered_count",
        "effective_missing_total",
        "raw_missing_rate",
        "effective_missing_rate",
        "unique_received_frames_total",
        "usable_datagrams",
        "total_datagrams_after_effective_loss",
        "usable_datagram_rate",
        "fec_recovered_datagrams",
        "fec_unrecovered_datagrams",
        "avg_latency_ms",
        "p99_latency_ms",
        "max_latency_ms",
        "rx_1sec_avg_cpu_pct",
        "run_dir",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_report(rows: list[dict[str, object]], report: Path, summary_csv: Path, log_dir: Path, metadata_path: Path) -> None:
    off = aggregate(rows, "off")
    xor = aggregate(rows, "xor")
    eff_reduction = (
        (off["effective_missing_total"] - xor["effective_missing_total"]) / off["effective_missing_total"]
        if off["effective_missing_total"] else 0.0
    )
    usable_gain = int(xor["usable_datagrams"]) - int(off["usable_datagrams"])

    lines: list[str] = ["# W09 random_drop + XOR FEC比較 summary", ""]
    if metadata_path.exists():
        lines += ["## 実験条件", ""]
        for line in metadata_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("## fec_mode="):
                break
            if line.startswith("- "):
                lines.append(line)
        lines.append("")

    lines += [
        "## 結論",
        "",
        f"- FEC ON(xor) は effective_missing_total を OFF {off['effective_missing_total']:,} から ON {xor['effective_missing_total']:,} にした。削減率は {pct(eff_reduction)}。",
        f"- 結果的に使えるdatagram数は OFF {off['usable_datagrams']:,}、ON {xor['usable_datagrams']:,}。差分は ON-OFF = {usable_gain:+,} datagrams。",
        f"- raw_missing_total は送信経路で落ちた/欠落した元のmissing量、effective_missing_total はFEC回復後に残ったmissing量として扱う。",
        f"- FEC ONで recovered_count={xor['recovered_count']:,} frames、fec_recovered_datagrams={xor['fec_recovered_datagrams']:,} datagrams を回復した。",
    ]
    if xor["unrecovered_count"]:
        lines.append(
            f"- FEC ONでも unrecovered_count={xor['unrecovered_count']:,} frames が残った。XOR k=4,r=1 は1 block内で複数data datagramが欠ける、またはparity datagramが欠ける条件では回復できない。"
        )
    else:
        lines.append("- FEC ONで未回復missingは観測されていない。")

    lines += [
        "",
        "## 集計比較",
        "",
        "| fec_mode | trials | usable datagrams | usable datagram rate | raw missing | recovered frames | unrecovered frames | effective missing | raw missing rate | effective missing rate | avg p99 latency ms | max latency ms | avg cpu pct |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for agg in [off, xor]:
        lines.append(
            f"| {agg['fec_mode']} | {agg['trials']} | {agg['usable_datagrams']:,} | {pct(agg['usable_datagram_rate'])} | "
            f"{agg['raw_missing_total']:,} | {agg['recovered_count']:,} | {agg['unrecovered_count']:,} | {agg['effective_missing_total']:,} | "
            f"{pct(agg['raw_missing_rate'])} | {pct(agg['effective_missing_rate'])} | {agg['p99_latency_ms']:.3f} | {agg['max_latency_ms']:.3f} | {agg['avg_cpu_pct']:.3f} |"
        )

    lines += [
        "",
        "## run別結果",
        "",
        "| trial | seed | fec_mode | usable datagrams | raw missing | recovered | unrecovered | effective missing | effective missing rate | p99 latency ms | max latency ms | dropped datagrams |",
        "|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(rows, key=lambda r: (int(r["trial"]), str(r["fec_mode"]))):
        lines.append(
            f"| {row['trial']} | {row.get('drop_seed', '')} | {row['fec_mode']} | {to_int(row, 'usable_datagrams'):,} | "
            f"{to_int(row, 'raw_missing_total'):,} | {to_int(row, 'recovered_count'):,} | {to_int(row, 'unrecovered_count'):,} | "
            f"{to_int(row, 'effective_missing_total'):,} | {pct(to_float(row, 'effective_missing_rate'))} | "
            f"{to_float(row, 'p99_latency_ms'):.3f} | {to_float(row, 'max_latency_ms'):.3f} | {to_int(row, 'dropped_datagrams'):,} |"
        )

    lines += [
        "",
        "## 生成物",
        "",
        f"- summary CSV: `{summary_csv}`",
        f"- report: `{report}`",
        f"- logs: `{log_dir}`",
        "",
    ]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-dir", default="logs/w09/fec_comparison")
    parser.add_argument("--metadata", default="data/w09/fec_comparison/run_metadata.md")
    parser.add_argument("--summary-csv", default="data/w09/fec_comparison/fec_comparison.csv")
    parser.add_argument("--report", default="reports/w09_fec_comparison_summary.md")
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    rows = collect(log_dir)
    if not rows:
        raise SystemExit(f"no runs found under {log_dir}")
    metadata_path = Path(args.metadata)
    add_metadata(rows, metadata_path)

    summary_csv = Path(args.summary_csv)
    report = Path(args.report)
    write_csv(rows, summary_csv)
    write_report(rows, report, summary_csv, log_dir, metadata_path)
    print(report)
    print(summary_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
