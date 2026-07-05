#!/usr/bin/env python3
import argparse
import csv
import math
import re
import statistics
from pathlib import Path

KEY_VALUE_RE = re.compile(r"([A-Za-z0-9_]+)=([^\s]+)")


def pct(value: float) -> str:
    return f"{value * 100:.4f}%"


def parse_key_values(text: str) -> dict[str, str]:
    return {key: value for key, value in KEY_VALUE_RE.findall(text)}


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


def parse_log(path: Path, marker: str) -> dict[str, object]:
    result: dict[str, object] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if marker in line:
            result.update(parse_key_values(line))
    return result


def parse_adaptive(path: Path) -> dict[str, object]:
    requested = 0
    sent_datagrams = 0
    buffer_miss = 0
    rows = 0
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            rows += 1
            requested += int(float(row.get("retransmit_count") or 0))
            sent_datagrams += int(float(row.get("retransmit_sent_datagrams") or 0))
            buffer_miss += int(float(row.get("retransmit_buffer_miss") or 0))
    return {
        "feedback_rows": rows,
        "retransmit_requested_frames": requested,
        "retransmit_sent_datagrams": sent_datagrams,
        "retransmit_sent_frames": sent_datagrams * 3,
        "retransmit_buffer_miss_count": buffer_miss,
    }


def parse_rx_1sec(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    rows: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        rows.extend(csv.DictReader(f))
    recv = sum(int(r["ok_recv_cnt"]) for r in rows)
    gap = sum(int(r["gap_cnt"]) for r in rows)
    avg_latency = sum(float(r["avg_latency_ms"]) * int(r["ok_recv_cnt"]) for r in rows) / recv if recv else 0.0
    max_latency = max((float(r["max_latency_ms"]) for r in rows), default=0.0)
    avg_cpu = statistics.mean(float(r["cpu_pct"]) for r in rows) if rows else 0.0
    return {
        "rx_1sec_recv_ok": recv,
        "rx_1sec_gap_cnt": gap,
        "avg_latency_ms": avg_latency,
        "max_latency_ms": max_latency,
        "avg_cpu_pct": avg_cpu,
    }


def parse_rx_by_recv(path: Path) -> dict[str, object]:
    bits = bytearray()
    highest: int | None = None
    received = 0
    unique = 0
    duplicate = 0
    recovered = 0
    missing = 0
    latency_sum = 0.0
    max_latency = 0.0
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row.get("parse_status") != "OK":
                continue
            seq = int(row["seq"])
            lat = int(row["latency_ns"]) / 1_000_000.0
            received += 1
            missing += int(row["missing_delta"])
            latency_sum += lat
            max_latency = max(max_latency, lat)
            need = seq // 8 + 1
            if need > len(bits):
                bits.extend(b"\x00" * (need - len(bits)))
            mask = 1 << (seq % 8)
            seen = (bits[seq // 8] & mask) != 0
            if seen:
                duplicate += 1
                continue
            if highest is not None and seq < highest:
                recovered += 1
            bits[seq // 8] |= mask
            unique += 1
            if highest is None or seq > highest:
                highest = seq
    effective = max(0, missing - recovered)
    raw_denom = received + missing
    eff_denom = unique + effective
    return {
        "received_frames_total": received,
        "unique_received_frames_total": unique,
        "duplicate_frames_total": duplicate,
        "missing_before_retransmit_total": missing,
        "recovered_by_retransmit_count": recovered,
        "effective_missing_total": effective,
        "raw_missing_rate": missing / raw_denom if raw_denom else 0.0,
        "effective_missing_rate": effective / eff_denom if eff_denom else 0.0,
        "delivered_rate": unique / eff_denom if eff_denom else 0.0,
        "raw_avg_latency_ms": latency_sum / received if received else 0.0,
        "raw_max_latency_ms": max_latency,
    }


def collect_from_data(data_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    paths = sorted(
        data_dir.glob("*_rx_by_1recv.csv"),
        key=lambda p: (p.name.split("_")[0], int(re.search(r"run(\d+)", p.name).group(1))),
    )
    for path in paths:
        match = re.match(r"(off|on)_run(\d+)_rx_by_1recv\.csv", path.name)
        if not match:
            continue
        mode = match.group(1)
        trial = int(match.group(2))
        row: dict[str, object] = {"mode": mode, "trial": trial}
        row.update(parse_rx_by_recv(path))
        row.update(parse_rx_1sec(data_dir / f"{mode}_run{trial}_rx_1sec.csv"))
        row.update(parse_adaptive(data_dir / f"{mode}_run{trial}_adaptive_log.csv"))
        rows.append(row)
    return rows


def collect_from_logs(log_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for run_dir in sorted(log_dir.glob("*_trial*")):
        match = re.match(r"(off|on)_trial(\d+)$", run_dir.name)
        if not match:
            continue
        mode = match.group(1)
        trial = int(match.group(2))
        rx = {f"rx_{k}": v for k, v in parse_log(run_dir / "rx.log", "rx summary").items()}
        tx = {f"tx_{k}": v for k, v in parse_log(run_dir / "tx.log", "tx summary").items()}
        row: dict[str, object] = {"mode": mode, "trial": trial, **rx, **tx}
        recv = to_int(row, "rx_recv_ok")
        gap = to_int(row, "rx_gap_cnt")
        recovered = to_int(row, "rx_recovered_by_retransmit_count")
        effective = max(0, gap - recovered)
        unique = to_int(row, "rx_unique_received_frames_total") or recv
        row.update({
            "received_frames_total": recv,
            "unique_received_frames_total": unique,
            "duplicate_frames_total": to_int(row, "rx_duplicate_frames_total"),
            "missing_before_retransmit_total": gap,
            "recovered_by_retransmit_count": recovered,
            "effective_missing_total": effective,
            "raw_missing_rate": gap / (recv + gap) if recv + gap else 0.0,
            "effective_missing_rate": effective / (unique + effective) if unique + effective else 0.0,
            "delivered_rate": unique / (unique + effective) if unique + effective else 0.0,
            "raw_avg_latency_ms": to_float(row, "rx_avg_latency_ms"),
            "raw_max_latency_ms": to_float(row, "rx_max_latency_ms"),
            "avg_cpu_pct": 0.0,
            "retransmit_requested_frames": to_int(row, "tx_retransmit_requested_frames"),
            "retransmit_sent_datagrams": to_int(row, "tx_retransmit_sent_datagrams"),
            "retransmit_sent_frames": to_int(row, "tx_retransmit_sent_frames"),
            "retransmit_buffer_miss_count": to_int(row, "tx_retransmit_buffer_miss_count"),
        })
        rows.append(row)
    return rows


def aggregate(rows: list[dict[str, object]], mode: str) -> dict[str, object]:
    rs = [r for r in rows if r["mode"] == mode]
    def s(key: str) -> int:
        return sum(to_int(r, key) for r in rs)
    result: dict[str, object] = {
        "trials": len(rs),
        "received": s("received_frames_total"),
        "unique": s("unique_received_frames_total"),
        "missing": s("missing_before_retransmit_total"),
        "recovered": s("recovered_by_retransmit_count"),
        "effective": s("effective_missing_total"),
        "duplicate": s("duplicate_frames_total"),
        "rtx_requested": s("retransmit_requested_frames"),
        "rtx_sent_frames": s("retransmit_sent_frames"),
        "rtx_sent_datagrams": s("retransmit_sent_datagrams"),
        "buffer_miss": s("retransmit_buffer_miss_count"),
        "avg_latency": statistics.mean(to_float(r, "raw_avg_latency_ms") for r in rs) if rs else 0.0,
        "max_latency": max((to_float(r, "raw_max_latency_ms") for r in rs), default=0.0),
        "avg_cpu": statistics.mean(to_float(r, "avg_cpu_pct") for r in rs) if rs else 0.0,
    }
    result["raw_rate"] = result["missing"] / (result["received"] + result["missing"]) if result["received"] + result["missing"] else 0.0
    result["eff_rate"] = result["effective"] / (result["unique"] + result["effective"]) if result["unique"] + result["effective"] else 0.0
    result["delivered_rate"] = result["unique"] / (result["unique"] + result["effective"]) if result["unique"] + result["effective"] else 0.0
    return result


def write_csv(rows: list[dict[str, object]], out: Path) -> None:
    fields = [
        "mode", "trial", "received_frames_total", "unique_received_frames_total",
        "duplicate_frames_total", "missing_before_retransmit_total", "recovered_by_retransmit_count",
        "effective_missing_total", "raw_missing_rate", "effective_missing_rate", "delivered_rate",
        "raw_avg_latency_ms", "raw_max_latency_ms", "avg_latency_ms", "max_latency_ms", "avg_cpu_pct",
        "feedback_rows", "retransmit_requested_frames", "retransmit_sent_datagrams",
        "retransmit_sent_frames", "retransmit_buffer_miss_count",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_report(rows: list[dict[str, object]], report: Path, summary_csv: Path, data_dir: Path | None) -> None:
    off = aggregate(rows, "off")
    on = aggregate(rows, "on")
    reduction = (off["effective"] - on["effective"]) / off["effective"] if off["effective"] else 0.0
    lines: list[str] = []
    lines += ["# W09 retransmit comparison summary", ""]
    if data_dir and (data_dir / "run_metadata.md").exists():
        lines += ["## 実験条件", ""]
        for line in (data_dir / "run_metadata.md").read_text(encoding="utf-8", errors="replace").splitlines()[:20]:
            if line.startswith("- "):
                lines.append(line)
        lines.append("")
    lines += ["## 結論", ""]
    lines += [
        f"- retransmit ON は effective_missing_total を OFF {off['effective']:,} から ON {on['effective']:,} に減らした。削減率は {pct(reduction)}。",
        f"- raw missing rate は OFF {pct(off['raw_rate'])}、ON {pct(on['raw_rate'])}。今回のrunではON側の再送前missingも小さいため、effective_missing改善の全てを再送だけの効果とは断定しない。",
        f"- effective missing rate は OFF {pct(off['eff_rate'])}、ON {pct(on['eff_rate'])}。",
        f"- ONでは {on['rtx_sent_frames']:,} frames を再送し、{on['recovered']:,} frames が後着受信として回復した。",
        f"- buffer miss は ON {on['buffer_miss']}。今回のbuffer設定では再送buffer不足はほぼ観測されていない。",
        f"- latencyは再送ONで大きく悪化した。平均latencyは OFF {off['avg_latency']:.3f} ms、ON {on['avg_latency']:.3f} ms。再送フレームは元のtx timestampを持つため、回復できた分だけ古いデータのlatencyが大きく出る。",
        "",
    ]
    lines += ["## 集計比較", ""]
    lines += ["| mode | trials | received | unique delivered | raw missing | recovered | effective missing | raw missing rate | effective missing rate | retransmit sent frames | buffer miss | avg latency ms | max latency ms | avg cpu pct |"]
    lines += ["|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for mode, agg in [("off", off), ("on", on)]:
        lines.append(
            f"| {mode} | {agg['trials']} | {agg['received']:,} | {agg['unique']:,} | {agg['missing']:,} | {agg['recovered']:,} | {agg['effective']:,} | "
            f"{pct(agg['raw_rate'])} | {pct(agg['eff_rate'])} | {agg['rtx_sent_frames']:,} | {agg['buffer_miss']} | {agg['avg_latency']:.3f} | {agg['max_latency']:.3f} | {agg['avg_cpu']:.2f} |"
        )
    lines += ["", "## run別詳細", ""]
    lines += ["| mode | trial | received | unique | raw missing | recovered | effective missing | raw missing rate | effective missing rate | rtx sent frames | buffer miss | avg latency ms | max latency ms |"]
    lines += ["|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        lines.append(
            f"| {row['mode']} | {row['trial']} | {to_int(row,'received_frames_total'):,} | {to_int(row,'unique_received_frames_total'):,} | "
            f"{to_int(row,'missing_before_retransmit_total'):,} | {to_int(row,'recovered_by_retransmit_count'):,} | {to_int(row,'effective_missing_total'):,} | "
            f"{pct(to_float(row,'raw_missing_rate'))} | {pct(to_float(row,'effective_missing_rate'))} | {to_int(row,'retransmit_sent_frames'):,} | {to_int(row,'retransmit_buffer_miss_count')} | "
            f"{to_float(row,'raw_avg_latency_ms'):.3f} | {to_float(row,'raw_max_latency_ms'):.3f} |"
        )
    lines += ["", "## 生成物", "", f"- summary CSV: `{summary_csv}`", f"- report: `{report}`", ""]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--log-dir", default=None)
    parser.add_argument("--summary-csv", default="reports/w09_retransmit_comparison.csv")
    parser.add_argument("--report", default="reports/w09_retransmit_summary.md")
    args = parser.parse_args()

    data_dir = Path(args.data_dir) if args.data_dir else None
    if data_dir:
        rows = collect_from_data(data_dir)
    elif args.log_dir:
        rows = collect_from_logs(Path(args.log_dir))
    else:
        rows = collect_from_data(Path("data/w09/retransmit"))
        data_dir = Path("data/w09/retransmit")
        if not rows:
            rows = collect_from_data(Path("data/retransmit"))
            data_dir = Path("data/retransmit")
        if not rows:
            rows = collect_from_logs(Path("logs/w09/retransmit"))
            data_dir = None
    if not rows:
        raise SystemExit("no retransmit run data found")
    summary_csv = Path(args.summary_csv)
    report = Path(args.report)
    write_csv(rows, summary_csv)
    write_report(rows, report, summary_csv, data_dir)
    print(report)
    print(summary_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
