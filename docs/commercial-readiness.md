# Commercial readiness: age, hosting and payments — 17 October 2026

> **Commercial update, 23 October 2026:** [Current offer](membership-offer.md) is £50 for one month, introductory launch price £10, all core features/ordinary messaging included, optional start within seven days, no automatic renewal. Earlier £10-standard and £1/day-ceiling assumptions below are superseded. Provider quotes must cover both £10 and £50 transactions.

## Outcome

**Research completed; commercial acceptance remains outstanding.** No account/application, enquiry, purchase, provider contract, KYC submission or live integration has been made. Public terms are evidence of possible fit, not approval of Anony-Mouses. We cannot honestly mark steps 1–2 fully closed until the operator reviews the assessment and providers answer the specific scope/cost/privacy questions.

The [age/access assessment](age-access-assessment.md) recommends a minimal 18+ gate for the proposed member area; a prohibition-only alternative is not established. Retain the non-explicit/no-routine-reading policy. Do not start deployment, moderation implementation or real-user testing under this research task.

## Provider decision

| Component | Published evidence checked | Decision / unresolved condition |
| --- | --- | --- |
| Public showcase: GitHub Pages | Existing fictional showcase remains hosted separately. | Keep current domain/DNS. No live membership or private data on Pages. |
| Member host: IO Zoom | Self-managed KVM 4GB: $18/month, 4 CPUs, 40GB SSD, 4TB transfer. VPS adult-content policy allows lawful adult content subject to US law. London is advertised. | Continue as first pilot candidate, subject to exact regional stock, taxes/renewal, full scope acceptance, processor terms, support/logs and backup details. No paid control panel required. |
| Backups/private storage | Main host page advertises daily off-server snapshots; backup KB describes internal-use backups. | Not resolved. Require independent encrypted application/database restore, exact locations, retention/deletion and actual cost. Do not budget $0 or promise a 30-day cap before confirmation. |
| Age: Didit | Age estimation $0.10 including passive liveness; ID verification $0.15; full KYC bundle $0.33. November 1 plan advertises pay-as-you-go and eligible $10 monthly shared credit. | Evaluate the smallest age-only hosted flow, not full KYC by default. Need adult-dating acceptance, credible accuracy/buffer/fallback/accessibility evidence and contract/deletion confirmation. No credit assumed in budget. |
| Age privacy | Verification privacy notice says general retention defaults to unlimited; configurable 30 days–10 years. Optional biometric-template retention can survive operational session deletion. Help centre describes immediate session deletion, while legal notice describes deletion requested until all in-scope stores confirm purge/beyond-use handling. | **Acceptance blocker:** no indefinite defaults, no retained biometric gallery/template, short documented upstream deletion including fallback, backups and independent-controller exceptions. Marketing descriptions of selfie-only deletion are insufficient. |
| Payments: CCBill | Advertises dating support. Pricing lists Visa $950/year and Mastercard $1,000/year for applicable high-risk MCCs. Its VIRP guidance includes dating MCC 7273, a $950 initial application charge and additional Visa transaction assessments. | First specialist quote candidate; exact UK merchant classification, fee applicability/frequency, reserves, GBP settlement, hosted checkout, privacy and manual monthly purchases need written confirmation. Banning pornography does not remove dating's MCC by itself. Do not add application/annual charges together without clarification. |
| Payments: Stripe | Dating is restricted and subject to diligence; adult-content/services are prohibited. Its linked FAQ includes sexually oriented dating services in adult restrictions. | **Do not select standard Stripe checkout or use its headline tariff as our budget.** Only pursue a truthful written classification of our actual sexual-focus/non-explicit model; never relabel it as generic software to gain acceptance. |

Public routes: [IO Zoom plans/pre-sales](https://www.iozoom.com/linux-vps/), [CCBill sales](https://ccbill.com/contact) (sales@ccbill.com), [Didit contact](https://didit.me/solutions/age-verification/) (hello@didit.me), [Stripe contact sales](https://stripe.com/contact/sales). These are researched routes, not completed submissions. IO Zoom's dedicated contact page returned a challenge during research; no browser bypass or form submission was attempted.

## Pilot arithmetic, not quotes

USD supplier costs and GBP receipts remain separate; no live FX is assumed. At 100 paying patrons buying a £10 month, receipts are £1,000 gross before refunds, tax and costs. Verification attempts can exceed paying patrons; renewals should not automatically repeat a valid age check.

| Scenario | Host USD/month | Age cost USD | Known subtotal USD |
| --- | --- | --- | --- |
| 100 estimation attempts, 10% fallback at an additional $0.15 | 18 | 11.50 | 29.50 |
| 100 attempts, 10% fallback at an additional $0.33 full-KYC list price | 18 | 13.30 | 31.30 |
| 1,000 attempts, same $0.15 fallback assumption | 18 | 115 | 133 |
| 1,000 attempts, same $0.33 fallback assumption | 18 | 133 | 151 |

The 10% fallback rate is a scenario, not our measured rate. $0.15 is a document-module assumption, not a verified total fallback price; the full-KYC illustration is not a guaranteed upper bound. Retries, additional liveness/face matching, human review, tax and other modules can add costs. Configure no unnecessary AML/PEP, face search, behavioural tracking or marketing re-engagement just because bundled features exist. Provider-required controls must be evaluated rather than silently disabled.

If both published high-risk annual scheme fees apply, $1,950/year is $162.50/month when spread for planning, potentially payable upfront. At only 100 members, that is material before processing fees. Reserves also tie up cash. **The £100 experiment remains possible for limited technical evaluation, not an established paid-launch budget.** The £1 day pass remains deferred; minimum ticket and fixed fees need a separate answer.

For comparison only, Stripe's standard UK-card headline rate is 1.5% + 20p, or 35p on £10; 100 such transactions would cost £35 before other charges. That arithmetic is **not an available offer for our service**, and scheme/high-risk terms must not be assumed included or waived. Do not put it in the launch forecast as an accepted rate.

The calculator's fallback price is now configurable, defaulting to the more conservative $0.33 illustration. All models exclude independent backups/storage expansion, tax, processor transaction/dispute/refund fees, reserves, support and labour. Existing historical provider notes use the earlier $0.15 assumption; this dated decision takes precedence.

## Required written answers before committing money

**Host:** actual plan/region and total recurring/renewal cost; confirmation that our non-explicit adult introductions with permitted private images is accepted; subprocessors/data locations, UK processing/transfer contract, network/security logs and retention; deletion on cancellation, abuse process, disk/transfer overages; whether listed snapshots are customer-restorable and their off-server locations/retention. Get a concrete independent backup quote and restore procedure.

**Age:** hosted age-only 18+ flow, account binding, signed result without identity payload persistence; challenge-age/fallback evidence, bypass testing and accessibility; adult-dating acceptance; cost of each completed/failed/retried/fallback/review step and minimum spend after November 1; raw-media/result/template/log/backup retention and complete erasure semantics; DPA, entities, countries, subprocessors and transfer safeguards. No facial-recognition gallery or cross-service identity dossier. Do not call any provider “Ofcom approved”.

**Payments:** exact UK MCC and written acceptance of actual purpose/content/reporting model; sole-trader/company eligibility and merchant KYC; all setup/application/annual and scheme fees, per-transaction/fixed/international/FX fees and whether Visa assessments are included; reserves/holdback, GBP settlement/payout/minimum ticket; chargebacks/refunds and unused-service cancellation treatment; hosted card entry and exact buyer fields collected; statement descriptor; manual single-month payments without rebilling; image-review/depicted-person requirements and whether report-led private review is accepted; national campaign restrictions. No creator payouts, paid sexual services or content sales are part of our model.

## Handoff and closure criteria

Ready-to-submit, supplier-specific wording is in [provider-enquiries.md](provider-enquiries.md). It discloses the sexual focus and implementation status honestly. Sending it is not an account signup or purchase. Required operator details for actual submissions/onboarding: confirmed legal trading entity (sole trader or company), business jurisdiction and reply/contact address; providers may require registered/business address and merchant owner KYC through their secure process. Do not put home address, identity documents, bank details or credentials in this public repository.

| Gate | Evidence needed | Status |
| --- | --- | --- |
| Pre-launch access conclusion and initial risks | Dated reasoning against actual non-explicit scope | Prepared; owner review and deployed-control evidence outstanding |
| Age approach accepted | Founder choice of age-only gate or substantiated alternative; provider scope/privacy/effectiveness accepted | Outstanding |
| Hosting commercial route | Written scope/region/processing/backup terms and total quote | Outstanding |
| Payment commercial route | Written scope acceptance and complete fee/reserve/settlement quote | Outstanding |
| Safe to proceed to next build/deploy steps | Gates above resolved, material cost review completed | Not yet |

## Sources checked 17 October 2026

- [IO Zoom plans](https://www.iozoom.com/linux-vps/), [VPS adult policy](https://www.iozoom.com/client/knowledgebase/2/Do-you-allow-adult-content.html), [backup KB](https://www.iozoom.com/client/knowledgebase/21/Do-you-provide-backups.html).
- [Didit prices](https://didit.me/pricing/), [November changes](https://didit.me/blog/new-pricing-november-2026/), [verification privacy notice](https://didit.me/terms/verification-privacy-notice/), [deletion help](https://help.didit.me/end-users/your-data), [age workflow marketing](https://didit.me/solutions/age-verification/).
- [CCBill pricing](https://ccbill.com/pricing), [dating/MCC and VIRP](https://ccbill.com/doc/visa-integrity-risk-program-virp), [annual-fee FAQ](https://ccbill.com/doc/visa-and-mastercard-payment-processing-faqs), [sales contact](https://ccbill.com/contact).
- [Stripe restricted businesses](https://stripe.com/legal/restricted-businesses), [linked adult/dating FAQ](https://support.stripe.com/questions/prohibited-and-restricted-business-list-faqs), [standard UK pricing, comparator only](https://stripe.com/gb/pricing). FAQ text was accessible in indexed official search results; direct opening failed. Treat the adverse classification as reason to require clarification, not as a personalised rejection already received.
