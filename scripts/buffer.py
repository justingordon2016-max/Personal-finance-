#!/usr/bin/env python3
"""How much has to be in the account to get through the debit orders.

Groups the standing schedule by the day it clears, finds the biggest single day
and the worst back-to-back run, and works out the opening balance needed to end
the cycle without going overdrawn.
"""
import csv, json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SALARY = 70000.00

# Variable spend splits across the two accounts; the card portion is settled
# through the cheque account when the card is paid, so both land here in the end.
CHEQUE_VARIABLE = 8499.63
CARD_VARIABLE   = 1833.00
CARD_FIXED      = 6917.01   # Happy Hound 6143.54 + iStore instalment 773.47

DAY_ORDER = ["25th", "27th", "31st", "1st", "3rd", "17th", "18th"]


def by_day():
    rows = list(csv.DictReader((ROOT / "data" / "monthly-commitments.csv").open()))
    days = OrderedDict((d, {"total": 0.0, "items": []}) for d in DAY_ORDER)
    for r in rows:
        if r["type"] == "Income" or r["day_label"] not in days:
            continue
        amt = float(r["amount"])
        days[r["day_label"]]["total"] += amt
        days[r["day_label"]]["items"].append((r["description"], amt, r["type"]))
    return days


def main():
    days = by_day()
    run = sum(d["total"] for d in days.values())

    print("=" * 74)
    print("WHAT CLEARS, AND WHEN  (cheque account debit orders only)")
    print("=" * 74)
    for d, v in days.items():
        print(f"  {d:>5}  {v['total']:>11,.2f}   ({len(v['items'])} debit"
              f"{'s' if len(v['items']) != 1 else ''})")
    print(f"  {'TOTAL':>5}  {run:>11,.2f}")

    # worst consecutive run of days
    tot = [days[d]["total"] for d in DAY_ORDER]
    worst, wi, wj = 0.0, 0, 0
    for i in range(len(tot)):
        for j in range(i, len(tot)):
            s = sum(tot[i:j + 1])
            if s > worst:
                worst, wi, wj = s, i, j
    big = max(DAY_ORDER, key=lambda d: days[d]["total"])

    print("\n" + "=" * 74)
    print("THE NUMBERS THAT MATTER")
    print("=" * 74)
    print(f"  Biggest single day        {big:>6}  {days[big]['total']:>11,.2f}")
    print(f"  31st + 1st back to back           "
          f"{days['31st']['total'] + days['1st']['total']:>11,.2f}")
    print(f"  31st + 1st + 3rd (to the 4th)     "
          f"{days['31st']['total'] + days['1st']['total'] + days['3rd']['total']:>11,.2f}")
    print(f"  Whole run, 25th to 18th           {run:>11,.2f}"
          f"   ({run/SALARY*100:.0f}% of salary)")
    print(f"  Salary                            {SALARY:>11,.2f}")
    print(f"  Spare after the debit orders      {SALARY - run:>11,.2f}")

    print("\n" + "=" * 74)
    print("BUT THE DEBIT ORDERS ARE NOT THE WHOLE CYCLE")
    print("=" * 74)
    cycle = run + CARD_FIXED + CARD_VARIABLE + CHEQUE_VARIABLE
    print(f"  Debit orders                      {run:>11,.2f}")
    print(f"  Card settlement (fixed)           {CARD_FIXED:>11,.2f}")
    print(f"  Card settlement (variable)        {CARD_VARIABLE:>11,.2f}")
    print(f"  Living, straight off the cheque   {CHEQUE_VARIABLE:>11,.2f}")
    print(f"  {'-'*56}")
    print(f"  TOTAL OUT PER CYCLE               {cycle:>11,.2f}")
    print(f"  Salary in                         {SALARY:>11,.2f}")
    print(f"  OPENING BALANCE NEEDED            {cycle - SALARY:>11,.2f}")

    # running low point, starting from the required opening balance
    need = cycle - SALARY
    print("\n" + "=" * 74)
    print(f"THE CYCLE STARTING FROM {need:,.2f}")
    print("=" * 74)
    bal = need + SALARY
    print(f"  {'25th':>5}  salary in                  {bal:>11,.2f}")
    for d in DAY_ORDER:
        bal -= days[d]["total"]
        print(f"  {d:>5}  after {days[d]['total']:>10,.2f}       {bal:>11,.2f}")
    for label, amt in (("card settlement", CARD_FIXED + CARD_VARIABLE),
                       ("living", CHEQUE_VARIABLE)):
        bal -= amt
        print(f"  {'':>5}  after {amt:>10,.2f} {label:<10}{bal:>11,.2f}")

    print("\n" + "=" * 74)
    print("CLOSING THE GAP: what each change is worth")
    print("=" * 74)
    gap = cycle - SALARY
    opts = [
        ("Stop the R9,000 savings transfer", 9000.00),
        ("  + stop FNB Invest (R2,500)", 2500.00),
        ("  + stop the EasyEquities TFSA (R3,006.22)", 3006.22),
    ]
    running = gap
    for name, v in opts:
        running -= v
        state = "covered" if running <= 0 else f"still short {running:,.2f}"
        print(f"  {name:<44} -{v:>9,.2f}   {state}")
    print(f"\n  Overdraft cost of carrying the gap at 21%: "
          f"{gap*0.21:,.2f}/yr on {gap:,.2f}")

    (ROOT / "reports" / "buffer.json").write_text(json.dumps({
        "salary": SALARY,
        "debitOrderRun": round(run, 2),
        "byDay": {d: round(v["total"], 2) for d, v in days.items()},
        "biggestDay": {"day": big, "amount": round(days[big]["total"], 2)},
        "monthEndRun": round(days["31st"]["total"] + days["1st"]["total"], 2),
        "toTheFourth": round(days["31st"]["total"] + days["1st"]["total"]
                             + days["3rd"]["total"], 2),
        "spareAfterDebitOrders": round(SALARY - run, 2),
        "cycleTotal": round(cycle, 2),
        "openingBalanceNeeded": round(cycle - SALARY, 2),
    }, indent=2))
    print("\n  Wrote reports/buffer.json")


if __name__ == "__main__":
    main()
