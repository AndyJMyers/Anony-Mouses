
            CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, login TEXT UNIQUE NOT NULL, salt TEXT NOT NULL,
                password TEXT NOT NULL, recovery TEXT NOT NULL, joined BIGINT NOT NULL, trial_end BIGINT NOT NULL,
                paid_until BIGINT NOT NULL DEFAULT 0, consent_version TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS payment_events(provider TEXT NOT NULL, event_id TEXT NOT NULL,
                user_id TEXT REFERENCES users(id) ON DELETE CASCADE, amount_minor BIGINT NOT NULL,
                currency TEXT NOT NULL, access_until BIGINT NOT NULL, starts_at BIGINT NOT NULL DEFAULT 0, offer_code TEXT NOT NULL DEFAULT 'launch', requested_start BIGINT, voucher_code TEXT NOT NULL DEFAULT '', PRIMARY KEY(provider,event_id));
            CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                csrf TEXT NOT NULL, expires BIGINT NOT NULL);
            CREATE TABLE IF NOT EXISTS profiles(user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                alias TEXT NOT NULL, bio BYTEA NOT NULL, wants BYTEA NOT NULL, district TEXT NOT NULL,
                age_range TEXT NOT NULL, avatar TEXT NOT NULL DEFAULT '{}', visible BIGINT NOT NULL DEFAULT 1 CHECK (visible IN (0,1)));
            CREATE TABLE IF NOT EXISTS districts(code TEXT PRIMARY KEY, lat DOUBLE PRECISION NOT NULL, lon DOUBLE PRECISION NOT NULL);
            CREATE TABLE IF NOT EXISTS conversations(id TEXT PRIMARY KEY, sender TEXT REFERENCES users(id) ON DELETE CASCADE,
                recipient TEXT REFERENCES users(id) ON DELETE CASCADE, status TEXT NOT NULL, created BIGINT NOT NULL);
            CREATE TABLE IF NOT EXISTS messages(id TEXT PRIMARY KEY, conversation TEXT REFERENCES conversations(id) ON DELETE CASCADE,
                sender TEXT REFERENCES users(id) ON DELETE CASCADE, body BYTEA NOT NULL, created BIGINT NOT NULL, expires BIGINT NOT NULL);
            CREATE TABLE IF NOT EXISTS attachments(message_id TEXT PRIMARY KEY REFERENCES messages(id) ON DELETE CASCADE,
                data BYTEA NOT NULL, width BIGINT NOT NULL, height BIGINT NOT NULL);
            CREATE TABLE IF NOT EXISTS keepsakes(user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                message_id TEXT REFERENCES messages(id) ON DELETE CASCADE, PRIMARY KEY(user_id,message_id));
            CREATE TABLE IF NOT EXISTS blocks(user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                target TEXT REFERENCES users(id) ON DELETE CASCADE, PRIMARY KEY(user_id,target));
            CREATE TABLE IF NOT EXISTS reports(id TEXT PRIMARY KEY, reporter TEXT, target TEXT,
                reason BYTEA NOT NULL, evidence BYTEA, created BIGINT NOT NULL, expires BIGINT NOT NULL);
            CREATE TABLE IF NOT EXISTS report_attachments(report_id TEXT PRIMARY KEY REFERENCES reports(id) ON DELETE CASCADE,
                data BYTEA NOT NULL, width BIGINT NOT NULL, height BIGINT NOT NULL);
            CREATE INDEX IF NOT EXISTS message_expiry ON messages(expires);
            CREATE INDEX IF NOT EXISTS session_expiry ON sessions(expires);

CREATE UNIQUE INDEX IF NOT EXISTS voucher_once ON payment_events(user_id,voucher_code) WHERE voucher_code != '';
CREATE INDEX IF NOT EXISTS payment_access ON payment_events(user_id, starts_at, access_until);
