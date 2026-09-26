#!/usr/bin/env python3
"""The budget: fixed, variable and savings, at current rates.

data/budget.csv is the single source of truth for what things cost now.
The transaction files behind it (data/transactions.csv, data/card-transactions.csv)
are the evidence; analyze.py and analyze_card.py reconcile them to the statements.
"""
import csv, json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALARY = 70000.00
ONE_OFF = ("Medical, out of pocket (June)", 26060.66)

CAT_ORDER = ["Debt", "Insurance & cover", "Subscriptions", "Connectivity",
             "Unidentified", "Bank charges", "Home", "Second credit account",
             "Food", "Family", "Shopping", "Travel", "Transport", "Savings"]


def load():
    rows = list(csv.DictReader((ROOT / "data" / "budget.csv").open()))
    for r in rows:
        r["amount"] = float(r["amount"])
    return rows


def group(rows, kind):
    out = OrderedDict()
    for c in CAT_ORDER:
        items = [r for r in rows if r["type"] == kind and r["category"] == c]
        if items:
            out[c] = sorted(items, key=lambda r: -r["amount"])
    return out


def show(title, grouped, salary=SALARY):
    total = sum(r["amount"] for g in grouped.values() for r in g)
    print("\n" + "=" * 78)
    print(f"{title}  —  {total:,.2f}/month  ({total/salary*100:.1f}% of salary)")
    print("=" * 78)
    for cat, items in grouped.items():
        sub = sum(r["amount"] for r in items)
        print(f"\n  {cat.upper()}  {sub:,.2f}")
        for r in items:
            flag = f"  [{r['status']}]" if r["status"] else ""
            day = r["day"] if r["day"] != "-" else ""
            print(f"    {r['item']:<38} {r['amount']:>10,.2f}  {day:<10}"
                  f"{r['account']:<10}{flag}")
    return total


def main():
    rows = load()
    fixed = group(rows, "Fixed")
    variable = group(rows, "Variable")
    savings = group(rows, "Savings")

    tot_fixed = show("FIXED EXPENSES", fixed)
    tot_var = show("VARIABLE EXPENSES", variable)
    tot_sav = show("SAVINGS", savings)

    print("\n" + "=" * 78)
    print("THE BUDGET")
    print("=" * 78)
    steps = [("Salary", SALARY), ("Fixed expenses", -tot_fixed),
             ("Variable expenses", -tot_var), ("Savings", -tot_sav)]
    bal = 0.0
    for name, v in steps:
        bal += v
        print(f"  {name:<24} {v:>12,.2f}   {bal:>12,.2f}")
    print(f"\n  Left after fixed only:        {SALARY - tot_fixed:>12,.2f}")
    print(f"  Left after fixed + variable:  {SALARY - tot_fixed - tot_var:>12,.2f}")
    print(f"  Monthly gap:                  {bal:>12,.2f}")

    unknown = [r for r in rows if r["status"] == "unidentified"]
    u = sum(r["amount"] for r in unknown)
    print(f"\n  Of which unidentified: {u:,.2f}/month "
          f"({', '.join(r['item'] for r in unknown)})")
    print(f"  Excluded one-off: {ONE_OFF[0]} {ONE_OFF[1]:,.2f}")

    (ROOT / "reports" / "budget.json").write_text(json.dumps({
        "salary": SALARY,
        "totals": {"fixed": round(tot_fixed, 2), "variable": round(tot_var, 2),
                   "savings": round(tot_sav, 2)},
        "leftAfterFixed": round(SALARY - tot_fixed, 2),
        "leftAfterVariable": round(SALARY - tot_fixed - tot_var, 2),
        "gap": round(bal, 2),
        "unidentified": round(u, 2),
        "oneOff": {"name": ONE_OFF[0], "amount": ONE_OFF[1]},
        "groups": {k: {c: [{kk: r[kk] for kk in
                            ("item", "amount", "frequency", "day", "account",
                             "basis", "status")} for r in items]
                       for c, items in g.items()}
                   for k, g in (("fixed", fixed), ("variable", variable),
                                ("savings", savings))},
        "subtotals": {k: {c: round(sum(r["amount"] for r in items), 2)
                          for c, items in g.items()}
                      for k, g in (("fixed", fixed), ("variable", variable),
                                   ("savings", savings))},
    }, indent=2))
    print("\n  Wrote reports/budget.json")


if __name__ == "__main__":
    main()
