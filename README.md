# Personal finance — budget

The budget at **September 2026 rates**, built from seven FNB statements across two
accounts covering 16 May to 17 September 2026. Every cycle reconciles to the
opening and closing balances printed on the statement.

## The budget

| | Per month | % of salary |
|---|---|---|
| Salary | 70,000.00 | 100.0% |
| Less fixed expenses | −58,542.21 | 83.6% |
| **Left after fixed expenses** | **11,457.79** | 16.4% |
| Less variable expenses | −16,861.18 | 24.1% |
| **Left after fixed and variable** | **−5,403.39** | — |
| Less savings instructions | −14,506.22 | 20.7% |
| **Monthly gap** | **−19,909.61** | — |

## Fixed — R58,542/month, 22 standing instructions

A rate you cannot change this month, shown at its most recent amount, not an average.

| Category | Per month | Per year | Items |
|---|---|---|---|
| Debt | 28,794.86 | 345,538.32 | Structured loan 22,202.79 · WesBank 5,749.60 · iStore 773.47 · home fee 69.00 |
| Insurance & cover | 15,785.84 | 189,430.08 | Discovery 7,578.00 · FNB Life 4,106.61 · JAC 3,836.27 · Netstar 231.38 · FNB Life 33.58 |
| Subscriptions | 6,143.54 | 73,722.48 | Happy Hound, R1,417.74 **weekly** |
| Connectivity | 5,804.01 | 69,648.12 | RSAWEB 1,728.00 + 1,299.01 · FNB Connect 749 + 579 + 499 · top-ups 415 + 145 · Stratum 390 |
| Unidentified | 850.00 | 10,200.00 | Ril Res001 — new 1 September |
| Bank charges | 764.96 | 9,179.52 | Service fee 661.46 · linked charges 103.50 |
| Home | 399.00 | 4,788.00 | Edgekloof levy |

## Variable — R16,861/month, four-cycle averages

You choose when and how much. Prepaid electricity and airtime sit here for that
reason, even though they recur.

| Item | Per month | Account |
|---|---|---|
| Payments to a second credit account | 7,750.00 | **Unknown** |
| Groceries and eating out | 3,196.98 | Both |
| Family support | 2,662.65 | Cheque |
| Shopping and other retail | 1,196.61 | Both |
| Travel and leisure | 777.70 | Both |
| Prepaid electricity | 625.00 | Cheque |
| Transport and fuel | 344.14 | Cheque |
| Airtime top-ups | 188.25 | Cheque |
| Overdraft and card interest | 119.85 | Both |

Strip the second credit account out and variable is **R9,111**, of which genuine
discretionary spending is R5,515. June's R26,060.66 of out-of-pocket medical was a
one-off and is excluded everywhere.

## Savings — R14,506/month, kept separate

R9,000 scheduled transfer (27th) · R3,006.22 EasyEquities TFSA (1st) · R2,500 FNB
Invest (17th). 20.7% of net salary. Standing instructions like the fixed block, but
money kept rather than spent — which is why they are in their own column.

## Timing

The debit-order run is R66,131.42, 94% of salary, and clears on salary alone with
R3,868.58 to spare. **R49,284 has to be in the account by the 30th** to carry the
31st (R28,124.89, four debits), the 1st (R17,754.24, twelve) and the 3rd. For the
full cycle, including the card settlement and living, R19,909 is needed on top of
salary.

## Open items

- **A second credit account.** Every "FNB App **Transfer** To Credit" plus the Fnbcc
  debit order totals R55,490.47 — exactly what card …4002 received. Every "FNB App
  **Payment** To Credit" totals R31,000.00 and appears nowhere. No statement exists
  for it, so its R7,750/month is the least reliable line in this budget.
- **A R200,000 capital repayment** on 9 September. If it came off the structured loan
  and the term was held, the 30 September debit should fall by roughly R2,000–R6,500.
- **Ril Res001**, R850/month, new on 1 September, assumed recurring.
- **The structured loan has risen three times**: 21,828.65 → 21,891.23 → 22,202.79.
- **The TFSA is R74.64/year over** the R36,000 annual limit; excess is taxed at 40%.
  An even R3,000 lands on it.

## Layout

```
data/budget.csv               THE BUDGET — every line at its current rate, classified
data/transactions.csv         Cheque account, statements 135–138, 184 transactions
data/card-transactions.csv    Credit card 4002, statements 130–132, both facilities
data/monthly-commitments.csv  The standing schedule by day, for the payday-to-payday walk

scripts/budget.py             Builds the budget summary from data/budget.csv
scripts/make_workbook.py      Builds reports/budget.xlsx
scripts/analyze.py            Cheque reconciliation + category summaries
scripts/analyze_card.py       Card reconciliation + the Transfer/Payment split
scripts/monthly_plan.py       Fixed vs variable and the payday-to-payday walk
scripts/buffer.py             What has to be in the account, and when
scripts/balance_series.py     Running daily balance as JSON (feeds the chart)

reports/budget-overview.html  The published overview
reports/budget.xlsx           The editable workbook
```

## Running it

```sh
python3 scripts/budget.py         # the budget: fixed, variable, savings
python3 scripts/analyze.py        # cheque reconciliation
python3 scripts/analyze_card.py   # card reconciliation + second-account split
python3 scripts/buffer.py         # what has to be in the account, and when
python3 scripts/make_workbook.py  # rebuild the xlsx
```

Only `make_workbook.py` needs a third-party package (`openpyxl`).

## Reconciliation

| Cheque | Period | In | Out | Closing | Stated |
|---|---|---|---|---|---|
| 135 | 16 May – 17 Jun | 72,500.00 | 79,545.82 | 42,792.28 | 42,792.28 |
| 136 | 17 Jun – 17 Jul | 76,245.62 | 116,543.50 | 2,494.40 | 2,494.40 |
| 137 | 17 Jul – 17 Aug | 104,745.73 | 102,562.88 | 4,677.25 | 4,677.25 |
| 138 | 17 Aug – 17 Sep | 300,000.00 | 295,740.41 | 8,936.84 | 8,936.84 |

Card statements 130–132 reconcile on both the Straight and Budget facilities — six
checks, all tying to R0.00.

## Editing it

`data/budget.csv` is the source of truth for what things cost. Change an amount or a
classification there and re-run `scripts/budget.py` and `scripts/make_workbook.py`.
In `reports/budget.xlsx`, the blue cells are inputs and everything else is a formula.

## What this does not cover

Any statement for the second credit account. Balances for the savings, investment,
structured-loan and vehicle-finance accounts, so the principal repaid each month is
not counted anywhere. A card statement covering September. The two accounts run on
different cycles — the card closes around the 29th, the cheque account on the 17th —
so combined monthly figures are close but not exact.

Nothing here is financial advice; it is your own data, added up.
