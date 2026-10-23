
            CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, login TEXT UNIQUE NOT NULL, salt TEXT NOT NULL,
                password TEXT NOT NULL, recovery TEXT NOT NULL, joined INTEGER NOT NULL, trial_end INTEGER NOT NULL,
                paid_until INTEGER NOT NULL DEFAULT 0, consent_version TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS payment_events(provider TEXT NOT NULL, event_id TEXT NOT NULL,
                user_id TEXT REFERENCES users(id) ON DELETE CASCADE, amount_minor INTEGER NOT NULL,
                currency TEXT NOT NULL, access_until INTEGER NOT NULL, PRIMARY KEY(provider,event_id));
            CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                csrf TEXT NOT NULL, expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS profiles(user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                alias TEXT NOT NULL, bio BLOB NOT NULL, wants BLOB NOT NULL, district TEXT NOT NULL,
                age_range TEXT NOT NULL, visible INTEGER NOT NULL DEFAULT 1);
            CREATE TABLE IF NOT EXISTS districts(code TEXT PRIMARY KEY, lat REAL NOT NULL, lon REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS conversations(id TEXT PRIMARY KEY, sender TEXT REFERENCES users(id) ON DELETE CASCADE,
                recipient TEXT REFERENCES users(id) ON DELETE CASCADE, status TEXT NOT NULL, created INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS messages(id TEXT PRIMARY KEY, conversation TEXT REFERENCES conversations(id) ON DELETE CASCADE,
                sender TEXT REFERENCES users(id) ON DELETE CASCADE, body BLOB NOT NULL, created INTEGER NOT NULL, expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS attachments(message_id TEXT PRIMARY KEY REFERENCES messages(id) ON DELETE CASCADE,
                data BLOB NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS keepsakes(user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                message_id TEXT REFERENCES messages(id) ON DELETE CASCADE, PRIMARY KEY(user_id,message_id));
            CREATE TABLE IF NOT EXISTS blocks(user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                target TEXT REFERENCES users(id) ON DELETE CASCADE, PRIMARY KEY(user_id,target));
            CREATE TABLE IF NOT EXISTS reports(id TEXT PRIMARY KEY, reporter TEXT, target TEXT,
                reason BLOB NOT NULL, evidence BLOB, created INTEGER NOT NULL, expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS report_attachments(report_id TEXT PRIMARY KEY REFERENCES reports(id) ON DELETE CASCADE,
                data BLOB NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL);
            CREATE INDEX IF NOT EXISTS message_expiry ON messages(expires);
            CREATE INDEX IF NOT EXISTS session_expiry ON sessions(expires);
