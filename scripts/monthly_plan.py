#!/usr/bin/env python3
"""What is left each month after the debit orders and fixed payments clear.

Reads data/monthly-commitments.csv (the standing schedule, at current rates) and
data/transactions.csv + data/card-transactions.csv (what was actually spent), and
walks the salary cycle day by day.
"""
import csv, json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALARY = 70000.00

# Variable spend, 3-cycle averages, both accounts. Anything not on the standing
# schedule: bought when needed, in amounts that change month to month.
VARIABLE = [
    ("Family support",            3381.87, "Cheque"),
    ("Food, groceries and eating out", 3199.02, "Both"),
    ("Shopping and other retail", 1395.03, "Both"),
    ("Prepaid electricity",        833.33, "Cheque"),
    ("Travel and leisure",         733.20, "Card"),
    ("Transport and fuel",         458.85, "Cheque"),
    ("Airtime top-ups",            209.33, "Cheque"),
    ("Overdraft and card interest", 122.54, "Both"),
]
ONE_OFF = ("Medical, out of pocket (June)", 8686.89)


def load_schedule():
    with (ROOT / "data" / "monthly-commitments.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["amount"] = float(r["amount"])
        r["cycle_day"] = int(r["cycle_day"])
    return rows


def walk(rows):
    """Running balance through the cycle, fixed first then savings."""
    steps, bal = [], 0.0
    for r in sorted(rows, key=lambda x: (x["cycle_day"], x["type"] != "Income")):
        bal += r["amount"] if r["type"] == "Income" else -r["amount"]
        steps.append({"day": r["day_label"], "what": r["description"],
                      "amount": r["amount"], "type": r["type"],
                      "left": round(bal, 2)})
    return steps


def main():
    rows = load_schedule()
    fixed = [r for r in rows if r["type"] == "Fixed"]
    savings = [r for r in rows if r["type"] == "Savings"]
    tot_fixed = sum(r["amount"] for r in fixed)
    tot_sav = sum(r["amount"] for r in savings)
    tot_var = sum(a for _, a, _ in VARIABLE)

    print("=" * 78)
    print("THE ANSWER: what is left after the debit orders and fixed payments")
    print("=" * 78)
    print(f"  Salary                                        {SALARY:>12,.2f}")
    print(f"  Fixed costs (must be paid)                   -{tot_fixed:>12,.2f}")
    print(f"  {'-'*62}")
    print(f"  LEFT AFTER FIXED COSTS                        {SALARY - tot_fixed:>12,.2f}")
    print(f"  Savings debit orders (scheduled)             -{tot_sav:>12,.2f}")
    print(f"  {'-'*62}")
    print(f"  LEFT AFTER SAVINGS TOO                        {SALARY - tot_fixed - tot_sav:>12,.2f}")
    print(f"  Variable spending (3-cycle average)          -{tot_var:>12,.2f}")
    print(f"  {'-'*62}")
    print(f"  MONTHLY GAP                                   "
          f"{SALARY - tot_fixed - tot_sav - tot_var:>12,.2f}")

    print("\n" + "=" * 78)
    print("FIXED COSTS BY CATEGORY (current rates)")
    print("=" * 78)
    by = defaultdict(float)
    for r in fixed:
        by[r["category"]] += r["amount"]
    for c, v in sorted(by.items(), key=lambda kv: -kv[1]):
        print(f"  {c:<24} {v:>12,.2f}   {v/SALARY*100:>5.1f}% of salary")
    print(f"  {'TOTAL FIXED':<24} {tot_fixed:>12,.2f}   {tot_fixed/SALARY*100:>5.1f}%")

    print("\n" + "=" * 78)
    print("VARIABLE / DISCRETIONARY (3-cycle average)")
    print("=" * 78)
    for n, a, acct in VARIABLE:
        print(f"  {n:<34} {a:>10,.2f}   {acct}")
    print(f"  {'TOTAL VARIABLE':<34} {tot_var:>10,.2f}")
    print(f"\n  Against the {SALARY - tot_fixed:,.2f} left after fixed costs, "
          f"that leaves {SALARY - tot_fixed - tot_var:+,.2f}")
    print(f"  {ONE_OFF[0]}: {ONE_OFF[1]:,.2f}/month averaged, not recurring")

    print("\n" + "=" * 78)
    print("THE CYCLE, DAY BY DAY")
    print("=" * 78)
    for s in walk(rows):
        tag = {"Income": "+", "Savings": "s", "Fixed": " "}[s["type"]]
        print(f"  {s['day']:>7} {tag} {s['what']:<44} "
              f"{s['amount']:>10,.2f}  ->{s['left']:>12,.2f}")

    out = {
        "salary": SALARY,
        "totalFixed": round(tot_fixed, 2),
        "totalSavings": round(tot_sav, 2),
        "totalVariable": round(tot_var, 2),
        "leftAfterFixed": round(SALARY - tot_fixed, 2),
        "leftAfterSavings": round(SALARY - tot_fixed - tot_sav, 2),
        "gap": round(SALARY - tot_fixed - tot_sav - tot_var, 2),
        "fixedByCategory": {k: round(v, 2) for k, v in
                            sorted(by.items(), key=lambda kv: -kv[1])},
        "variable": [{"name": n, "amount": a, "account": acct} for n, a, acct in VARIABLE],
        "fixed": [{"day": r["day_label"], "what": r["description"],
                   "amount": r["amount"], "category": r["category"],
                   "account": r["account"], "note": r["note"]} for r in fixed],
        "savingsItems": [{"day": r["day_label"], "what": r["description"],
                          "amount": r["amount"], "note": r["note"]} for r in savings],
        "steps": walk(rows),
    }
    (ROOT / "reports" / "monthly-plan.json").write_text(json.dumps(out, indent=2))
    print(f"\n  Wrote reports/monthly-plan.json")


if __name__ == "__main__":
    main()
