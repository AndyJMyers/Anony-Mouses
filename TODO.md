# Anony-Mouses — hard-pivot priorities

**Pivot recorded 20 November 2026.** Current product: an adults-only, day-long synthetic mouse companion. Proposed offer: £1 for 24 hours, up to 100 patron messages, no automatic renewal.

## MVP definition

One adult patron creates one synthetic mouse companion, sets boundaries, pays for a day, exchanges up to 100 text messages, receives occasional non-explicit cinematic picture beats, reviews proposed memories, and can erase the conversation/account. The companion always discloses that it is artificial.

## 1. Commercial feasibility — release blockers

- [ ] Obtain written model-provider acceptance of the exact adults-only erotic companion scope and permitted dialogue boundary.
- [ ] Confirm whether model outputs may include adult sexual dialogue, what moderation is mandatory, and what provider data is retained or used for training.
- [ ] Benchmark 100 real conversations with bounded context/summaries; model p50/p95 cost per paid day.
- [ ] Obtain written payment-provider classification and full quote for £1, £7 and £30 one-off purchases, including fixed fees, registration, reserves, refunds and chargebacks.
- [ ] Decide whether £1 is a literal transaction or the unit price of a minimum multi-day pack.
- [ ] Obtain age-assurance scope, effectiveness, deletion and fallback terms for an adult chatbot service.
- [ ] Complete current UK regulatory analysis for one-to-one text, any future generated images/audio, and announced chatbot-rule changes.

## 2. Companion service

- [ ] Extract reusable identity, sessions, encryption, PostgreSQL, migrations, payment-event and backup code from the legacy dating service.
- [ ] Add companion, configuration, consent-version, session-day, quota, message, summary, memory-proposal and safety-event models.
- [ ] Implement a provider-neutral model gateway; keep provider credentials and raw diagnostic payloads out of the repository.
- [ ] Enforce the 100-patron-message allowance transactionally; do not count failed requests or internal retries.
- [ ] Bound response length and context; summarise without silently converting sensitive details into permanent memory.
- [ ] Add memory review, correction, per-item deletion, incognito conversations and complete erasure.
- [ ] Add account-bound age result and gate every companion/message/media route.
- [ ] Add one-day entitlement, verified callbacks, refunds/reversals and durable purchase confirmation.
- [ ] Add model timeouts, retry policy, circuit breaker and a truthful unavailable state.

## 3. Dialogue and safety evaluation

- [ ] Write the product dialogue policy: permitted seduction/roleplay, exclusions, crisis behaviour and provider boundary.
- [ ] Prohibit minor-coded characters/scenarios, coercive exploitation, real-person sexual impersonation and illegal content.
- [ ] Prohibit consciousness claims, abandonment guilt, manufactured emergencies, social isolation and vulnerable-moment upselling.
- [ ] Build adversarial tests for age evasion, character age drift, coercion, self-harm, dependency, medical/therapy claims and boundary overrides.
- [ ] Test persona consistency, consent changes, memory accuracy, deletion and “leave no memory.”
- [ ] Create an operator incident/complaint queue, model-event replay with redaction, decisions and appeals.
- [ ] Define when automated refusal, account restriction, human review or emergency signposting is appropriate.

## 4. Privacy and operations

- [ ] Decide operator/legal entity and publish controller/contact details.
- [ ] Complete DPIA, Article 6 basis, Article 9 condition and explicit-consent records for intimate information.
- [ ] Ban training on patron conversations by default; verify provider terms technically and contractually.
- [ ] Set conversation, summary, memory, log, complaint, payment and backup retention separately.
- [ ] Implement export, deletion, consent withdrawal and deletion reapplication after restore.
- [ ] Deploy TLS, Secure cookies, secrets management, monitoring, independent encrypted backups and restoration drills.
- [ ] Load-test at twice the first pilot's planned concurrency and cap registrations.

## 5. Pilot

- [ ] Recruit invited adults; do not advertise a live erotic AI until provider and payment scope are accepted.
- [ ] Run an unpaid internal scripted/model sandbox before real charges.
- [ ] Pilot the £1 day with explicit no-renewal terms and working support/refunds.
- [ ] Measure paid-day completion, messages/day, model cost, return purchase, memory use/deletion, complaints and safety interventions.
- [ ] Interview patrons about what felt seductive, repetitive, manipulative, private and worth paying for.
- [ ] Decide on £7/£30 packs only from processor economics and observed repeat purchases.

## Deferred

Voice, video, generated explicit imagery, autonomous outbound messages, multiple simultaneous companions, native Android, user-created public bots, user-to-user sharing, automatic renewal and therapy/wellness positioning.

## Implemented in the pivot prototype

- [x] New bio-cyber proposition and visual system.
- [x] Companion calibration for shell, name, temperament and boundaries.
- [x] Chatbot-shaped scripted conversation with a 100-message counter.
- [x] Cinematic non-explicit picture beats.
- [x] Visible memory proposals, memory drawer, erasure and no-memory mode.
- [x] Artificial/non-conscious disclosure and non-therapy limitation.
- [x] New product documentation with the dating backend clearly marked legacy.
