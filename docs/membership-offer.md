# Membership offer — agreed 23 October 2026

This decision supersedes earlier £25 joining offers, the £10 standard monthly price and the £1/day ceiling. It applies to website and Android. The live member service is not open; public pages demonstrate the proposed offer and take no payments.

## Price and purchase

- **Standard: £50 for one calendar month. Introductory launch offer: £10 for one calendar month.** Paid upfront, all core features included, with no per-message charge or automatic renewal. Necessary access/age-check costs must be included in the displayed consumer total, not surprise supplements.
- No free trial. Each further month requires an explicit purchase at the price shown then. A launch purchase does not confer a perpetual £10 renewal rate. The operator has not set a launch-offer end date/eligibility rule; settle and display those before live sales. Do not invent a deadline or imply £50 is a previously charged price.
- Sell service access and the possibility of meeting someone. No guaranteed introduction, response, partner, encounter or sexual outcome. No paid boosts, message credits or undisclosed feature fees in the core offer.
- One calendar month starts at the agreed start time, not the first of a named month. Month-end dates clip to the next month's last valid day. The chosen start and exact expiry must appear before payment and in the receipt, with a clear timezone. The development ledger uses UTC timestamps; production should display them consistently for the patron.

## Start now, or within seven days

A new or lapsed patron chooses immediate activation or a start up to seven days after purchase. Payment is collected upfront; discovery visibility, sending hellos and new messages begin only at activation. Waiting does not consume the paid calendar month. Store the chosen start and expiry, not a reason, moving itinerary, exact future address or speculative profile of plans. A patron can choose/edit an outward postcode district; it is not a claim about current physical presence. No GPS or moving-status field is required.

An early explicit repeat purchase appends a month to already-purchased access so existing time is not lost. The first/lapsed purchase can use the seven-day delay; it does not let someone postpone an already bought renewal indefinitely. If a lapsed start leaves a gap, access must actually be inactive in that gap. Changing a paid start after purchase is not implemented or promised; cancellation rights remain separate.

Age/access eligibility should be settled before charging. Preserve the selected purchase price/start on a server-created order. Authenticate and reconcile provider events; browser redirects cannot activate membership. Retries must neither move the original dates nor add a second month. A delayed callback must use the order's original purchase context, not silently recalculate from callback time. Real order creation/payment integration remains pending.

The public demo shows an optional 0–7-day selector and illustrative start/expiry dates. The local ledger supports actual scheduled test entitlement through the operator fixture; creating an unpaid test account does not itself book a paid start.

## All included, ordinary messaging without a quota

Public wording: **All core features included. No per-message fees or ordinary conversation quota. Fair use applies.**

Fair use addresses spam, automation, mass solicitation, harassment, evasion and traffic that degrades service. Apply proportionate temporary throttling, investigation or account restrictions with reasons and review where appropriate. No routine reading of private conversations is introduced by fair-use enforcement. Do not silently sell “unlimited” and then impose an ordinary monthly conversation allowance or charge for extra messages.

Safety and technical limits remain: accepted conversation requests, rate limits, maximum message/file size, permitted image formats, storage safeguards, 14-day ordinary-message expiry and 100 keepsakes. The local prototype currently has a 300-text-send/hour HTTP throttle, 2,000-character text limit, 60-image-attempt/hour throttle and bounded image storage. Production limits and fair-use terms must be shown clearly before purchase; these development settings are not a verified production capacity promise. The non-explicit conduct policy continues to apply.

## Mouse-first profiles

Before entering other details, patrons create a mouse avatar using optional hair, colouring, build, bust/chest, clothing and accessory choices. All public profile portraits are mice; public real-photo upload is not offered. The default is ready to use, and styling need not reflect the patron's real appearance. Store configuration choices, not a generated identity photograph. Real permitted non-explicit pictures remain private conversation attachments; recipients can still copy them.

## Tone

A little fizz in your cocktail. Choose your company, check that the ingredients mix, and decide together what happens next. Adult, playful and a little louche. Profiles and identity claims remain unverified: caveat emptor. Consent is ongoing and no conversation creates an obligation. Avoid promises of consequence-free sex, guaranteed anonymity, chemistry or safety.

## Consumer terms before live checkout

Use “introductory launch offer” and “planned standard price £50”, rather than an unsupported crossed-out “was £50” or claimed saving. Establish genuine launch eligibility/end terms and actually honour the intended later price if advertised. Source: [ASA introductory-price guidance](https://www.asa.org.uk/advice-online/promotional-savings-claims.html).

A seven-day deferred start does not remove statutory cancellation rights or reset the ordinary service-contract cancellation clock from purchase to activation. For a qualifying distance service contract, disclose the applicable cancellation/refund rights and obtain the required express request before starting within the cooling-off period. Merely beginning a month does not automatically extinguish all cancellation rights. Implement appropriate cancellation and any permitted proportionate charge calculation before taking money; neither exists in the development payment ledger. Sources: [Consumer Contracts Regulations, Part 3](https://www.legislation.gov.uk/uksi/2013/3134/part/3), [government guidance](https://assets.publishing.service.gov.uk/media/5a817b92ed915d74e33fe73a/bis-13-1368-consumer-contracts-information-cancellation-and-additional-payments-regulations-guidance.pdf). Confirm final legal classification/terms at launch; do not substitute draft future auto-renewal rules for this manually purchased month.
