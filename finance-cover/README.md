# Finance Cover Desk

The brain for covering the finance role at **Motion Ads** and **iXperience**, and the FM gap at **Country Hotels**, from **14 October 2026 to about 14 February 2027**.

Live desk: https://claude.ai/artifact/HQ3SHLxUEmrhbyvtdboMhN

## How the day runs

| Time | Block | What happens |
|---|---|---|
| Before 08:00 | Brief | Claude scrubs the inboxes and posts the morning brief to the desk |
| 08:00 to 08:45 | Inbox scrub | Reply to quick ones. Anything needing Xero goes into the capture box |
| 08:45 to 09:00 | Chasing | Copy the chase messages Claude built from Mercury and Xero |
| 12:30 to 12:50 | Midday pass | Urgent only |
| 16:00 to 17:00 | Xero hour | Motion Ads, iX ZA, iX USA daily processing (15 min each), then the request queue |
| 17:00 to 17:10 | Wrap | Set tomorrow's musts |

The rule: **during the day you capture, at 16:00 you process.** A request like "create a PO" goes into the capture box and lands in the Xero hour queue.

Weekly and monthly items (payment run, payroll, EMP201, VAT201, month end, invoicing) appear on the right day automatically. The rhythm follows Melissa's SOPs of 28 September 2026 for Motion Ads, iX ZA and iX USA. Anything tagged **Confirm with SOP** is an open point in those SOPs. Country Hotels has no SOP yet.

## Files

| File | Purpose |
|---|---|
| `brain.json` | Single source of truth: rhythm, SARS deadlines, public holidays |
| `dashboard.template.html` | The desk page |
| `scripts/build_dashboard.py` | Builds `dashboard.html` from the template and `brain.json` |
| `seed/` | Handover checklist and setup items loaded into the desk |

When the SOP arrives: update `brain.json`, run `python3 scripts/build_dashboard.py`, republish to the same URL.

## Desk data (for Claude and routines)

The desk keeps live data in its artifact database. Routines write here so everything shows in one place.

| Collection | Shape |
|---|---|
| `tasks` | `title, entity (motion, ix, ixusa, country, general), block, due (YYYY-MM-DD or null), queue (xero, today, later), must, status (open, done), source (me, claude, handover), notes` |
| `missing` | `entity, source (mercury, xero), person, date, merchant, amount, currency, kind (receipt, invoice, unreconciled)`. Replaced on every check, no manual entry |
| `state/missing` | `checkedAt, sources` |
| `briefs` | `date, title, body` (the latest by date shows on the desk) |
| `replies` | `subject, from, entity, received, summary, draft, triage (reply, xero, forward, fyi), flags, gmailUrl, status (ready, sent, skipped)` |
| `checks/<date>` | `{ruleId: true}` for ticked rhythm items |
| `state/deadlines` | `{deadlineId: {done, at}}` |

## Email replies

Tone, risk rules and reply templates live under `email` in `brain.json`. The desk's **Draft a reply** box uses them to draft in your voice. The morning routine uses the same rules to save drafts in Gmail (it never sends) and lists each one in `replies` for review.

## Key SARS dates in the window

| Due | What |
|---|---|
| Fri 30 Oct 2026 | EMP501 interim (Mar to Aug), iX ZA VAT201 for September |
| Fri 6 Nov 2026 | EMP201 October (iX ZA internal: Thu 5 Nov) |
| Mon 30 Nov 2026 | iX ZA VAT201 October. Motion Ads bi-monthly VAT if Category B |
| Mon 7 Dec 2026 | EMP201 November (iX ZA internal: Fri 4 Dec) |
| Thu 31 Dec 2026 | iX ZA VAT201 November |
| Thu 7 Jan 2027 | EMP201 December (iX ZA internal: Wed 6 Jan) |
| Fri 29 Jan 2027 | iX ZA VAT201 December |
| Fri 5 Feb 2027 | EMP201 January (iX ZA internal: Thu 4 Feb) |
| Fri 26 Feb 2027 | IRP6 second period for February year ends (after the return) |

iX ZA files VAT monthly and targets the 25th with payroll. Motion Ads' bi-monthly VAT months are an open SOP point.
