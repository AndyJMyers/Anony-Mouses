# Anony-Mouses — initial product brief

## Proposition

A deliberately simple, discreet adult dating service with a sexual focus. A description of who you are, a description of what you want, a configurable mouse avatar as the only public portrait, and private messaging. Membership is £50 for one calendar month, with a £20 website introductory offer and £10 example invitation code, all core features included and no automatic renewal or free trial. A new/lapsed month can start immediately or within seven days of purchase. See [the current membership offer](membership-offer.md) for timing, fair use and price transitions.

## Agreed essentials

- Pseudonymous profiles with mouse avatars only; no public real-photo uploads. Signup begins with choosing hair, fur, face shape, facial hair, outfit and accessories. These optional choices can be fictional.
- No validation of users' identity claims; patrons assess those claims themselves.
- Private text and image exchanges.
- Ordinary messages and attachments expire 14 days after sending.
- Up to 100 keepsake messages per user.
- Privacy aimed at avoiding unnecessary public disclosure, rather than claiming invisibility to service providers or authorities.

## Map discovery UI

Enter a partial postcode (outward code), such as GU2, and explore potential matches on a map. Match markers pulse gently and show short, patron-authored hints about what they seek or offer. Selecting a marker opens a profile and a message-request action.

Use district-level approximate placement, with an explicit explanation that markers are illustrative locations, not homes or live positions. Do not request GPS access or store exact addresses for this flow. Avoid implying somebody is online merely because their marker pulses. Provide a list view and reduced-motion option. Hints are controlled by the patron; do not infer or expose private sexual preferences beyond what they choose to publish.

## Motivation

The primary goal is the fun of making the project. Commercial success and notoriety are optional bonuses. Keep the pilot simple and spending bounded.

## Suggested launch scope

- Adult age range and broad location rather than exact address or public coordinates.
- Message requests, acceptance, blocking and reporting.
- Strip image metadata; compress uploads and limit attachment sizes.
- Discreet notifications with message previews disabled by default.
- Account deletion and a clear explanation of retention.
- Text and still images initially; video and voice would add complexity.

These are implementation proposals, not yet final decisions.

## Decisions before implementation

- Adults-only access and age assurance, considered separately from identity verification.
- Account access and recovery without exposing email or phone details to patrons.
- Whether saving a received message requires the sender's consent, and how withdrawal works.
- Whether the 100 keepsakes include both text and images, and the maximum size of each.
- Precise retention for backups, reported content and deleted accounts.
- Private image access controls and the level of message encryption.
- Geographic launch area, platform and payment route.
- Operational handling of reports and account problems.

## Pilot economics

100 paid months produce £1,000 gross at the invitation price, £2,000 at the website offer or £5,000 at the standard price, before provider fees, refunds, tax and operating costs. These are price scenarios, not forecasts of conversion or retention. Renewal depends on explicit repeat purchases.

The proposed £100 experiment budget should be treated as an initial infrastructure spending cap with a defined stop/review point. It does not cap development time, support labour or all costs of launching an adult dating service.

Expected engagement of one or two hours a day is the founder's hypothesis, to be tested. Time online affects concurrent connections; message counts, image uploads and downloads determine other usage costs.

Short retention bounds accumulated storage. It does not eliminate delivery costs or maintenance. Track active users, peak concurrent sessions, messages, images, reports, spending and new paid memberships during the pilot.

## Launch campaign proposal

Commercial entrance: £50 standard or the £20 website introductory offer and £10 example invitation code, bought upfront for one month with no automatic renewal. Choose immediate activation or a start within seven days. Registration alone does not grant discovery or messaging access. All core features and ordinary messaging are included, subject to disclosed fair-use/safety/storage limits.

The founder proposes tailored launch outreach to every UK student union and every UK MP. This is a future launch plan, not an instruction to send the campaign before the real service is ready. No recipient list has been assembled and no messages have been sent.

Student-union copy should focus on adults-only access, the price, pseudonyms and optional identity disclosure, and invite relevant editorial or society channels to consider sharing it. MP-office copy should present a constituent's software project and local creative enterprise; do not imply that the recipient personally needs an anonymous sexual encounter.

Creative headline concept: “New Anony-Mouses Dating App promises anonymity for all us mices!” Publishable wording should promise discretion and control of disclosure rather than guaranteed anonymity.

Launch strategy: a national cultural push from the outset, led by the distinctive mice artwork and playful proposition. Include creators/influencers, podcasts, journalists and student publications alongside tailored student-union and MP-office outreach. Local match density is a metric to improve after attention arrives, not a reason to constrain the campaign geographically. Attention and conversion remain hypotheses to test; national coverage is an ambition, not a guaranteed outcome. Campaign delivery, recipients and final copy remain to be prepared and reviewed at launch.

## Marketing language

Core brand line: **Adult, playful and a little louche.**

Preserve this tone across the website, launch campaign and artwork: adult glamour, playful humour and a touch of louche flirtation.

## Brand attitude

Relaxed, sophisticated and open to possibilities, with an awareness of pitfalls. Designed for intelligent, experienced adults while welcoming younger adults too: 18+ throughout. Warmth, wit, clear boundaries and room for surprise. A little fizz in your cocktail; check the ingredients mix before making it.

See [the prioritised TODO list](../TODO.md) for the implementation and launch sequence.

## What the service offers

An introduction service for adults: a hello, perhaps a drink, and room to discover mutual chemistry. No promise of romance, sex or a lasting relationship. A conversation creates no obligation to meet or continue; membership never purchases another person’s time or affection. Consent is ongoing and patrons may change their minds. Profiles and identity claims are unverified: caveat emptor, take your time and keep your eyes open.

Make this plain for every adult, including younger or inexperienced patrons, without patronising them. Keep the relaxed, sophisticated, playful voice.

## District lookup scope

Only outward codes/postcode districts such as GU2 are required, not full postcodes or addresses. Store the district code and its approximate centre (latitude/longitude); optional labels can aid display. Distance filtering compares district centres and must be described as approximate. Exact matching treats GU2 and GU20 as separate districts.

A small district table or a server-side outward-code lookup cached on demand is sufficient. Postcodes.io documents an outcode endpoint with averaged district coordinates: https://postcodes.io/docs/outcode/lookup/ and https://postcodes.io/docs/outcode/schema/. An on-demand request should send only the district code, never account IDs, descriptions or messages. No full postcode database, GPS collection or house-address fields are required. Provider/data licensing and availability still need checking before production.

## Brand and domain

Brand: **Anony-Mouses** — the deliberate plural celebrates a community of little mices. Domain owned by the founder: **anonymouses.com**. Domain/DNS connection is a separate deployment task and has not been configured here.

## Confirmed private-content approach — revised 17 October 2026

The [README conduct, privacy and reporting policy](../README.md#conduct-privacy-and-reporting-policy) is authoritative. It supersedes the earlier explicit-image proposal: sexually explicit pictures, videos and written messages are prohibited, including consensual DMs. Flirtation and non-graphic statements of intention are allowed. Any image-sharing functionality is for permitted non-explicit content only; the founder has not adopted a text-only launch restriction.

No routine reading of private conversations. Investigate reports and other credible indications promptly, restrict credible serious risks while reviewing, remove confirmed prohibited material and remove accounts where warranted. No three-strike entitlement for serious or illegal conduct. Make required reports to the NCA/police and preserve evidence lawfully. Distinguish malicious reporting from mistaken or unproven good-faith complaints; provide reasons and review where lawful and safe.

The service remains adults-only. Complete the revised children's access/risk assessments and settle necessary age/access safeguards before changing the planned age gate. Payment and terms alone do not establish children cannot access it. No claim of a regulatory exemption has been made. The development image functionality is not evidence that production moderation or compliance is ready.
