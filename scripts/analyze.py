#!/usr/bin/env python3
"""Budget overview for FNB Fusion Private Wealth acct 62542488756.

Reads data/transactions.csv (transcribed from three FNB statements) and prints
a reconciliation check plus category summaries per statement cycle.
"""
import csv
from collections import defaultdict, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "transactions.csv"

# Opening/closing balances as printed on each statement, for reconciliation.
STATEMENTS = OrderedDict([
    ("135", dict(label="16 May – 17 Jun 2026", opening=49838.10, closing=42792.28)),
    ("136", dict(label="17 Jun – 17 Jul 2026", opening=42792.28, closing=2494.40)),
    ("137", dict(label="17 Jul – 17 Aug 2026", opening=2494.40, closing=4677.25)),
])

# Order in which categories are reported (largest structural items first).
CATEGORY_ORDER = [
    "Debt & Loans",
    "Insurance & Medical",
    "Savings & Investments",
    "Credit Card Payments",
    "Unidentified Recurring",
    "Connectivity & Subscriptions",
    "Home & Utilities",
    "Groceries & Eating Out",
    "Family Support",
    "Transport & Fuel",
    "Shopping & Other",
    "Bank Charges & Interest",
    "Pass-through",
    "Income",
]


def load():
    with CSV.open() as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["amount"] = float(r["amount"])
        r["signed"] = r["amount"] if r["direction"] == "Cr" else -r["amount"]
    return rows


def reconcile(rows):
    print("=" * 74)
    print("RECONCILIATION vs printed statement balances")
    print("=" * 74)
    ok = True
    for stmt, meta in STATEMENTS.items():
        rs = [r for r in rows if r["statement"] == stmt]
        cr = sum(r["amount"] for r in rs if r["direction"] == "Cr")
        dr = sum(r["amount"] for r in rs if r["direction"] == "Dr")
        derived = meta["opening"] + cr - dr
        diff = derived - meta["closing"]
        ok &= abs(diff) < 0.005
        print(f"  Stmt {stmt} ({meta['label']}): {len(rs):>2} txns | "
              f"in {cr:>12,.2f} | out {dr:>12,.2f} | "
              f"close {derived:>11,.2f} (stated {meta['closing']:,.2f}, diff {diff:+.2f})")
    print(f"\n  Reconciled: {'YES' if ok else 'NO'}")
    return ok


def by_category(rows):
    """{category: {statement: total_outflow}} for spending categories."""
    out = defaultdict(lambda: defaultdict(float))
    for r in rows:
        if r["category"] == "Income":
            continue
        if r["direction"] == "Cr":  # rebates offset their own category
            out[r["category"]][r["statement"]] -= r["amount"]
        else:
            out[r["category"]][r["statement"]] += r["amount"]
    return out


def report(rows):
    stmts = list(STATEMENTS)

    print("\n" + "=" * 74)
    print("INCOME BY CYCLE")
    print("=" * 74)
    for s in stmts:
        inc = [r for r in rows if r["statement"] == s and r["category"] == "Income"]
        print(f"\n  Cycle {s} ({STATEMENTS[s]['label']})")
        for r in sorted(inc, key=lambda x: -x["amount"]):
            print(f"    {r['subcategory']:<26} {r['amount']:>12,.2f}")
        print(f"    {'TOTAL INCOME':<26} {sum(r['amount'] for r in inc):>12,.2f}")

    cats = by_category(rows)
    print("\n" + "=" * 74)
    print("OUTFLOW BY CATEGORY AND CYCLE (ZAR)")
    print("=" * 74)
    header = f"  {'Category':<30}" + "".join(f"{s:>14}" for s in stmts) + f"{'Avg/mo':>14}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    ordered = [c for c in CATEGORY_ORDER if c in cats]
    for c in ordered:
        vals = [cats[c].get(s, 0.0) for s in stmts]
        avg = sum(vals) / len(vals)
        print(f"  {c:<30}" + "".join(f"{v:>14,.2f}" for v in vals) + f"{avg:>14,.2f}")
    tot = [sum(cats[c].get(s, 0.0) for c in ordered) for s in stmts]
    print("  " + "-" * (len(header) - 2))
    print(f"  {'TOTAL OUTFLOW':<30}" + "".join(f"{v:>14,.2f}" for v in tot)
          + f"{sum(tot)/len(tot):>14,.2f}")

    print("\n" + "=" * 74)
    print("NET POSITION PER CYCLE (income minus all outflow)")
    print("=" * 74)
    for i, s in enumerate(stmts):
        inc = sum(r["amount"] for r in rows
                  if r["statement"] == s and r["category"] == "Income")
        print(f"  Cycle {s}: income {inc:>12,.2f} | outflow {tot[i]:>12,.2f} "
              f"| net {inc - tot[i]:>+12,.2f}")

    print("\n" + "=" * 74)
    print("FIXED MONTHLY COMMITMENTS (debit orders present in all three cycles)")
    print("=" * 74)
    seen = defaultdict(lambda: defaultdict(float))
    for r in rows:
        if r["direction"] == "Dr" and r["subcategory"]:
            seen[(r["category"], r["subcategory"])][r["statement"]] += r["amount"]
    fixed = {k: v for k, v in seen.items() if len(v) == 3}
    total = 0.0
    for (cat, sub), v in sorted(fixed.items(), key=lambda kv: -sum(kv[1].values())):
        avg = sum(v.values()) / 3
        if cat in ("Bank Charges & Interest", "Groceries & Eating Out",
                   "Credit Card Payments"):
            continue
        total += avg
        print(f"  {sub:<28} {cat:<28} {avg:>12,.2f}")
    print(f"  {'TOTAL FIXED (excl. card & variable)':<57} {total:>12,.2f}")

    print("\n" + "=" * 74)
    print("FLAGGED FOR YOU TO IDENTIFY")
    print("=" * 74)
    for r in rows:
        if r["note"].startswith("UNCONFIRMED"):
            print(f"  {r['date']}  {r['description']:<42} {r['amount']:>10,.2f}")


if __name__ == "__main__":
    rows = load()
    reconcile(rows)
    report(rows)
