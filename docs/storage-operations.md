# Storage operations — 23 October 2026

This checkpoint is **fictional staging**, not public production. The same core now supports SQLite and PostgreSQL. The public GitHub Pages site never receives database credentials or customer data. Approved providers, production serving, private external media and operational/reporting/rights controls remain prerequisites for real users.

## Database configuration and migrations

Install `requirements.txt`. Default storage is the ignored local SQLite file. To exercise PostgreSQL, set `ANONY_MOUSE_DATABASE_URL` privately in the process environment; never put a DSN or encryption key in commands, URLs, source, screenshots or public logs. `ANONY_MOUSE_DATA_KEY` must remain the same for data you want to read. The same key also derives shared rate-limit keys; app instances must agree on it.

Psycopg pools have one initial connection, at most eight per process and a bounded wait queue. Total app instances × processes × pool maxima must fit the server's connection budget. Connections have ten-second statement and five-second lock timeouts. Initialise a service after forking, close it during shutdown and do not use preload to share live connections across processes. Deployment pool sizes still require load testing.

Startup takes a migration advisory lock and applies numbered migrations. SQLite legacy additions remain compatible with earlier development fixtures; PostgreSQL receives the current schema. Pair/account/event locks protect payment replay, duplicate introductions and keepsake/image allowances without a single application-wide write mutex. Rate limits are database-backed fixed UTC-hour windows, with HMAC keys rather than stored raw IP addresses. Do not trust arbitrary forwarded-IP headers; production proxy handling is still to be configured.

## Import only outward districts

Run the local server with `--import-demo-districts` to import the bundled 2,988 approximate district centres. This is an idempotent import of **district, latitude and longitude**, not full postcodes or addresses. The connected lounge accepts typed districts with suggestions from the imported index. The source is the dated GeoNames-derived demo atlas: retain [its attribution and limits](demo-atlas.md), and choose/validate a maintained production source before launch. No real accounts are created by importing districts.

## Retention worker

The local development server runs a background worker every 60 seconds, removing up to 500 expired messages, sessions, reports and rate-limit records per class per batch. Expired messages saved as keepsakes are excluded. Access queries hide expired messages/sessions immediately, even if cleanup is behind. Image/report attachment deletion follows foreign-key cascades. This is bounded cleanup, not a guarantee that a large backlog drains in one minute.

A separately supervised worker is available as `python -m backend.maintenance` with environment-held keys/database configuration. `--once`, `--batch-size` (1–5000) and `--interval` (1–60 seconds) support drills and scheduling. Do not start duplicate workers unnecessarily; the database lock serialises cleanup batches. A real deployment needs health/error monitoring and a tested restart policy. The existing 90-day development report rule is **not** the production statutory evidence workflow.

## Encrypted snapshots and restore

`python -m backend.backups snapshot runtime/backups/checkpoint.amb` writes an encrypted snapshot. Supply a **separate** `ANONY_MOUSE_BACKUP_KEY` in the environment as well as the service data key. The destination must not already exist. Files are created with mode 0600 under ignored `runtime/` or outside source; publishing customer dumps inside the repository is rejected. Never commit archives or keys.

Each record is encrypted/authenticated with Fernet and includes an archive ID and sequence number. An authenticated footer confirms all table counts. The writer takes a consistent database snapshot, streams rows (server-side cursors on PostgreSQL), writes no plaintext dump, fsyncs the temporary file and publishes the completed archive under an exclusive filename. A truncated, altered, reordered or mixed archive must fail verification. Do not infer backup-provider durability from a local file.

For a restore drill, provision an **empty** destination with the original service data key and set its private database environment. Run `python -m backend.backups restore <archive-path>`. The destination must contain no data in any imported table, including districts. Restore imports all records in one transaction and checks the original service encryption key. Authentication, schema, sequence or count failures roll back imported data. After a complete import, bounded cleanup reapplies current expiry before the drill is accepted. Original saved keepsakes remain available under the established participant rules.

This same archive provides a SQLite-to-PostgreSQL development migration: snapshot the source, change only the database destination environment to an empty PostgreSQL database, restore with both original keys, then verify accounts, paid periods, conversations, pictures, keepsakes and access isolation. Stop writes during a real cutover, keep the original database intact, and validate/plan rollback before changing traffic. A rollback after accepting new writes requires reconciliation; do not silently switch to a stale snapshot.

The snapshot includes private encrypted message/media payloads, financial fixtures and session hashes. Protect both archive and keys independently. Retaining backups for no more than the proposed 30 days needs an external retention/deletion schedule; this utility **does not** implement that deployment policy or statutory evidence holds. External object-store contents are not implemented yet and must be incorporated into a future backup/restore contract.

## Evidence and remaining work

The CI workflow runs the full functional/concurrency/HTTP suite on SQLite and PostgreSQL 16. Backup drills test round-trip private pictures/keepsakes, wrong keys, missing footer, archive reordering, refusal to overwrite/nonempty restore, expiry after restoration and cross-engine portability. These tests do not measure production throughput, failover or disaster recovery at national scale.

Next: external private media and isolated decoding; a production server/TLS/secret setup; final payment/age adapters and provider acceptance; restricted reports, accounting/deletion and evidence policy; load testing and a hosted adult pilot. Production remains disabled throughout this checkpoint.
