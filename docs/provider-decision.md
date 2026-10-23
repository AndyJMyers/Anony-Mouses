# Provider decision and pilot cost — 14 October 2026

> **Commercial update, 23 October 2026:** [Current offer](membership-offer.md) is £50 for one month, introductory launch price £10, all core features/ordinary messaging included, optional start within seven days, no automatic renewal. Earlier £10-standard and £1/day-ceiling assumptions below are superseded. Provider quotes must cover both £10 and £50 transactions.

> **17 October 2026 review supersedes the earlier explicit-image and pricing assumptions below.** See [the current age/access assessment](age-access-assessment.md), [initial illegal-risk register](illegal-risk-register.md), [commercial-readiness decision](commercial-readiness.md) and [ready-to-submit enquiries](provider-enquiries.md). No supplier acceptance or complete quote has been obtained.

## Scope update — 17 October 2026

The [agreed policy](../README.md#conduct-privacy-and-reporting-policy) now prohibits sexually explicit content in profiles and DMs. This supersedes the earlier explicit-image assumptions below. Historical prices are not new quotes for this revised service. Reclassify the actual non-explicit adult introductions service with each candidate; do not assume a prohibited-content policy automatically changes payment fees, provider acceptance or age-assurance duties. No enquiry has been sent.

## Decision

Keep anonymouses.com on GitHub Pages for the public showcase. Prepare the live member service at **app.anonymouses.com**, with its UI and API on the same origin. This preserves cookie/CSRF isolation without inventing a cross-origin shortcut. That subdomain is proposed, not deployed or added to DNS.

Use **IO Zoom KVM 4GB self-managed VPS** as the first hosting candidate, **Didit adaptive age assurance** as the first technical evaluation, and **CCBill PSP** as the payment-classification/quote candidate. These are provisional selections: no provider account, contract, acceptance, credentials or purchase is in place.

The commercial offer is now **£10 per calendar month, paid up front, with explicit monthly renewal**. No public free month, no automatic charge. £1/day is the ceiling for a possible later day pass; it is not implemented or advertised as available.

## Published prices and fit

| Component | Finding | Selection / remaining check |
| --- | --- | --- |
| IO Zoom VPS | KVM 4GB: $18/month, 4 vCPU, 40GB SSD, 4TB bandwidth. Its VPS policy explicitly allows legal adult content subject to US law; shared hosting does not. | Select this plan for a small pilot, subject to regional stock, taxes/checkout and full use-case acceptance. No cPanel, Plesk or website-builder purchase is needed. |
| Backups | The Linux VPS page advertises off-server daily snapshots. A separate support article describes internal-only backups. | Get retention/restore terms confirmed; do not equate a snapshot with a tested PostgreSQL restore. Additional independent encrypted backups remain unpriced. |
| Didit age assurance | Age estimation lists $0.10/check including passive liveness; adaptive document fallback lists another $0.15 when used. | Evaluate the hosted age workflow with an appropriate conservative threshold/fallback. Vendor claims are not proof that our eventual implementation satisfies Ofcom. Confirm adult-dating acceptance, accuracy evidence, UK suitability, retention and data region. Prefer an over-18 decision without importing identity documents into our app. |
| Didit pricing change | From 1 November 2026 it announces a no-minimum pay-as-you-go plan and $10 monthly shared credit, subject to eligibility; age estimation remains $0.10. | Budget without free credit until eligibility is confirmed. Do not assume today's advertised 500 free full-KYC checks make age checks free. |
| CCBill | Publishes adult-dating support; exact transaction rate/reserves need a quote. Its pricing page lists annual Visa $950 and Mastercard $1,000 high-risk registrations, applying to certain MCCs. | Do not open a paid merchant arrangement until the service's MCC and applicable fees are confirmed. If both apply, $1,950/year is $162.50/month when spread for planning, but may be payable up front. |

Published tariff details are not quotes, availability promises or workload guarantees. Hosting selection is based on a direct policy match; the operational/data-processing terms still need acceptance. London/Frankfurt are advertised locations, not proof this exact plan is available there. The US-law condition remains relevant regardless of server location.

## Cost model

Use USD for vendor costs and GBP for subscription receipts. No live exchange rate is assumed. The included calculator only combines them if an explicit planning conversion is supplied.

Illustration: one age-estimation attempt per new patron, 10% document fallback, no free credit, no optional white-label features. The fallback share is a planning assumption; retries and extra checks add cost.

| New verification attempts in a month | VPS | Age checks | Subtotal before backup/tax/payment/support |
| --- | --- | --- | --- |
| 100 | $18 | $11.50 | $29.50 |
| 1,000 | $18 | $115 | $133 |

100 paying monthly patrons generate £1,000 gross monthly receipts. This is revenue, not profit; processor costs, applicable tax, age checks, refunds, backups and operations must be deducted. Verification attempts can exceed paying patrons. Do not assume a publicity spike is free or that one VPS serves any arbitrary audience.

CCBill card-scheme registration, if applicable, can exceed the founder's £100 experiment budget before a payment is collected. The experiment budget can fund a limited infrastructure/age-assurance evaluation, not a verified commercial launch at those fees. A £1 day pass needs a separate transaction-fee/minimum-ticket check and is deferred.

CCBill's AUP also restricts unsolicited bulk email, including campaigns sent through another provider to promote a covered merchant. Our national publicity plan needs provider-compatible delivery; a lawful campaign is not automatically acceptable to every processor.

## Provider questions ready for enquiry

**Hosting:** Confirm this exact VPS and a UK/EU region support pseudonymous adult dating with an enforced prohibition on sexually explicit content, permitted non-explicit private images, encrypted messages, PostgreSQL, private media and independent encrypted backups. Specify data-processing terms, snapshot retention/restore, renewal taxes, overage, backup options and any content obligations. No bulk email would be sent from the VPS.

**Age assurance:** Confirm an age-only hosted flow for this service, the applicable borderline buffer/accuracy evidence and alternative accessible methods. Give the complete per-attempt/fallback/retry price and free-credit eligibility after November 1; specify retention, deletion, region, processor terms, availability and service acceptance. We want a signed over-18 result, not public identity validation.

**Payments:** Classify the revised adult introductions service with non-explicit private messages/images and a genuine ban on pornography, rather than just the landing page. Quote MCC, all scheme/onboarding fees, transaction/fixed fees, reserve, payout, refund/chargeback and minimum-ticket costs for £10 monthly single purchases. State obligations for depicted-person age/consent/content review, private exchanges and publicity campaigns. Can a manual £1 day purchase be supported economically? No automatic rebilling is requested.

These enquiries are prepared, not sent. Legal operator/contact details are needed for actual onboarding. No card or identity information has been submitted.

## Sources

- IO Zoom VPS plan: https://www.iozoom.com/linux-vps/
- IO Zoom adult-content policy: https://www.iozoom.com/client/knowledgebase/2/Do-you-allow-adult-content.html
- IO Zoom backup caveat: https://www.iozoom.com/client/knowledgebase/21/Do-you-provide-backups.html
- IO Zoom locations: https://www.iozoom.com/datacenter/
- IO Zoom terms: https://www.iozoom.com/terms-of-service
- Didit price list: https://didit.me/pricing/
- Didit adaptive workflow: https://didit.me/solutions/age-verification/
- Didit November pricing: https://didit.me/blog/new-pricing-november-2026/
- Didit billable checks: https://help.didit.me/billing-credits/what-counts-as-billable
- CCBill adult services: https://ccbill.com/industries/adult-business
- CCBill pricing: https://ccbill.com/pricing
- CCBill AUP: https://ccbill.com/cs/client/policies/ccbill/acceptable_use.html
