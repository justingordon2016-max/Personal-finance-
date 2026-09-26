# Personal finance — budget overview

A cash-flow analysis of two FNB Private Wealth accounts — cheque `…8756` and
credit card `…4002` — built from six consecutive statements covering
**16 May – 28 August 2026**.

## The short version

Six cheque statements (135–138) and three card statements (130–132), 16 May to
17 September 2026. All reconcile to the printed balances to the cent.

**What is left after the debit orders and fixed payments: R11,457.79.**

| On salary alone | Per month | Running |
|---|---|---|
| Salary | 70,000.00 | 70,000.00 |
| Less fixed costs | −58,542.21 | **11,457.79** |
| Less variable spending | −16,861.18 | −5,403.39 |
| Less savings debit orders | −14,506.22 | **−19,909.61** |

### What you need in the account to clear the debit orders

**For the debit orders alone: nothing extra.** The run is R66,131.42 against a
R70,000 salary and clears with R3,868.58 to spare — down from R5,036.60 last month.

| Clears | Amount | Debits |
|---|---|---|
| 25th | 4,685.61 | 2 |
| 27th | 9,000.00 | 1 |
| **31st** | **28,124.89** | 4 — the cliff |
| 1st | 17,754.24 | 12 |
| 3rd | 3,405.22 | 2 |
| 17th | 2,500.00 | 1 |
| 18th | 661.46 | 1 |
| **Total** | **66,131.42** | 23 (94% of salary) |

**The date to watch is the 30th: R49,284 has to be there** to carry the 31st, 1st
and 3rd — 18 debit orders inside four days.

**For the whole cycle, R19,909 on top of salary** — R89,909 leaves per cycle once
card …4002 (R8,750), living off the cheque account (R7,278) and the second credit
account (R7,750/month) are counted.

### September's findings

- **There is a second credit account.** The wording splits perfectly: every
  "FNB App **Transfer** To Credit" (plus the Fnbcc debit order) totals R55,490.47 —
  exactly what card …4002 received. Every "FNB App **Payment** To Credit" totals
  **R31,000.00** and appears nowhere. R3,000 (16 Jul), R1,000 (20 Jul), R1,000
  (21 Jul), R10,000 (7 Aug), R16,000 (20 Aug) — and accelerating.
- **A R200,000 capital repayment** on 9 September, funded by an external transfer.
  If it went against the structured loan, the 30 September debit should fall by
  roughly R2,000–R6,500/month depending on remaining term.
- **A new R850/month debit order**, "Ril Res001", first seen 1 September.
- **The structured loan has risen three times**: R21,828.65 → R21,891.23 →
  R22,202.79.
- **External money is carrying the cycle.** R30,000 in on 20 August funded R26,000
  of card payments; the cycle closed up at R8,936.84. On salary alone it would have
  closed about R25,740 down.

### Fixed — R58,542/month, 84% of salary

| Category | Per month |
|---|---|
| Debt (structured loan, WesBank, iStore, home-loan fee) | 28,794.86 |
| Insurance & cover (Discovery, FNB Life ×2, JAC, Netstar) | 15,785.84 |
| Subscription (Happy Hound, weekly) | 6,143.54 |
| Connectivity (FNB Connect ×3, top-ups ×2, RSAWEB ×2, Stratum) | 5,804.01 |
| Unidentified (Ril Res001) | 850.00 |
| Bank charges | 764.96 |
| Home (Edgekloof levy) | 399.00 |

### Savings — R14,506/month, shown separately

R9,000 scheduled transfer + R2,500 FNB Invest + R3,006.22 EasyEquities TFSA.
Note R3,006.22 × 12 = R36,074.64, R74.64 over the R36,000 annual TFSA limit; SARS
taxes the excess at 40%. An even R3,000 lands on the limit.

### Variable — R16,861/month (4-cycle average)

Second credit account R7,750 · food R3,197 · family support R2,663 · shopping
R1,197 · travel R778 · electricity R625 · fuel R344 · airtime R188 · interest R120.

Strip the second credit account out and variable is R9,111, of which genuine
discretionary spending is R5,515.

### Confirmed by the account holder

- `FWT` R3,006.22 — **EasyEquities tax-free savings account** (savings, not spending)
- `JAC` R3,836.27 — **insurance**. With FNB Life (R4,140.19) that is R7,976.46/month
  of life and risk cover across two providers, on top of the R7,578 Discovery premium.

Two commitments were invisible until the card statements arrived: a **weekly**
`Paystack *Happy Houn` charge (R1,417.74 since 20 July — R73,722/year) and a
**R773.47/month iStore budget facility** at 11.50% p.a. with R9,868.11 outstanding.

## Layout

```
data/transactions.csv         Cheque account, 140 transactions, hand-categorised
data/card-transactions.csv    Credit card, 52 rows across both facilities
data/monthly-commitments.csv  The standing fixed/savings schedule, at current rates
scripts/buffer.py             What has to be in the account, and when
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
