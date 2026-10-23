CREATE TABLE IF NOT EXISTS rate_limits(key TEXT NOT NULL,window_start BIGINT NOT NULL,count INTEGER NOT NULL,PRIMARY KEY(key,window_start));
CREATE INDEX IF NOT EXISTS rate_limit_expiry ON rate_limits(window_start);
