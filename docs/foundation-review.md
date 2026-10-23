# Foundation review — 14 October 2026

> **Commercial update, 23 October 2026:** [Current offer](membership-offer.md) is £50 for one month, introductory launch price £10, all core features/ordinary messaging included, optional start within seven days, no automatic renewal. Earlier £10-standard and £1/day-ceiling assumptions below are superseded. Provider quotes must cover both £10 and £50 transactions.

> **17 October 2026 review supersedes the earlier explicit-image and pricing assumptions below.** See [the current age/access assessment](age-access-assessment.md), [initial illegal-risk register](illegal-risk-register.md), [commercial-readiness decision](commercial-readiness.md) and [ready-to-submit enquiries](provider-enquiries.md). No supplier acceptance or complete quote has been obtained.

## Implementation direction

Preserve the existing static design. Keep production backend code portable rather than tied to GitHub Pages or a payment provider. A small self-hosted service is a candidate; no commercial host has been purchased or approved for this particular project. The Python/SQLite core is local development only and is not a final production stack decision.

## Payment finding

Stripe distinguishes restricted dating services from prohibited adult content/services. Online dating is a restricted category; adult live-chat features and sexually explicit content designed for sexual gratification are in prohibited categories. Given Anony-Mouses's stated sexual focus and planned DM image exchanges, treating a normal Stripe signup as automatic approval would be a mistake. Obtain an explicit classification of the complete service.

CCBill explicitly advertises support for adult dating and UK payment services. It is the first candidate for a quote and business-model assessment, not an approved merchant account. Obtain onboarding fees, card-scheme fees, transaction rates, rolling reserves, payout timing, minimum charges, refund/chargeback costs and any content-verification obligations. A £10/month offer cannot be assessed using an ordinary card-processing rate alone.

Sources:
- https://stripe.com/legal/restricted-businesses
- https://ccbill.com/industries/adult-business
- https://ccbill.com/industries/dating

## Hosting finding

NovoServe explicitly permits legal adult content on its dedicated servers, subject to jurisdiction and its policies. It is a verified policy-fit candidate, not a budget recommendation; dedicated hosting may be excessive for this pilot. A smaller suitable host still needs to be selected with explicit acceptance of the actual content model. Cloudflare's pass-through/CDN role is distinct from hosting, and provider terms must be checked per service rather than assuming a CDN implies storage approval.

No provider has yet approved Anony-Mouses, and no complete monthly operating quote is available. The £100 cap remains an initial infrastructure experiment target, not a verified public-launch budget. Age checks, payment onboarding and human operations may materially affect it.

Sources:
- https://novoserve.com/knowledge-base/what-is-your-policy-on-adult-content
- https://www.cloudflare.com/trust-hub/abuse-approach/

## Adults-only access

Ofcom's dating-service guidance says highly effective age assurance is required where pornography is permitted, including in private messages. A checkbox alone cannot be the planned gate for such a service. Preserve pseudonyms and unverified public identity claims while separating them from age assurance. Ideally the service receives an over-18 attestation and does not retain identity documents. Actual provider integration, data flows and suitability remain to be chosen.

The image/content policy must be explicit before provider applications: non-explicit dating imagery only, or consensual explicit adult exchanges with the corresponding operational requirements. Do not quietly assume the former when the founder intends the latter. Age assurance must cover every patron before sensitive access; payment is not a substitute.

Source:
- https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/dating-and-social-discovery-know-the-online-safety-risks-rules-and-how-to-comply

## Privacy

Descriptions of sex life or sexual orientation can be special-category personal data even under a pseudonym. Document an Article 6 lawful basis and an Article 9 condition; explicit consent is a candidate, not a blanket replacement for a proper privacy assessment. Profile publication and private messaging need distinct, clear visibility rules. Public hints are written and published by the patron, not inferred.

The local backend uses encrypted description/message/report fields, no email or telephone collection, hashed session tokens, private logins separate from display names, and district centres only. Encryption at rest is not end-to-end encryption or a guarantee of anonymity.

Sources:
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/special-category-data/
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-are-the-conditions-for-processing/

## Provider enquiry brief — ready to adapt, not sent

Anony-Mouses is a proposed UK adults-only dating service with a sexual focus. Patrons use pseudonyms, an outward postcode and a profile image, and exchange private text and images after a conversation request is accepted. Identities presented to other patrons are unverified. The intended membership is £10 for a calendar month paid up front, with an explicit new purchase for each renewal and no public free trial. A possible day pass is capped at £1/day and is not yet enabled. Ordinary messages expire after 14 days; up to 100 messages per patron may be retained as keepsakes. Blocking, reporting, account deletion and separate reported-content retention are planned.

Please assess whether you support this model, including the intended possibility of consensual explicit private image exchanges. Specify required age assurance, content moderation/verification, merchant identity checks, permitted countries, retention requirements, fee/reserve structure and integration options. Please distinguish the patron's public pseudonym from any identity information required by your service.

No enquiry has been sent, no account opened and no fees committed. Founder identity/business details and a final content policy are needed for actual onboarding.

## Growth and transition

See [hosting and growth due diligence](hosting-and-growth.md) for the hobby-to-large-service path, provider-route comparison, illustrative workload, current code limitations and migration acceptance gates. The recommended production direction is portable app instances, PostgreSQL and private S3-compatible media storage; this remains subject to vendor/content acceptance and quotes. The local SQLite backend should not be described as a million-customer architecture.

## Provider selection update

See [the provider decision](provider-decision.md) for the current IO Zoom/Didit/CCBill shortlist, sourced tariffs and conditional card-scheme fees. No accounts or purchases have been made.
