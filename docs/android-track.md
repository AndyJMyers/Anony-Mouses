# Android track — Anony-Mouses

The website and Android app should feel like the same little nightclub: minimal interfaces, expressive artwork and a little va-va-voom. Adult, playful and a little louche. Introductions create no obligation.

This is the Android development track, not a released app. No Android binary, signing key or store listing has been created. Production service choices apply to both clients.

## Shared interface contract

- Two main destinations: **Sparks** and **Conversations**. Keepsakes sit with conversations; profile details and visibility sit behind the chosen-name control.
- One clear primary action per screen: find a spark, send a hello, accept, or send a message.
- The first interaction is a shared mouse-avatar creator (hair, fur, face shape, facial hair, outfit and accessories). Public profile portraits are always mice, never real-photo uploads. Private permitted pictures remain a separate conversation feature.
- Entry remains one page of details followed by one page for the paid monthly entrance. Login and recovery remain separate utilities.
- The postcode district is the only location input. Map positions represent district centres with decorative offsets, never home/GPS locations or live activity.
- Cream cards, midnight navy, warm gold and small rose accents. Use the established mice artwork, readable type and generous spacing.
- Gentle pulses and a restrained kiss sparkle supply movement. Honour Android system reduced-animation settings and the website's reduced-motion preference. No flashing, autoplay sound or fake online counts.
- Mood choices, surprise introductions and suggested opening lines are optional shortcuts. Patrons author public hints. Messages are sent only after the patron taps Send.
- The same truthful copy on both: adults only, identity claims unverified, no obligation, £50 per calendar month with a £20 website introductory offer and £10 example invitation code, all core features included, optional start within seven days and explicit manual renewal. Discretion has limits.
- Permission requests only when needed: a system photo picker for images, optional notifications after an accepted conversation. No contacts, precise location or background tracking.

## Delivery order

| Stage | Website | Android |
| --- | --- | --- |
| Now | Pages concept preview; locally connected account/message lounge | Establish shared interaction and visual contract; keep native build pending |
| Service foundation | Approved production host, age assurance, portable account/message API | Agree a mobile authentication contract without embedding server secrets or weakening the existing cookie/CSRF flow |
| First device build | Validate the core journey against the hosted test service | Kotlin/Jetpack Compose client: two-page entry, district discovery, requests and text conversations using the same service |
| Private adult trial | Images, 14-day expiry, keepsakes, block/report, recovery/deletion | Same behavior, system photo picker, screen-reader labels, lifecycle handling and safe logout; no sensitive offline message cache by default |
| Release readiness | Paid monthly access, provider checkout, renewal and operating procedures | Confirm current Google Play content/payment rules before deciding store distribution; sign builds, run device tests, publish only after review |

Use one backend and one entitlement model. Native authentication, provider handoffs and any store billing rules must be settled before implementing mobile purchases. Avoid separate Android-only business rules.

## First Android acceptance journey

Two fictional adults on separate devices create profiles, discover by district, request and accept a hello, then exchange a message. A third account cannot read it. Logout removes access; blocking stops contact; expiry and 100-keepsake semantics match the website.

The Android app must not ship a client-only age assertion, production credentials or an unreviewed payment workaround. The present loopback service is development-only and cannot be exposed as a mobile production server.

Avatar parity: use the shared eighteen presets and enum contract, including strong/rugged jaws, clean-shaven/stubble/moustache/beard choices, crew/swept cuts, open-neck shirts and leather jackets. These are styling choices, not verified sex or gender information. Existing saved avatars default to soft face/clean shaven.

Current profile scope: shared avatar creator has no body-size or bust/chest fields. Use the same two open introduction prompts as the website; do not add a partner-measurement questionnaire. No routine reading of conversations is policy; technical server blindness is not implemented.

Map interaction parity: a permanently displayed brass half-dial, turn or use +/−, drag when enlarged, tap reset to fit. No inactivity fade; support keyboard access. Zoom changes the view, not search radius or privacy precision.

Geographic scale parity: start at District, with dial stops Country → Region → County → District → Close. Reset returns to the selected district. Wider context uses bundled coastline data and groups the current search results; zooming the view does not silently widen the search. Nationwide viewport-based discovery is a separate backend task.
