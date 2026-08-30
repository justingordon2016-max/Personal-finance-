# Personal finance — budget overview

A cash-flow analysis of two FNB Private Wealth accounts — cheque `…8756` and
credit card `…4002` — built from six consecutive statements covering
**16 May – 28 August 2026**.

## The short version

**What is left after the debit orders and fixed payments: R12,625.81.**

| On salary alone | Per month | Running |
|---|---|---|
| Salary | 70,000.00 | 70,000.00 |
| Less fixed costs | −57,374.19 | **12,625.81** |
| Less variable spending | −10,333.17 | 2,292.64 |
| Less savings debit orders | −14,506.22 | **−12,213.58** |

Fixed costs are 82% of salary. After them *and* normal living you genuinely have
about **R2,293/month spare** — but R14,506 of savings instructions then clear on
top, so the plan runs **R12,214/month** beyond what salary supports. That gap is
what drained R45,161 of buffer in three months, not overspending: discretionary
living (food, shopping, travel, fuel) is R5,786/month.

### Fixed — R57,374/month, 82% of salary

| Category | Per month | % of salary |
|---|---|---|
| Debt (structured loan, WesBank, iStore, home-loan fee) | 28,483.30 | 40.7% |
| Insurance & cover (Discovery, FNB Life ×2, JAC, Netstar) | 15,785.84 | 22.6% |
| Subscription (Happy Hound, weekly) | 6,143.54 | 8.8% |
| Connectivity (FNB Connect ×3, top-ups ×2, RSAWEB ×2, Stratum) | 5,804.01 | 8.3% |
| Bank charges | 758.50 | 1.1% |
| Home (Edgekloof levy) | 399.00 | 0.6% |

Two days do almost all of it: the **31st** takes R27,813 (R21,891 of it the
structured loan) and the **1st** takes R16,905, mostly insurance and fibre. By the
3rd you are down to R11,598.

### Savings — R14,506/month, shown separately

R9,000 scheduled transfer + R2,500 FNB Invest + R3,006.22 EasyEquities TFSA.
Money you keep, not money you spend — but it competes for the same rand.

### Variable — R10,333/month

Family support R3,382 · food R3,199 · shopping R1,395 · electricity R833 ·
travel R733 · fuel R459 · airtime R209 · interest R123.

### Other headlines

| | |
|---|---|
| Cash buffer | R49,838 → R4,677 (down R45,161 in three months) |
| Card debt | R16,972 → R10,770 (down R6,201) |
| Net worth | up about **R2,353 / month**, before loan principal |

The cheque account was overdrawn for five days in late July, bottoming around
R3,200 below zero before payday — the R9,000 savings transfer leaves on the 27th,
four days ahead of the month-end run.

### Two beneficiaries, confirmed by the account holder

- `FWT` R3,006.22 / month — **EasyEquities tax-free savings account**. Counts as
  savings, not spending. Note R3,006.22 × 12 = R36,074.64, R74.64 over the R36,000
  annual TFSA limit; SARS taxes the excess at 40%. An even R3,000 lands on the limit.
- `JAC` R3,836.27 / month — **insurance**. With FNB Life (R4,140.19) this is
  R7,976.46 / month of life and risk cover across two providers, on top of the
  R7,578 Discovery premium.

Two further commitments were invisible until the card statements arrived: a
**weekly** `Paystack *Happy Houn` charge (R1,317.44, raised to R1,417.74 on
20 July — R73,722/year at the current rate) and a **R773.47/month iStore budget
facility** at 11.50% p.a. with R9,868.11 outstanding.

## Layout

```
data/transactions.csv         Cheque account, 140 transactions, hand-categorised
data/card-transactions.csv    Credit card, 52 rows across both facilities
data/monthly-commitments.csv  The standing fixed/savings schedule, at current rates
scripts/analyze.py            Cheque reconciliation + category/commitment summaries
scripts/analyze_card.py       Card reconciliation, spending mix, payment cross-check
scripts/monthly_plan.py       Fixed vs variable split and the payday-to-payday walk
scripts/balance_series.py     Running daily balance as JSON (feeds the chart)
reports/budget-overview.html  The published overview
```

## Running it

```sh
python3 scripts/analyze.py        # cheque summary tables + reconciliation check
python3 scripts/analyze_card.py   # card facilities, spending mix, payment cross-check
python3 scripts/monthly_plan.py   # what's left after fixed costs, step by step
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

## Fixed versus variable

Fixed means a standing instruction at a rate you cannot change this month, and lives
in `data/monthly-commitments.csv`. Prepaid electricity and airtime are treated as
variable — they recur, but you choose when and how much. Savings debit orders are
kept separate from fixed costs throughout, because they are money you keep.

## Categorisation

Categories are judgement calls, not bank data. To change one, edit the `category`
or `subcategory` column in `data/transactions.csv` and re-run `analyze.py`.

Every recurring beneficiary is now identified. The two Netcash debit orders that
the statements name only as `JAC` and `FWT` were confirmed by the account holder as
insurance and an EasyEquities TFSA respectively, and are categorised accordingly.

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
