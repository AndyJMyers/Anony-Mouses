# Member-service deployment plan

This plan uses the provisional selections in [provider-decision.md](provider-decision.md). No server has been provisioned. The current service remains loopback-only and production-disabled; do not reverse-proxy it onto the Internet.

## Policy prerequisite — 17 October 2026

Follow the [agreed non-explicit conduct/reporting policy](../README.md#conduct-privacy-and-reporting-policy). The former explicit-image scope is superseded. Assess children's access and risks under the actual revised design before deciding whether/how to retain age assurance; do not remove safeguards on the strength of a terms-only ban. References to the age provider below remain conditional design work, not a finding that a specific check is mandatory for the revised service. Add restricted report review, prompt removal/suspension, documented decisions and appeals, malicious-report handling and statutory NCA evidence/reporting workflows before real users. Do not routinely read private conversations; access to investigate credible concerns must be necessary and controlled.

## Topology

- **anonymouses.com:** existing GitHub Pages showcase. Retain its current DNS/HTTPS configuration.
- **app.anonymouses.com:** proposed member UI plus authenticated API, served by one production app origin. Create DNS only after the backend and TLS are ready.
- **PostgreSQL:** private service/network, outside individual app processes; indexed/paginated accounts, conversations and messages.
- **Private media:** storage abstraction with authenticated delivery and bounded uploads. Select a compatible external object store when its content policy, minimum cost and region are confirmed. The 40GB VPS disk is not a permanent media solution or a capacity promise.
- **Provider-hosted age/payment pages:** server-created sessions/orders with signed, reconciled results. Public clients never get provider secrets, and a successful browser redirect never grants access.

## Commercial entry

One page of details creates a pending account/profile draft, not public discovery access. The second entrance page explains the £50 standard month / £10 introductory launch month, age-check handoff and payment. Age assurance completes before sensitive content access; payment clears before membership becomes active. Failed/abandoned checks do not publish the profile. The provider handoffs may involve their own screens; do not promise literally two screens end-to-end.

A server-validated offer-bound £50 standard or £10 introductory launch purchase grants one calendar month. A new/lapsed purchaser may choose a start up to seven days after payment; an early renewal preserves already-paid time. Month-end dates clip to the target month's last day. A new payment extends access; a duplicate event does not. Manual renewal only. The earlier £1/day ceiling is superseded by the [23 October offer](membership-offer.md). No automatic renewal; show the actual price/start/expiry before each purchase.

## Implementation order

1. Port the tested core to PostgreSQL with versioned migrations, connection pooling, database constraints, bounded cleanup and paginated message/discovery queries. Keep export/restore independent of the host.
2. Introduce a production HTTP server, HTTPS, secure cookies, trusted proxy/host checks and shared rate limits. Keep the same-origin member UI. Do not expose SQLite/wsgiref or a development access override.
3. Integrate the selected age workflow with a single-use account-bound session, authenticated callback, replay protection and an auditable policy version. Store only the required over-18 result/reference; settle upstream retention separately.
4. Integrate single-payment checkout: server-side order amount/currency, signed notifications and provider reconciliation, unique event/order records, account binding, refunds/chargebacks and no hidden recurring mandate.
5. Add image limits/validation, re-encoding/metadata removal, authenticated delivery, report evidence and expiry/keepsake accounting. Require age-cleared, paid entitlement on relevant routes.
6. Implement tested encrypted backups and restoration, expiry after restoration, secret/key custody, operator report access and a named reporting/support route.
7. Invite a limited adult cohort only after provider acceptance and all above behavior is verified on the actual host. Measure spending/verification attempts, latency, errors and restore results; no scalability claim from customer counts alone.

## Existing implementation checkpoint

The local core now creates unpaid accounts and tracks £50 standard / £10 introductory launch calendar months and scheduled starts through an internal, idempotent payment ledger. The ledger is not a payment verification adapter. An operator-only local fixture command exercises it; no public API can grant access. Historical `trial_end` database fields are retained for compatibility but no longer confer membership.

Before live payments the ledger needs durable provider/order reconciliation and refund/chargeback behavior, including retained/tombstoned financial event IDs after account deletion. The current development deletion behavior is not a production accounting policy.

The public preview demonstrates the new price but never collects money. Real provisioning/onboarding requires operator identity, provider accounts and credentials; the selected provider's legal/financial onboarding must be completed by the operator.
