# Age and access assessment — 17 October 2026

> **Commercial update, 23 October 2026:** [Current offer](membership-offer.md) is £50 for one month, introductory launch price £10, all core features/ordinary messaging included, optional start within seven days, no automatic renewal. Earlier £10-standard and £1/day-ceiling assumptions below are superseded. Provider quotes must cover both £10 and £50 transactions.

## Decision for the proposed service

**Do not launch the member service on a checkbox/payment-only age gate.** Our pre-launch children's access assessment concludes that the proposed service, without effective age assurance, is likely to be accessed by children. The non-explicit policy is worthwhile but does not establish an exemption. This is an assessment of the planned product, not an Ofcom decision or certification.

Recommend an age-only, account-bound 18+ gate before discovery, profiles or messaging. Prefer an existing trustworthy age credential where suitable; otherwise evaluate selfie estimation with an evidence-based challenge-age buffer and an accessible document/alternative route. Do not arbitrarily choose an estimation cutoff. Keep identity claims between patrons unverified. No age provider is approved, contracted or integrated yet.

This is our proportionate design recommendation, not a claim that every non-explicit dating service must use facial checking or require passports. A route without highly effective age assurance remains possible only with a complete alternative safety case. We have not established that case.

## Scope and evidence

Assessment author: project development review; operator approval and named accountable owner remain to be recorded before launch. Evidence date: 17 October 2026. Scope: UK users of the future website and Android member service, considered together. The static GitHub Pages showcase has fictional demonstrations, no user-to-user backend and no real registrations. It is not evidence that the future service excludes children.

Planned features: pseudonyms, brief bios/preferences, configurable mouse-only profile portraits, outward-postcode district discovery, approximate map pins, accepted hello requests, private text and permitted non-explicit images, 14-day message expiry, 100 keepsakes, £10 manually renewed calendar months. No public activity feed, video, live streaming, monetised creator content, paid sexual services or patron-to-patron payments are planned. Discovery is filtering/sorting, not a behavioural content feed; recommender applicability must be rechecked against the eventual implementation.

Evidence used: repository README/product brief and current local UI/API, founder's agreed non-explicit/no-routine-reading policy, the intended national campaign including adult students, Ofcom's access guidance and dating case study, children's risk profiles and current/upcoming codes listed below. There are no live-user age statistics, supplier effectiveness tests or operational report metrics. Do not invent them.

## Children's access assessment: recorded outcome

| Question | Finding for Anony-Mouses | Reason |
| --- | --- | --- |
| Is the planned member service in scope? | Treat as UK-linked user-to-user service. | Members create profiles and exchange content encountered by other members. |
| Stage 1: can children normally be prevented from accessing it? | **Not demonstrated. Proceed to Stage 2.** | The local adult checkbox is fictional testing. £10 payment and an 18+ rule do not independently establish age. No effective gate exists. |
| Stage 2: are there significant actual child users? | Unknown, not zero as an inference about launch. | No real member service or representative user data. |
| Stage 2: is it of a kind likely to attract a significant number of children? | **Yes, on the planned ungated design.** | Dating, private contact with strangers, images, playful art and broad publicity can attract older teenagers. Student outreach must be restricted to adults but does not prove exclusion of 16–17-year-olds. |
| Overall outcome | **Likely to be accessed by children without an effective gate.** | Proceed with children's risk assessment; do not describe the service as exempt. |

Ofcom's access guidance sections 3–4 and dating case study support this reasoning. The outcome is an inference applied to our design, not a finding that children have used our prototype. After implementing and validating an effective 18+ gate with access controls, reassess the member area; leave a non-explicit informational entrance accessible without requiring identity collection. Assess any remaining child-accessible user content separately. Record reviews after material feature/content/campaign changes or evidence of bypass; review at least annually as an internal baseline.

## Age-assurance applicability: why the ban alone is insufficient

In the currently listed Protection of Children Code, PCU B4 covers services likely to be accessed by children which allow any primary-priority content, or cannot technically remove all such content they determine breaches their terms. PCU B5 addresses certain medium/high priority-content risks. The October-issued successor retains that structure. These are recommended code measures; an alternative route requires demonstrating compliance with the underlying duties, not merely declining the recommendation.

Our present rules expressly prohibit pornography and abuse. They do not yet expressly cover every primary-priority category, including encouragement/instructions for suicide, deliberate self-injury or eating disorders. **Proposed terms work, not a silently adopted new policy:** prohibit those harmful forms, while preserving legitimate discussion, support and reporting. Assess priority and non-designated harms too. Even comprehensive prohibitions require working enforcement and cannot establish that no child can enter.

The 12 October 2026 code amendments are listed by Ofcom as issued but not yet in force on this review date; its directory says they take effect 21 days after issue. Recheck commencement and applicable provisions before launch. Do not substitute the upcoming code for the current one without checking the date.

## Initial children's risk assessment

Method: qualitative likelihood of exposure on the proposed design **without a proven age gate or production enforcement**, combined with potential severity. L/M/H are planning judgments, not measured incident rates or Ofcom labels. Conservative uncertainty does not justify a low residual-risk claim. Each category needs evidence from the deployed controls before approval. Consider younger children as well as 16–17s; older teenagers are particularly foreseeable here. Disability, vulnerability, distress, coercion and repeated exposure can increase harm.

| Harm | Likelihood / impact → initial risk | Project-specific pathway and control needed |
| --- | --- | --- |
| Pornography | H / H → H | Explicit DMs/uploads despite the ban; age gate, effective report/removal and media controls. Text can also be pornographic. |
| Suicide encouragement/instructions | L / H → M | Private coercion after rejection; explicit harmful-content rule, urgent escalation. |
| Deliberate self-injury encouragement/instructions | L / H → M | Manipulative direct contact; same rule and safety escalation, separately assessed. |
| Eating-disorder encouragement/instructions | M / H → H | Appearance-based pressure and private encouragement; separate prohibition, response and evidence. |
| Abuse targeting listed protected characteristics | M / H → H | Sexual orientation/sex/race disclosed through profiles; block/report, sanctions and appeals. |
| Incitement of hatred | L / H → M | Targeted hateful profiles/messages; restrict and remove on credible evidence. |
| Encouragement/instructions for serious violence | L / H → M | Threatening or coercive exchanges; urgent safety escalation. |
| Bullying | H / M → H | Rejection, repeated contact and pile-on via replacement accounts; request acceptance, block and repeat-abuse controls. |
| Graphic human violence/injury | L / H → M | Shock image sent privately; permitted-media rules and removal. |
| Graphic animal/fictional-creature violence/injury | L / H → M | Shock uploads or links; same controls, separate category. |
| Dangerous challenges/stunts | L / H → M | Coercive “prove it” messages; prohibited-content response and escalation. |
| Encouragement of harmful substance use | M / H → H | Pressure around intoxication before a meeting; clear rules and report handling. |
| Body stigma (non-designated) | H / M → H | Dating/appearance judgments and body-shaming; no harassment, block and sanctions. |
| Depression/despair promotion (non-designated) | M / H → H | Manipulation, rejection and isolation; prohibit harmful promotion without banning support conversations. |

Cross-cutting concerns also include grooming, adult impersonation of minors, sexual exploitation, sextortion, stalking, fraud and unsafe off-service meetings. These overlap illegal-content duties; the [illegal-risk register](illegal-risk-register.md) assesses those separately. A ban on messages does not remove contact/meeting risks. District-only location reduces precision but a sparse district, identifying bio or privately shared real photo can still expose someone.

Existing local controls (not production assurance): accepted requests, server-side participant isolation, blocking/report evidence, expiry and approximate district fixtures. Missing: real age gate, operator moderation/removal/suspension tools, response coverage, appeals, production anti-evasion/rate controls, nationwide location privacy, supplier acceptance and tested deletion/backups. Residual risks are **unproven**, not “low”.

## Minimal-data implementation specification, subject to provider acceptance

1. Anonymous visitor reads public information. Create an unpublished pending account using private login, password and recovery code; no mandatory email/phone for the app itself.
2. Before discovery or member content, explain the selected age provider and its data use. Offer the fewest necessary steps, plus an accessible correction/alternative route. No face-search gallery, marketing reuse or routine repeated identity checks merely because a month renews.
3. Use a single-use, account-bound checking session; accept only authenticated server results. Keep result, time, method/policy version and minimal reference. Gate all API routes, including image delivery, not just the browser screen. Fail closed; handle suspected account transfer/bypass proportionately.
4. Do not persist raw provider payloads, images, documents, full DOB, names or confidence ranges in app logs/database. Where upstream data is temporarily returned, minimise before persistence. Verify this is technically and contractually possible, including backups and debug logs.
5. Delete upstream checking material promptly after securely recording the minimal result, subject to justified review needs. Establish a measured deadline and evidence of deletion, including retained templates, subprocessors and backups. Do not use provider defaults unquestioningly.
6. Complete age before taking £10 payment to avoid charging someone who cannot enter. Reuse the valid account-bound adult result for manual renewals unless a justified recheck is needed. Failed checks need a fair, prompt review path without paying for membership first.

Age-only checking is an architectural preference, not “no personal data”: a third-party selfie still involves collection on our behalf. Before use: DPIA, Article 6 basis and any Article 9 condition, provider processing roles/transfer terms, accuracy/bias/accessibility and circumvention evidence, controller contact details and production verification.

## Release gate and accountable review

**Not cleared for real member launch.** This document completes the pre-launch access reasoning and initial children's risk analysis; it does not complete implementation validation or operator sign-off. Keep the public fictional showcase available. Do not start steps 3–5 of the launch plan until the founder has reviewed this conclusion and provider acceptance/costs are resolved.

Required evidence: named responsible operator; reviewed risk records and terms; validated age/access controls or a documented viable alternative; adequate report coverage with no promise of continuous availability unless staffed; provider deletion contract/tests; fair appeal route; and a reassessment on the actual hosted implementation. No regulatory filing or application for an exemption has been submitted.

## Sources checked 17 October 2026

- [Ofcom access guidance, sections 3–4 and Annex 2](https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/statement-protecting-children-from-harms-online/main-document/childrens-access-assessments-guidance.pdf?v=396655).
- [Ofcom access assessment tool](https://www.ofcom.org.uk/os-toolkit/child-access-assessment/childrens-access-assessment-tool).
- [Children's risk guidance and risk profiles](https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/statement-protecting-children-from-harms-online/main-document/childrens-risk-assessment-guidance-and-childrens-risk-profiles.pdf?v=396653), including content categories and design/functionality risks.
- [Current children's code: PCU B4–B5](https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/statement-protecting-children-from-harms-online/main-document/protection-of-children-code-of-practice-for-user-to-user-services.pdf?v=403579).
- [October-issued successor, not yet in force at review](https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/statement-protecting-children-from-harms-online/upcoming-codes-of-practice/issued-protection-of-children-code-of-practice-for-user-to-user-services.pdf?v=426298).
- [Ofcom version/commencement directory](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/online-safety-regulatory-documents).
- [Guidance distinguishing harmful content from legitimate discussion](https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/statement-protecting-children-from-harms-online/main-document/guidance-on-content-harmful-to-children.pdf?v=395445).
