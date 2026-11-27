#!/usr/bin/env python3
"""
map_controls.py
Maps NIST SP 800-53 sample controls to evidence and produces a status report.
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path

# Paths relative to project root
ROOT = Path(__file__).resolve().parent.parent
CONTROLS_FILE = ROOT / "data" / "controls_sample.json"
EVIDENCE_FILE = ROOT / "data" / "sample_evidence.csv"
OUTPUT_DIR = ROOT / "output"
FRESHNESS_DAYS = 90  # Evidence older than this is considered stale


def load_controls():
    with open(CONTROLS_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_evidence():
    evidence = {}
    with open(EVIDENCE_FILE, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            evidence[row["control_id"]] = {
                "evidence_file": row["evidence_file"],
                "collected_date": row["collected_date"],
                "notes": row["notes"],
            }
    return evidence


def determine_status(control_id: str, evidence: dict) -> tuple[str, str]:
    """Return (status, reason) for a control."""
    if control_id not in evidence:
        return "Not Implemented", "No evidence mapped"

    rec = evidence[control_id]
    collected = datetime.strptime(rec["collected_date"], "%Y-%m-%d")
    age_days = (datetime.now() - collected).days

    # Simple heuristics for the demo
    if control_id == "IA-2" and "mfa" in rec["evidence_file"].lower():
        # Treat as partial if we only have a sample MFA file
        if age_days > FRESHNESS_DAYS:
            return "Stale", f"Evidence is {age_days} days old (threshold {FRESHNESS_DAYS})"
        return "Partial", "MFA evidence present but coverage incomplete in sample"

    if age_days > FRESHNESS_DAYS:
        return "Stale", f"Evidence is {age_days} days old (threshold {FRESHNESS_DAYS})"

    return "Implemented", "Evidence present and within freshness window"


def generate_report():
    controls = load_controls()
    evidence = load_evidence()

    OUTPUT_DIR.mkdir(exist_ok=True)

    rows = []
    for ctrl in controls:
        cid = ctrl["id"]
        status, reason = determine_status(cid, evidence)
        ev = evidence.get(cid, {})
        rows.append({
            "control_id": cid,
            "title": ctrl["title"],
            "family": ctrl["family"],
            "status": status,
            "evidence_file": ev.get("evidence_file", ""),
            "collected_date": ev.get("collected_date", ""),
            "notes": ev.get("notes", ""),
            "reason": reason,
        })

    # CSV output
    csv_path = OUTPUT_DIR / "control_status.csv"
    fieldnames = ["control_id", "title", "family", "status", "evidence_file",
                  "collected_date", "notes", "reason"]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Markdown summary
    md_path = OUTPUT_DIR / "control_status.md"
    status_counts = {}
    for r in rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1

    lines = [
        "# Control Status Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Freshness threshold: {FRESHNESS_DAYS} days",
        "",
        "## Summary",
        "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- **{status}**: {count}")
    lines.extend(["", "## Detail", ""])
    lines.append("| Control | Title | Status | Evidence | Collected | Reason |")
    lines.append("|---------|-------|--------|----------|-----------|--------|")
    for r in rows:
        lines.append(
            f"| {r['control_id']} | {r['title']} | {r['status']} | "
            f"{r['evidence_file']} | {r['collected_date']} | {r['reason']} |"
        )

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Report written to:")
    print(f"  {csv_path}")
    print(f"  {md_path}")
    print()
    print("Summary:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    generate_report()
