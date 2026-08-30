#!/usr/bin/env python3
"""Emit the running daily balance as JSON, for the overview chart."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPENING = 49838.10  # stated opening balance of statement 135

rows = list(csv.DictReader((ROOT / "data" / "transactions.csv").open()))
rows.sort(key=lambda r: (r["date"], r["statement"]))

bal, series = OPENING, [{"date": "2026-05-16", "balance": OPENING}]
for r in rows:
    amt = float(r["amount"])
    bal += amt if r["direction"] == "Cr" else -amt
    series.append({"date": r["date"], "balance": round(bal, 2)})

# collapse to the last balance of each day
daily = {}
for p in series:
    daily[p["date"]] = p["balance"]
out = [{"date": d, "balance": b} for d, b in sorted(daily.items())]
print(json.dumps(out))
print(f"\n# final {out[-1]}  min {min(out, key=lambda p: p['balance'])}", file=__import__("sys").stderr)
