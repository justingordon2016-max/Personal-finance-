# Personal finance — budget overview

A cash-flow analysis of two FNB Private Wealth accounts — cheque `…8756` and
credit card `…4002` — built from six consecutive statements covering
**16 May – 28 August 2026**.

## The short version

| | |
|---|---|
| Net salary | **R70,000** / month, steady across all three cycles |
| Recurring commitments | **R73,017** / month at today's rates — 104% of net salary |
| Of which paid to yourself | R12,333 into savings and FNB Invest |
| Living costs | R11,325 / month against the R9,317 that leaves — about **R2,000 short** |
| Cash buffer | R49,838 → R4,677 (down R45,161 in three months) |
| Card debt | R16,972 → R10,770 (down R6,201) |
| Net worth | roughly **flat** (−R653 / month), before loan principal |

The cheque account was overdrawn for five days in late July, bottoming around
R3,200 below zero before payday.

Two commitments were invisible until the card statements arrived: a **weekly**
`Paystack *Happy Houn` charge (R1,317.44, raised to R1,417.74 on 20 July —
R73,722/year at the current rate) and a **R773.47/month iStore budget facility**
at 11.50% p.a. with R9,868.11 outstanding.

## Layout

```
data/transactions.csv         Cheque account, 140 transactions, hand-categorised
data/card-transactions.csv    Credit card, 52 rows across both facilities
scripts/analyze.py            Cheque reconciliation + category/commitment summaries
scripts/analyze_card.py       Card reconciliation, spending mix, payment cross-check
scripts/balance_series.py     Running daily balance as JSON (feeds the chart)
reports/budget-overview.html  The published overview
```

## Running it

```sh
python3 scripts/analyze.py        # cheque summary tables + reconciliation check
python3 scripts/analyze_card.py   # card facilities, spending mix, payment cross-check
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

`analyze_card.py` does the same for both card facilities on all three card
statements — six reconciliations, all tying to R0.00:

| Statement | Period | Straight closing | Budget closing |
|---|---|---|---|
| 130 | 30 May – 29 Jun | 368.53 Cr | 11,209.46 |
| 131 | 30 Jun – 29 Jul | 2,437.53 | 10,541.94 |
| 132 | 30 Jul – 28 Aug | 902.27 | 9,868.11 |

## Categorisation

Categories are judgement calls, not bank data. To change one, edit the `category`
or `subcategory` column in `data/transactions.csv` and re-run `analyze.py`.

Two recurring Netcash debit orders totalling **R6,842.49/month** are marked
`Unidentified Recurring` because the statement gives no beneficiary name:

- `JAC` — R3,836.27 on the 1st
- `FWT` — R3,006.22 on the 1st

Label these once you know what they are.

## Known gaps

- **R5,000 of card payments does not reconcile.** The cheque account shows
  R60,490.47 paid to "Credit"; this card recorded R55,490.47 received. The payments
  of R3,000 (16 Jul) and R1,000 each (20 and 21 Jul) have no counterpart on the card,
  and the R10,000 sent on 7 Aug posts on the card dated 20 Aug. There may be a
  second card.
- The two accounts run on **different cycles** — the card closes around the 29th,
  the cheque account on the 17th — so combined monthly figures are close but not exact.
- Savings, investment, structured-loan and vehicle-finance *balances* are unknown, so
  the principal repaid each month (real, and positive for net worth) is not counted
  anywhere.
- Two same-day in-and-out transfers (R15,280 on 24 Jul, R10,000 on 7 Aug) are tagged
  `Pass-through` and excluded from both income and outflow.
- The FNB Invest collection falls on the 17th, so four R2,500 collections land inside
  three statement periods; its R3,333/month average overstates a R2,500/month run rate.
