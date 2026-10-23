# Anony-Mouses — priorities and TODO

Current offer updated 23 October 2026; earlier checkpoints below are dated history. See [the membership decision](docs/membership-offer.md).

## Goal

Keep the established atmosphere: **adult, playful and a little louche**. Build a small real adult dating service behind the prototype, then launch nationally with distinctive creative and tailored outreach. Making it is part of the pleasure; revenue and notoriety are possible bonuses.

## Already done

- [x] Public GitHub repository and live HTTPS GitHub Pages concept preview.
- [x] Technicolor mouse artwork and coherent responsive visual design.
- [x] Fictional postcode map, pulsing markers, profile hints and map/list views.
- [x] Demo details-to-payment journey, scripted chat and session-only keepsakes.
- [x] Agreed direction: £10 paid up front per calendar month, explicitly renewed; no public free trial.
- [x] National launch ambition and core brand language captured.

These are completed design/concept tasks. The preview does not yet provide real accounts, geographical search, messaging, membership or payment.

## Implementation status — 14 October 2026

- [x] Preview pricing now £10/calendar month paid up front with manual renewal; core brand line added.
- [x] Hosting/payment/age/privacy foundation review and provider enquiry brief prepared: [review](docs/foundation-review.md).
- [x] Hosting growth paths and specific local-backend limits reviewed: [hosting and growth](docs/hosting-and-growth.md).
- [ ] Before real users: PostgreSQL persistence, pagination/indexed discovery, shared rate limits and portable private media storage.
- [ ] Rehearse a second app instance, data migration/restore and representative burst-load tests; obtain actual provider quotes and acceptance.
- [x] Local persistent account, district-discovery and private text-message core built: [backend](backend/README.md).
- [x] Twelve tests pass, covering the two-account flow and access/retention boundaries.
- [ ] Suitable production host and payment account approved; age assurance integrated.
- [ ] Polished live UI connected to backend; district lookup coverage and secure image handling added.
- [ ] Production retention, payment entitlement/webhooks and operational testing completed.

The local API is deliberately not deployed publicly and is not wired into the GitHub Pages mockup. The fixture postcode data and adult checkbox are for fictional testing only. The first end-to-end **API** milestone is tested; the real-user website milestone remains open.

## Ordered priorities

| Order | Priority | Work | Completion evidence |
| --- | --- | --- | --- |
| 1 | Now | Align the public preview with £10/month paid up front; add the core brand line. Preserve its visual character. | Website, checkout demo and README agree on pricing and renewal terms. |
| 2 | Before backend commitment | Confirm a hosting and payment route suitable for the actual adult dating service and intended user-uploaded content. Define 18+ access, reporting duties and privacy approach using current authoritative guidance. | Providers accept the described business/content; implementation choices, baseline monthly costs and launch obligations documented. |
| 3 | First working milestone | Accounts, login/recovery, editable profiles, public image and real outward-postcode discovery with approximate map placement. | Two test adults can sign in separately, edit their profiles and discover each other without exposing contact details or precise location. |
| 4 | First working milestone | Private message requests, text and image messaging, block/report, upload limits and image metadata removal. Decide encryption before storing real exchanges. | The two test adults can exchange messages; a third account cannot read them; blocking and reporting work. |
| 5 | Before taking users | Implement 14-day expiry, 100 keepsakes, account deletion and disclosed backup/reported-content retention. | Time-controlled checks demonstrate expiry, keepsake limits, removal and deletion behavior including attachments. |
| 6 | Before paid launch | Paid-month entitlement, payment-provider checkout, verified payment events, monthly access and explicit renewal. Preserve one page of details then one entrance/payment page. | Test payments grant the correct access; duplicates cannot grant it twice; expiry and renewal behave predictably. |
| 7 | Before campaign | Operational trial across desktop and phones; spending alerts, capacity check, recovery exercise and report handling. | A small private test cohort completes the core journey; spending and support work are visible and manageable. This is testing, not a geographically limited marketing launch. |
| 8 | In parallel, release after readiness | Prepare national campaign: influencer/creator press kit, student publication/union copy, podcast/journalist pitches and distinct MP-office copy. Build a reviewed contact list and appropriate sending process. | Finished creative and tailored copy, checked recipients and campaign delivery plan; no unreviewed mass send. |
| 9 | Launch and learn | Launch nationally; monitor signup, activity, conversations, paid conversion, renewals, reports and costs. | Decisions use observed results, while keeping public anonymity claims honest. |

## Decisions to settle

- [x] No public free trial; registration starts unpaid.
- [x] Renewal: £10 explicit purchase each calendar month; no automatic charging.
- [ ] What remains available after membership expires: profile visibility, old conversations, keepsake access and deletion.
- [ ] Whether a sender can withdraw a message/image saved by another patron; explain that downloaded copies/screenshots cannot be recalled.
- [ ] Keep actual identity claims unverified, while choosing workable adults-only access and account recovery.
- [ ] Filters and matching: interests, age ranges, distance and mutual preferences; keep the initial controls small.
- [ ] Public hints must be patron-authored and approved by them; never infer or expose private preferences.
- [ ] A £100 initial infrastructure experiment cap and a clear review point; do not treat it as a cap on development/support labour or all launch expenses.

## Keep for later

- Native mobile apps, video/voice calls, elaborate recommendation systems and paid boosts.
- Additional artwork before core behavior works; the present artwork already establishes the brand.

## Next development objective

Resolve production provider/content/age-assurance choices, then connect the polished interface to the tested core: **two accounts → discover → request a conversation → exchange a private message**. Add private images and real district lookup coverage before live-user testing.

GitHub Pages remains the static concept showcase. Real membership, sensitive exchanges and payment require suitable production hosting and backend services.

## Connected lounge milestone — 14 October 2026

- [x] Same-origin local member UI: two-page registration/entrance, login and recovery-code handoff.
- [x] Profile editing/hiding, district discovery with schematic pulsing markers, requests/acceptance, private text, 100 keepsakes, block/report and deletion.
- [x] Local server serves an explicit asset allowlist; source/runtime files remain inaccessible.
- [x] HTTP integration checks exercise separate session cookies and exclude a third patron.
- [x] anonymouses.com configured and verified in GitHub Pages, with HTTPS enforcement.
- [ ] Production host and PostgreSQL migration, provider approval and age assurance.
- [ ] Private image attachments and metadata removal, national district coverage, payment integration and live-user readiness checks.

The local interface uses fictional adult accounts. The Pages showcase does not call the backend or open public registration.

## Android track — shared minimal interface

- [x] Establish [the Android track and shared interface contract](docs/android-track.md).
- [ ] Keep website and Android aligned around Sparks and Conversations, with quiet secondary controls.
- [ ] Settle hosted API/mobile authentication and current distribution/content/payment requirements.
- [ ] Build the first Kotlin/Compose device client against the shared test backend.
- [ ] Match images, expiry, keepsakes, block/report, recovery and deletion across clients before release.

Visual excitement comes from the mice, colour, gentle pulses and optional playful shortcuts—not extra screens, mandatory questionnaires or fake activity. Native Android development follows the production service foundation; no Android app has been built or published yet.

## Provider and monthly-payment checkpoint

- [x] Provisional hosting/age/payment selection with sourced cost model and prepared vendor questions: [provider decision](docs/provider-decision.md).
- [x] £10/month paid-upfront public copy; manual renewal; £1/day ceiling reserved for a later evaluation.
- [x] Unpaid registration and internal idempotent paid-month ledger; no browser-granted access.
- [x] Concrete [deployment plan](docs/deployment-plan.md), preserving GitHub Pages and proposing same-origin app.anonymouses.com.
- [ ] Obtain provider acceptance, billing classification/quote, required operator accounts and credentials.
- [ ] Real age/payment adapters, PostgreSQL/production serving, private media, verified backup restore and real-adult trial.

## Private-image checkpoint

- [x] Patron-selected pictures in accepted local conversations; no pre-supplied private imagery.
- [x] Server byte/pixel/format limits, metadata removal and encrypted attachment storage.
- [x] Authenticated delivery, participant isolation, blocking, shared 100-keepsake limit and 14-day expiry.
- [x] Separate reported-image evidence retention and account-deletion/expiry cleanup checks.
- [ ] Production private object store, isolated decoding workers, live age/content/provider requirements and backup retention.

Twenty-two tests now cover the local core/HTTP interface. The real service remains undeployed; image functionality is available only in the local test lounge.

## Privacy and UK legal checkpoint — 17 October 2026

- [x] Add sourced plain-English [data and privacy statement](README.md#data-and-privacy-statement), mapping minimum fields to purpose, recipients and retention.
- [ ] Before real users: final controller/contact details, named provider contracts/roles/countries/retention and UK transfer safeguards; DPIA, lawful-basis/consent records and rights/age-appeal process.
- [ ] Implement production expiry and backup deletion; define dormant-account and sender/recipient keepsake/deletion rules; separate tax ledger from removable accounts. The README's new operational limits are proposed targets, not implemented guarantees.
- [ ] Implement the current NCA CSEA reporting workflow and regulation 8 evidence preservation, including associated data: one year for specified material/data and five years for report references. The development 90-day report timer is insufficient for these cases. Establish valid sensitive/offence-data conditions and restricted access.
- [ ] Remove external Google Fonts requests or serve fonts locally before member launch; publish the finished notice in website and Android, not only GitHub.

## Agreed conduct-policy revision — 17 October 2026

- [x] Record the [non-explicit, private-conversation and accountable-reporting policy](README.md#conduct-privacy-and-reporting-policy); supersede the prior explicit-image plan in the product brief and provider/deployment scope.
- [ ] Assess age/access safeguards for the revised service; no automatic age-check exemption or removal is authorised by the content ban alone.
- [ ] Implement prompt restricted report review, content removal/account restrictions, serious-case escalation, decision reasons/review, statutory reporting/preservation and protection for good-faith reporters. Distinguish knowingly false/abusive reports from unproven allegations. These operating processes are not yet production-ready.

## Steps 1–2 research checkpoint — 17 October 2026

- [x] Prepare dated children's access conclusion, initial children's risks and minimal-data age-gate specification: [assessment](docs/age-access-assessment.md).
- [x] Prepare the current 18-priority-kind [initial illegal-risk register](docs/illegal-risk-register.md), with unvalidated residual risks and remaining code/control review clearly identified.
- [x] Recheck provider fit/prices/privacy and prepare specific enquiries: [commercial decision](docs/commercial-readiness.md), [enquiry packet](docs/provider-enquiries.md).
- [ ] Operator review/sign-off, effective-control evidence and complete current-code applicability review; finalise age approach. Do not infer legal clearance from the research documents.
- [ ] Obtain written supplier scope/privacy acceptance and complete hosting/payment quotes under confirmed legal operator/contact details. Not sent or obtained yet.
- [ ] Resolve those gates before beginning later implementation/deployment/testing steps.

## Current offer checkpoint — 23 October 2026

- [x] £50 standard calendar month / £10 introductory launch month; upfront single purchase, no automatic renewal. Earlier price ceilings superseded.
- [x] Public preview price/fair-use wording and 0–7-day illustrative start-date selector; no real payment.
- [x] Local ledger validates offer-specific prices, preserves existing paid time, schedules a month up to seven days later and excludes not-yet-active patrons from discovery. Existing test-ledger migration and duplicate-event checks included.
- [x] Provider enquiry brief, Android contract and cost scenarios align with the current offer. No enquiries sent.
- [ ] Set and publish launch eligibility/end conditions before live sales; do not imply £50 is an established previous selling price.
- [ ] Real server-created orders/callback reconciliation, cancellation/refunds and applicable express early-start request; exact receipt dates/timezone and production fair-use limits.
- [ ] Validate the whole hosted journey and applicable safeguards before opening paid access.

## Mouse-first public profiles — 23 October 2026

- [x] Shared instant SVG mouse creator with hair/fur/build/bust-or-chest/outfit/accessory options, shown first in signup.
- [x] Remove public photo-upload selector; fictional map/list/profile portraits use mice.
- [x] Persist and edit validated mouse configuration in local profiles; older test accounts receive defaults. Reject arbitrary avatar URLs/markup.
- [x] Keep real permitted picture messages private and separate from public mouse portraits; update privacy/provider/Android contract.
- [ ] Match the shared avatar contract in the future native Android client.

## 23 October — ready-made mice and invitation codes

- [x] Twelve tasteful, fully clothed adult mouse presets with editable styling, shared by public and local member interfaces. Public real photos remain excluded.
- [x] Current offer supersedes the earlier £10 general launch price: £50 planned standard, £20 website offer, £10 example KEELE_SU_10 invitation through 30 November 2026 (UK time).
- [x] Public illustrative code entry; authenticated local quote; exact-price, expiry, per-account redemption and idempotency tests in the development ledger.
- [ ] Agree real partner permission/campaign conditions; do not imply Keele affiliation. Bind campaigns to real server-created orders and implement payment/refund reconciliation before live sales.
- [ ] Set a genuine end condition for the general website offer before advertising a deadline.
