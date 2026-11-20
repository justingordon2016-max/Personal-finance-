# iX USA weekly process: HubSpot invoices and payouts into Xero

You are running the weekly iXperience USA process: collect the paid HubSpot invoices and the HubSpot Payments payouts, build two Xero import files, help me import them, then reconcile and check.

**How to work**
1. Give a short summary first, then the detail.
2. Don't use dashes as punctuation.
3. Write amounts in USD with two decimals. Xero dates are MM/DD/YYYY, so 11/03/2026 means 3 November.
4. Do all sums in code, not by hand. Totals must tie to the cent.

**Where we are**
1. The last batch covered HubSpot INV-1699 to INV-1780, imported as Xero INV-1566 to INV-1623.
2. The next batch starts at HubSpot invoices after INV-1780. The next Xero number is INV-1624. Check Xero's last invoice number first in case it has moved.
3. Three receipts were left in the clearing account waiting for a payout:
   1. INV-1776 Erica Zhang, $983.25.
   2. INV-1777 Illeana Higby-Medina, $2,820.38.
   3. INV-1780 Mason Oliver, $2,820.38.

   Their payouts land in this new batch. They are already invoiced, so add only the payout and fee lines for them.
4. Some HubSpot invoices were still open last week: 1701 (Nusra, returned), 1710, 1742, 1773, 1778 and 1779. Check each one again. If it is now paid, include it.

---

## Step 1. Collect the data

### 1a. HubSpot invoices (HubSpot connector, INVOICE object)
1. Pull every invoice dated after the last batch, plus the open ones above. For each, get:
   1. Invoice number (hs_number).
   2. Invoice date.
   3. Amount.
   4. Status (paid or open).
   5. Payment date.
   6. The associated deal name, which comes through query_crm_data. The deal name gives the student, the programme and the city.
2. Keep only invoices with status PAID.
3. Note any invoice still showing as processing. That usually means an ACH payment that hasn't cleared yet.
4. The connector can't read the COMMERCE_PAYMENT object (missing scope), so don't rely on it. If I've exported a HubSpot payments file, use that.

### 1b. Mercury payouts (Mercury connector)
1. List the incoming transactions on the iX USA Mercury account since the last payout we used (11/19/2026).
2. Filter to the HubSpot payouts. The counterparty is HubSpot or Stripe, depending on the descriptor.
3. Note every ACH return as well. Last time that was Nusra Nabwanja on 11/09.

### 1c. Payout mapping (Supabase project qcjuvipewezaghfexkau, table ix_bank_payouts)
1. Each row links a Mercury payout (mercury_date, amount) to its HubSpot invoice numbers. Use it to decide which invoices make up each payout.
2. If a payout is missing from the table, match it this way:
   1. Take paid invoices in date order.
   2. Card payments pay out about 2 business days after payment; ACH payments about 3 to 4.
   3. Find the set whose gross less fees equals the payout.

   Show me any match you're unsure of.

### 1d. Xero (iXperience USA)
1. Find the last invoice number used.
2. List the HubSpot references already invoiced, so nothing gets invoiced twice.
3. Note the current balance of the HubSpot Payments clearing account.

---

## Step 2. Rules for building the files

### Which invoices to include
1. Include an invoice when it is PAID in HubSpot and not already in Xero. Match on the HubSpot number, which sits in Xero's Reference field.
2. Leave out open invoices.
3. An ACH payment that was paid out and then returned gets no invoice. Put the receipt, its fee and the return through 8300/004 so they net to nil.
4. An invoice that has been paid out but still shows as processing in HubSpot gets included. Flag it as a return risk.

### Account codes (all lines Tax Exempt)

| Item | Account |
|---|---|
| Deposit ($950.00 ACH or $983.25 card) | 1010/004 |
| Programme payment, Cape Town | 1010/001 |
| Programme payment, Lisbon | 1010/002 |
| Programme payment, New York or Online | 1010/003 |
| Payout to Mercury | 8300/004 (HubSpot Control) |
| Fees, Cape Town | 2010/026 |
| Fees, Lisbon | 2010/034 |
| Fees, New York or Online | 2010/037 |
| Returned ACH: receipt, fee and return | 8300/004 |

### Telling card from ACH
1. These amounts are ACH (base prices): 950.00, 2725.00, 4520.00, 5260.00, 708.05 and 3250.50.
2. These amounts are card (base plus a 3.5% surcharge): 983.25, 2820.38, 4678.20 and 5444.10.
3. For any other amount, work it out from whether amount ÷ 1.035 gives a round base price.

### Fees
1. The fees in a payout always equal the gross of its payments less the net payout. That total is exact.
2. To spread the fees across students:
   1. Card fees are about 3.475% of the amount.
   2. ACH fees are about 1.375%, capped at $21.50. For $950.00 and $2,725.00 ACH payments the fee is effectively the $21.50 cap or less.
   3. Estimate each payment's fee, then scale them so they add up exactly to the actual fee total for that payout.
3. Group the fees by city, using the city in the deal name.
4. Say where the split is approximate. Last time the ACH fees on $5,260 and $4,520 payments were uncertain.

---

## Step 3. Build the two import files (CSV)

### File 1: Sales invoice import
1. The header must be exactly:
```
*ContactName,EmailAddress,*InvoiceNumber,Reference,*InvoiceDate,*DueDate,*Description,*Quantity,*UnitAmount,*AccountCode,*TaxType,TrackingName1,TrackingOption1,Currency
```
2. Example row:
```
Niall Gillen,,INV-1566,INV-1699,11/03/2026,11/03/2026,Investment Banking New York deposit,1,950.00,1010/004,Tax Exempt,,,USD
```
3. Fill the columns like this:

| Column | What goes in it |
|---|---|
| ContactName | The student's full name. |
| InvoiceNumber | Xero numbers in sequence, starting at the next free number, in HubSpot number order. |
| Reference | The HubSpot invoice number. |
| InvoiceDate and DueDate | Both the HubSpot payment date, as MM/DD/YYYY. |
| Description | "<Programme> <City> deposit" or "<Programme> <City> programme payment". |
| Quantity | 1. |
| UnitAmount | The amount paid. |
| AccountCode | From the table in Step 2. |
| TaxType | Tax Exempt. |
| Currency | USD. |

### File 2: HubSpot Payments bank statement import
1. The header must be exactly:
```
*Date,*Amount,Payee,Description,Reference,Account Code,Tax Type
```
2. The file has these lines, in date order:
   1. **One receipt line per paid invoice.** Positive amount. Payee is the student. Description is "HubSpot ACH payment INV-xxxx" or "HubSpot card payment INV-xxxx". Reference is the Xero invoice number. Leave Account Code and Tax Type blank, because these lines are matched to the invoices.
   2. **One payout line per Mercury payout.** Negative amount. Payee is HubSpot. Description is "Payout to Mercury". Reference is Payout. Account 8300/004, Tax Exempt.
   3. **Fee lines for each payout.** Negative amounts. Payee is "HubSpot fee <City>". Description is "Fee for <student>". Reference is Fee. Account code by city, Tax Exempt.
   4. **For a returned ACH:**
      1. The receipt line, coded 8300/004.
      2. Its fee, coded 8300/004.
      3. A negative return line on the return date, coded 8300/004.
3. Checks before you hand the files over:
   1. For each payout, the receipts in it less its fees equal the payout amount exactly.
   2. The invoice file total equals the receipts in the statement file, excluding returned ACH lines.
   3. Closing clearing balance = opening balance + receipts − payouts − fees ± returns. List which receipts make up that balance (paid but not yet paid out).
   4. The Xero numbers run in sequence with no gaps or duplicates, and no HubSpot reference is already in Xero.
4. Give me both files ready to download, then a short summary:
   1. Invoice count and total.
   2. The payouts covered.
   3. The expected closing balance and what makes it up.
   4. The flags (returns, return risks, approximate fee splits).

---

## Step 4. Import into Xero (I do this)
1. **Invoices first.** In Xero, go to Business, then Invoices, then Import. Upload File 1 and choose the date format MM/DD/YYYY. Leave them as Draft and check the totals, then approve them all.
2. **Then the statement.** In Accounting, go to Bank accounts, then HubSpot Payments, then Import a statement. Upload File 2 and map:
   1. Date to Date.
   2. Amount to Amount.
   3. Payee to Payee.
   4. Description to Description.
   5. Reference to Reference.
   6. Account Code to Account code.
   7. Tax Type to Tax rate.

   Choose the date format MM/DD/YYYY.

## Step 5. Reconcile in Xero (I do this)
1. Match each receipt line to its invoice. Xero suggests the match through the Reference.
2. Payout, fee and return lines are already coded, so just click OK on them.
3. If a receipt for an earlier invoice was imported last week but the invoice is still unpaid, match it to that existing line. Don't import it again.

## Step 6. Check afterwards (you do this, then report)
1. The new invoices exist in Xero with the right count and total, and all are PAID once reconciled.
2. The clearing account balance equals the expected closing balance from Step 3, made up of the receipts waiting for payout.
3. No duplicate HubSpot references.
4. Every invoice date is correct. In particular, no day and month swap like the old INV-1488 and INV-1489, which showed 10 December instead of 12 October.
5. Give me pass or fail for each check, with the invoice number, what it shows and what it should be for anything wrong.
6. Finish by stating the next starting point: the last HubSpot number used and the next free Xero number.
