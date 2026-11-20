# Anony-Mouses

**The relationship that admits it is artificial.**

Anony-Mouses is now an adults-only bio-cyber intimacy concept: create a synthetic mouse, tune its temperament and boundaries, and spend a private evening together. The intended arc is arrival after a busy day, unwinding over a drink and food, deepening flirtation and erotic possibility, then an unhurried afterglow. The emotional promise is **a warm hug with a happy after**. The proposed commercial offer is **£1 for 24 hours and up to 100 patron messages**, paid once with no automatic renewal.

The current public build is a transparent, scripted product prototype. It does not contact an AI model, create an account, verify age, retain conversations or take payment.

## Current prototype

- Bio-cyber landing page with a generated adult synthetic-mouse art direction.
- Three configurable companion shells and chosen names.
- Chat-first entry: choose a mouse, give a name and begin; no mandatory calibration sequence.
- Optional tone, boundaries, memory and picture controls stay behind Fine-tune and Settings.
- Chatbot-shaped scripted conversation with a 100-message meter.
- A 100-direction conversation engine used as invisible subtext, not a patron-facing menu or questionnaire.
- Organic pacing: attentive responses and companion self-disclosure between occasional, purposeful questions.
- A provider-neutral `ai-client.js` adapter: production can use the strongest contractually eligible model through a same-origin server gateway, while the scripted engine remains an offline fallback.
- Session-only fact extraction and shared-moment callbacks, so later replies refer specifically to earlier answers without inventing history.
- Cinematic, fully clothed picture beats.
- Participant-directed picture language: one-click moods, a free-text cue or an ordinary chat request shapes periodic visual prompts.
- Every prototype image is labelled as a local concept-library scene and exposes its proposed production prompt.
- Proposed memories that the patron must accept before retention.
- A visible memory drawer with item-by-item and complete erasure.
- A “leave no memory” mode.
- Clear artificial/non-conscious disclosure and crisis limitations.

Open `index.html` directly, or serve the repository root with a static HTTP server. `companion.html` contains the interactive prototype.

## Product compact

Intimacy is the product. The companion may become seductive and erotically charged, but it must also know how to arrive gently and remain close afterwards. The product remains candid about its nature and gives the patron control.

1. **Always artificial.** It never claims to be a human, conscious, physically present, in danger or dependent on the patron.
2. **Adult access.** The intended service is 18+. The checkbox in this prototype is not age assurance.
3. **No emotional hostage-taking.** No guilt for leaving, manufactured emergencies, isolation from people, threats, or vulnerable-moment upselling.
4. **Memory with a window.** Retained memories are visible, editable and erasable. Incognito conversation is available.
5. **Boundaries over momentum.** Patrons can configure and change limits. Illegal, exploitative, underage and real-person impersonation scenarios are excluded.
6. **No therapy claims.** The companion is not emergency, medical or mental-health support.
7. **Honest capability claims.** Scripted previews are labelled. A provider's actual permitted adult-content boundary must be disclosed before payment.

## Commercial shape

| Offer | Proposed terms |
| --- | --- |
| One day | £1 paid once |
| Usage | Up to 100 messages sent by the patron |
| Renewal | None automatically |
| Trial | The £1 day is the trial |
| Longer access | Consider £7 / 7 days and £30 / 30 days only if processor fixed fees make £1 transactions impractical |

Retries and technical failures should not consume quota. The interface warns patrons as the daily message allowance runs down. Live pricing must include clear cancellation/refund information and must not use an invented higher reference price.

## Production architecture

The existing Python service remains a useful but **legacy human-dating foundation**. Its password hashing, opaque sessions, CSRF protection, encryption, migrations, PostgreSQL adapter, payment-event idempotency, expiry workers and encrypted backups are reusable. Human discovery, districts, peer conversations, blocks and peer reports are not part of the pivoted product.

The production companion requires a new service layer:

- age-assurance session and replay-safe result;
- one-day order, verified payment callback, quota and expiry;
- companion configuration and versioned consent/boundaries;
- provider-neutral model gateway with explicit contractual adult-content eligibility;
- a stable `anony-companion-v1` response contract so the underlying model can be replaced without changing the intimate interface;
- a separate image gateway that receives only a minimal structured visual cue, never the raw private transcript;
- prompt and output moderation, companion-appearance continuity and an immediate picture opt-out;
- prompt/policy versioning and evaluation fixtures;
- bounded context, summarisation and cost controls;
- encrypted conversation storage with patron-selected retention;
- transparent structured memory proposals;
- complaint, safety-event and model-incident handling;
- account export/deletion, backup expiry and deletion reapplication;
- monitoring, abuse limits, secrets, TLS and tested restoration.

Do not connect a general model first and negotiate eligibility later. Model-provider permission, payment classification and the intended dialogue boundary are architecture gates.

## Content boundary in this repository

The product is described as erotic and the interface may use charged innuendo, anticipation, consensual power dynamics and seductive imagery. The included demonstration copy and artwork remain non-graphic. A future contracted adult-dialogue provider, legal review and written product policy determine any live explicit boundary; the prototype must not imply that functionality exists before it does.

No generated or user-supplied depictions of minors, non-consensual exploitation, incest, bestiality, real-person sexual impersonation or otherwise illegal content are permitted. “Mouse” refers to a fictional adult synthetic anthropomorphic character, never an animal or child-coded character.

## Privacy

Intimate conversations can reveal sex life, orientation, health, relationships and other highly sensitive information. Production work therefore requires a DPIA, an Article 6 basis, an applicable Article 9 condition where special-category data is processed, processor terms, international-transfer analysis, strict access control and tested deletion. Do not train models on patron chats by default.

The public prototype stores its active conversation only in page memory and loses it when the tab closes. It makes no production privacy guarantee.

## Repository map

- `index.html`, `style.css` — pivoted public proposition.
- `companion.html`, `companion.css`, `companion.js` — interactive scripted companion chamber.
- `conversation-engine.js` — 100 conversation directions, phase progression, session facts and shared-history callbacks.
- `mouse-avatar.js` — reusable SVG mouse renderer.
- `assets/bio-cyber-mouse-hero.webp` — landing hero generated for the pivot.
- `assets/companion-*-signal.webp` — non-explicit chat picture beats.
- `assets/scene-*.webp` — arrival, spark and afterglow concept-library scenes for participant-directed beats.
- `backend/`, `tests/` — legacy dating foundation pending extraction of reusable infrastructure.
- `docs/history/` and the dated dating documents — historical research, not the current product decision.

## Status

This is not a live adult service and is not commercially cleared. See [TODO.md](TODO.md) for the pivot sequence. No open-source licence has been granted.

Project by Andy J Myers.
