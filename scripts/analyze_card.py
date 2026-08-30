#!/usr/bin/env python3
"""Credit-card analysis for FNB Private Wealth card 4483 81** **** 4002.

Reconciles both facilities (Straight and Budget) against the printed statement
balances, then summarises what the card was actually used for, and cross-checks
card payments against the cheque account's "payment to credit" transactions.
"""
import csv
from collections import defaultdict, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STATEMENTS = OrderedDict([
    ("130", dict(label="30 May – 29 Jun 2026",
                 open_s=5108.22, close_s=-368.53, open_b=11863.32, close_b=11209.46)),
    ("131", dict(label="30 Jun – 29 Jul 2026",
                 open_s=-368.53, close_s=2437.53, open_b=11209.46, close_b=10541.94)),
    ("132", dict(label="30 Jul – 28 Aug 2026",
                 open_s=2437.53, close_s=902.27, open_b=10541.94, close_b=9868.11)),
])


def load(name):
    with (ROOT / "data" / name).open() as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["amount"] = float(r["amount"])
    return rows


def reconcile(rows):
    print("=" * 76)
    print("CARD RECONCILIATION vs printed statement balances")
    print("=" * 76)
    ok = True
    for stmt, m in STATEMENTS.items():
        rs = [r for r in rows if r["statement"] == stmt]
        for fac, o, c in (("Straight", m["open_s"], m["close_s"]),
                          ("Budget", m["open_b"], m["close_b"])):
            f = [r for r in rs if r["facility"] == fac]
            dr = sum(r["amount"] for r in f if r["direction"] == "Dr")
            cr = sum(r["amount"] for r in f if r["direction"] == "Cr")
            derived = o + dr - cr
            diff = derived - c
            ok &= abs(diff) < 0.005
            print(f"  Stmt {stmt} {fac:<9} open {o:>10,.2f} + charges {dr:>10,.2f} "
                  f"- credits {cr:>10,.2f} = {derived:>10,.2f} "
                  f"(stated {c:>10,.2f}, diff {diff:+.2f})")
    print(f"\n  Reconciled: {'YES' if ok else 'NO'}")
    return ok


def spending(rows):
    print("\n" + "=" * 76)
    print("WHAT THE CARD WAS USED FOR (new spending, excl. internal transfers)")
    print("=" * 76)
    skip = {"Payment", "Budget Instalment", "Interest"}
    cats = defaultdict(lambda: defaultdict(float))
    for r in rows:
        if r["category"] in skip or r["direction"] == "Cr":
            continue
        cats[r["category"]][r["statement"]] += r["amount"]
    stmts = list(STATEMENTS)
    hdr = f"  {'Category':<26}" + "".join(f"{s:>13}" for s in stmts) + f"{'Total':>13}{'Avg/mo':>12}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    grand = 0.0
    for c, v in sorted(cats.items(), key=lambda kv: -sum(kv[1].values())):
        vals = [v.get(s, 0.0) for s in stmts]
        tot = sum(vals)
        grand += tot
        print(f"  {c:<26}" + "".join(f"{x:>13,.2f}" for x in vals)
              + f"{tot:>13,.2f}{tot/3:>12,.2f}")
    print("  " + "-" * (len(hdr) - 2))
    print(f"  {'TOTAL NEW SPENDING':<26}" + " " * 39
          + f"{grand:>13,.2f}{grand/3:>12,.2f}")

    weekly = [r for r in rows if r["category"] == "Weekly Subscription"]
    print(f"\n  The weekly subscription alone: {len(weekly)} charges over 3 cycles, "
          f"{sum(r['amount'] for r in weekly):,.2f} total")
    print(f"  Current rate 1,417.74/week  ->  {1417.74 * 52 / 12:,.2f}/month, "
          f"{1417.74 * 52:,.2f}/year")


def debt_and_payments(rows, cheque):
    print("\n" + "=" * 76)
    print("WHERE THE CARD PAYMENTS ACTUALLY WENT")
    print("=" * 76)
    paid = sum(r["amount"] for r in rows if r["category"] == "Payment")
    interest = sum(r["amount"] for r in rows
                   if r["category"] == "Interest" and r["direction"] == "Dr")
    spend = sum(r["amount"] for r in rows if r["direction"] == "Dr"
                and r["category"] not in {"Payment", "Budget Instalment", "Interest"})
    open_debt = STATEMENTS["130"]["open_s"] + STATEMENTS["130"]["open_b"]
    close_debt = STATEMENTS["132"]["close_s"] + STATEMENTS["132"]["close_b"]
    print(f"  Payments received by the card        {paid:>12,.2f}")
    print(f"    ... funded new spending            {spend:>12,.2f}")
    print(f"    ... covered interest               {interest:>12,.2f}")
    print(f"    ... actually reduced debt          {open_debt - close_debt:>12,.2f}")
    print(f"\n  Total card debt {open_debt:,.2f} -> {close_debt:,.2f} "
          f"(down {open_debt - close_debt:,.2f} over 3 cycles, "
          f"{(open_debt - close_debt)/3:,.2f}/month)")

    print("\n" + "=" * 76)
    print("CROSS-CHECK: cheque account 'payment to credit' vs card payments received")
    print("=" * 76)
    out = [r for r in cheque if r["category"] == "Credit Card Payments"]
    tot_out = sum(float(r["amount"]) for r in out)
    for r in sorted(out, key=lambda x: x["date"]):
        print(f"    {r['date']}  {r['description']:<44} {float(r['amount']):>10,.2f}")
    print(f"    {'TOTAL out of the cheque account':<56} {tot_out:>10,.2f}")
    print(f"    {'TOTAL received by this card':<56} {paid:>10,.2f}")
    print(f"    {'UNMATCHED':<56} {tot_out - paid:>10,.2f}")


if __name__ == "__main__":
    rows = load("card-transactions.csv")
    cheque = load("transactions.csv")
    reconcile(rows)
    spending(rows)
    debt_and_payments(rows, cheque)
