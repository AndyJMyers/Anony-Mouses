# Local backend foundation

This Python API is for fictional adult test accounts on your own computer. The member lounge connects to it locally; it is not connected to the public GitHub Pages demo and is not a public production service.

## Implemented and tested

- Persistent pseudonymous accounts; scrypt password hashes, opaque sessions and CSRF tokens.
- A separate chosen profile name and private login handle; no email or phone required in this development model.
- A one-use recovery code, rotated on recovery; old sessions are revoked.
- Editable profiles, hiding, and distance-based discovery using imported **outward postcode centres**.
- Conversation requests and acceptance before text/image messaging.
- Access checks preventing a third account from reading or saving another conversation.
- Server-side encryption at rest for profile descriptions, text messages and report evidence. **Not end-to-end encryption**; the server holds the key.
- Blocking, reporting (including after blocking), and account deletion.
- Accounts start unpaid. A trusted internal offer-bound GBP £50 standard / £20 website offer / £10 example invitation monthly-payment ledger grants a calendar month, clips month-end dates and ignores duplicate provider events. A new/lapsed month may start up to seven days later, with no active access/discovery visibility before that start. Early renewals preserve existing paid time. No payment-grant HTTP endpoint exists. The ledger does not verify actual provider payments.
- Text and image messages expire after 14 days. Only the individual patron who saves an expired message can read their keepsake; saving does not retain it in the other person's inbox. Limit: 100 per patron.

## Run locally

From the repository root, use Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export ANONY_MOUSE_DATA_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
python -m backend.server --seed-test-districts
```

Keep the same data key if reusing the database; losing it makes encrypted data unreadable. The key is supplied through the environment, not committed. Put persistent runtime state outside the repository. Never use this developer key setup for public deployment.

The server listens only at `http://127.0.0.1:8080`; it serves the website and JSON API from the same origin. Open **http://127.0.0.1:8080/members.html** for the connected member lounge. Cookies and CSRF remain on this origin; no cross-origin API URL is accepted. The public Pages copy of the lounge is disabled. `--seed-test-districts` imports three deliberately approximate fixtures: GU2, GU1 and SW1A. Nationwide district lookup coverage is still required, through a small outward-code table or cached district lookups. No full postcode/address database is needed. These fixture coordinates must not be presented as production geography.

Tests:

```bash
python -m unittest discover -s tests -v
```

Cleanup:

```bash
python -m backend.server --purge
```

Reads also run expiry cleanup, but a real service needs a scheduled cleanup task. Report evidence has a separate **development-only 90-day rule**. Production report retention and backup expiry are unresolved. Account deletion removes shared conversation data and keepsakes via cascading deletion; independently retained report evidence is anonymised and follows its own expiry. These semantics need product review before real use.

## Try the connected lounge

1. Start the server with `--seed-test-districts`, then open `/members.html` at the loopback address above.
2. Choose **Come on in**, enter invented adult details, then create the unpaid test account. Save the one-time recovery code.
3. Open a separate browser profile or a private window for a second invented account. Ordinary tabs share a session cookie.
4. Add an operator-only fictional payment fixture for each login using `python -m backend.server --grant-test-month LOGIN` (same database and data key; no money moves). Then search GU2 or GU1, send a hello, and accept it from the second account's Conversations view.
5. Exchange text and test pictures, save/remove keepsakes and refresh or reload to confirm persistence. The open Conversations view polls every 10 seconds while visible.
6. Edit/hide profiles, block, submit a local test report, recover access, or delete an account using the corresponding controls.

No public signup, real payments or full district coverage is enabled. Private image uploads work only in the loopback test lounge. Reports remain local test records, without a monitored support inbox. No real personal or sexual data should be entered.

## Private test pictures

- Accepted conversations only; a third account cannot retrieve the bytes even with the URL.
- Still JPG/PNG/WebP, up to 5 MB and 12 million decoded pixels. Animated or invalid inputs are rejected by the server.
- Re-encoded to a fresh JPEG, at most 1600 pixels on the longest edge and 1 MB. Orientation is applied, source EXIF/GPS/text/ICC/XMP and filenames are discarded; transparency is flattened onto white.
- Encrypted attachment bytes are kept in SQLite for this local checkpoint. This is not end-to-end encryption or the final production media store.
- 60 upload attempts/hour per test account and a 100 MB encrypted attachment allowance per sender. Report evidence follows a separate rule.
- Image messages count as one of the same 100 keepsakes. Expired bytes are only accessible to the individual keeper; removing the last expired keepsake deletes the ordinary attachment.
- Blocking removes access for both participants; account deletion cascades through shared attachments. A reported image is copied into encrypted evidence for the separate development-only 90-day retention, including after account deletion, then purged.
- Retrieval uses authenticated `/api/images/{message_id}` with private/no-store headers. No original files, public uploads, user-controlled filesystem paths or source filenames are retained.
- The recipient taps **View picture** before display. This does not prevent screenshots or copying. Unchanged conversation polls do not reload image bytes.

These checks do not certify age, depicted-person consent or lawful content. Live age assurance/provider acceptance and an operational content/report process remain required. Use synthetic test images only. Production processing also needs worker/resource isolation and a backup retention policy; the present in-process decoder is not a public upload service.

## API

JSON POST requests require `Content-Type: application/json`; the image-upload route accepts raw bytes with `image/jpeg`, `image/png` or `image/webp`. Authenticated mutations also require the `X-CSRF-Token` returned by login. Sessions use an HttpOnly, SameSite=Strict cookie. No CORS is enabled.

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/api/districts` | GET | Imported district centres for the local schematic map |
| `/api/health` | GET | Confirms development mode |
| `/api/register` | POST | login, password (12+ characters), alias, bio, wants, district, age_range, adult=true, consent=true |
| `/api/login` | POST | login, password; returns CSRF token and cookie |
| `/api/recover` | POST | login, recovery_code, new password |
| `/api/session` | GET | Own profile, monthly access status and CSRF token |
| `/api/logout` | POST | Revoke current session |
| `/api/profile` | GET / POST | Read or edit own profile |
| `/api/discover` | POST | district, radius_km (1–200) |
| `/api/conversations` | GET / POST | List conversations or request one with target account ID |
| `/api/conversations/{id}/accept` | POST | Recipient accepts |
| `/api/conversations/{id}/messages` | GET / POST | Read or send body text |
| `/api/conversations/{id}/images` | POST | Raw binary JPG/PNG/WebP upload with authenticated cookie and CSRF header |
| `/api/images/{message_id}` | GET | Authenticated, per-patron visibility check and private image bytes |
| `/api/keepsakes` | GET | Own saved messages |
| `/api/keepsakes/{id}` | POST / DELETE | Save or remove a keepsake |
| `/api/block` | POST | Block target account ID |
| `/api/report` | POST | target, reason, optional message_id |
| `/api/account` | DELETE | Delete current account |

## Still required

Production hosting, age assurance, provider checkout/webhooks, paid entitlement, production private object storage and image-worker isolation, national postcode data, production UI deployment, moderation tools, durable rate limits, a production HTTP server, TLS, Secure cookies, encryption-key management/rotation, backup/recovery and operating procedures.

An `adult=true` flag is only a fictional-test assertion. It is **not** production age assurance. There is no payment or age-verification override endpoint. Attempting to initialise the service in production mode fails closed. The development HTTP server must not be exposed through a reverse proxy or port forwarding.

## Current offer and deferred development fixtures — 23 October 2026

See [the membership decision](../docs/membership-offer.md). The default local offer is `website` (£20); `standard` is £50. All ordinary messaging is included subject to the disclosed technical/fair-use limits; no per-message charging is added.

Use `python -m backend.server --grant-test-month LOGIN --offer standard --start-in-days 7` to record a fictional standard-price month with a delayed start. Omit the last two options for an immediate website-price fixture. The same database and key are required. No money moves. Existing payment rows are migrated additively; old fixtures retain access. Membership responses distinguish scheduled, active and expired access. Only active periods appear in discovery.

The real provider must validate a server-created order's price/offer/start and purchase time, then reconcile signed callbacks idempotently. The local helper checks its chosen start relative to fixture time; it is not an implementation of delayed real callbacks, cancellation/refunds or commercial launch eligibility. No HTTP parameter can grant membership.

## Public mouse portraits — 23 October 2026

Signup starts with the mouse creator. Profiles persist only enumerated avatar choices: fur, hair, hairColour, build, chest, outfit, colour and accessory. A shared SVG renderer serves website and local UI; Android must use the same option contract. Defaults migrate older test accounts. The server rejects unknown avatar values and public photo-URL fields; it has no public-profile image upload route. Editing the profile saves the selected mouse. These choices are an optional alter ego, not verified physical attributes. Permitted private picture messages remain isolated from discovery/profile portraits. Twenty-nine automated checks cover the local core/HTTP journey.

### Development invitation codes

Authenticated `POST /api/quote` with `{"voucher_code":"KEELE_SU_10"}` returns £10 before 1 December 2026 UTC, or rejects an expired/already-redeemed code. This sample implies no union affiliation and is not a reserved order. `python -m backend.server --grant-test-month LOGIN --offer website --voucher KEELE_SU_10` records a fictional discounted payment; it never charges money. Codes are one use per account, cannot stack, and do not enable access before the chosen start. `launch` is retained for historical fixtures only. See the membership offer for real-order, reversal and retention work still required.

## Returning members

The lounge restores authenticated sessions on load. Optional “Keep me signed in on this device” on signup/sign-in uses an opaque HttpOnly, SameSite=Strict cookie and matching server-side expiry of 30 days. Without it, the cookie is session-only with a seven-day server limit (browser session-restore features may restore session cookies). Sign out revokes the current token; recovery revokes all tokens. The homepage checks the same local API to offer Continue; no identity or credentials enter localStorage. Remembered sign-in does not grant or renew paid access. Production HTTPS must set Secure cookies (the adapter adds Secure for an HTTPS origin); production remains disabled.
