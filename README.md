# Personal finance — budget overview

A cash-flow analysis of FNB Fusion Private Wealth cheque account `…8756`, built
from three consecutive statements covering **16 May – 17 August 2026**.

## The short version

| | |
|---|---|
| Net salary | **R70,000** / month, steady across all three cycles |
| Fixed debit orders | **R66,100** / month — 94% of net salary |
| Left for everything else | **R3,900** / month |
| Cash buffer | R49,838 → R4,677 (down R45,161 in three months) |
| Net worth | up roughly R14,110 / month — the cash went to debt paydown and savings |

The account was overdrawn for five days in late July, bottoming around R3,200
below zero before payday.

## Layout

```
data/transactions.csv      All 140 transactions, hand-categorised
scripts/analyze.py         Reconciliation + category and commitment summaries
scripts/balance_series.py  Running daily balance as JSON (feeds the chart)
reports/budget-overview.html  The published overview
```

## Running it

```sh
python3 scripts/analyze.py        # summary tables + reconciliation check
python3 scripts/balance_series.py # daily balance series as JSON
```

Neither script needs third-party packages.

## Reconciliation

`analyze.py` checks each statement cycle against the opening and closing balances
printed on the statement. All three tie to R0.00, and the transaction counts match
the statements' own turnover lines (45 / 45 / 50):

| Statement | Period | In | Out | Closing | Stated |
|---|---|---|---|---|---|
| 135 | 16 May – 17 Jun | 72,500.00 | 79,545.82 | 42,792.28 | 42,792.28 |
| 136 | 17 Jun – 17 Jul | 76,245.62 | 116,543.50 | 2,494.40 | 2,494.40 |
| 137 | 17 Jul – 17 Aug | 104,745.73 | 102,562.88 | 4,677.25 | 4,677.25 |

## Categorisation

Categories are judgement calls, not bank data. To change one, edit the `category`
or `subcategory` column in `data/transactions.csv` and re-run `analyze.py`.

Two recurring Netcash debit orders totalling **R6,842.49/month** are marked
`Unidentified Recurring` because the statement gives no beneficiary name:

- `JAC` — R3,836.27 on the 1st
- `FWT` — R3,006.22 on the 1st

Label these once you know what they are.

## Known gaps

- **Credit-card spending is not visible.** R50,490 of cash moved to the card over
  the three cycles; what was bought with it is in the card statements, not here.
- Savings, investment, structured-loan and vehicle-finance *balances* are unknown —
  only the payments into and out of the cheque account appear.
- Two same-day in-and-out transfers (R15,280 on 24 Jul, R10,000 on 7 Aug) are tagged
  `Pass-through` and excluded from both income and outflow.
- The FNB Invest collection falls on the 17th, so four R2,500 collections land inside
  three statement periods; its R3,333/month average overstates a R2,500/month run rate.
