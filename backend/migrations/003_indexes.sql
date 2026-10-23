CREATE INDEX IF NOT EXISTS profile_district_visible ON profiles(district,visible,user_id);
CREATE INDEX IF NOT EXISTS district_lat_lon ON districts(lat,lon,code);
CREATE INDEX IF NOT EXISTS message_thread_time ON messages(conversation,created,id);
CREATE INDEX IF NOT EXISTS conversation_sender_time ON conversations(sender,created,id);
CREATE INDEX IF NOT EXISTS conversation_recipient_time ON conversations(recipient,created,id);
CREATE INDEX IF NOT EXISTS block_target_user ON blocks(target,user_id);
CREATE INDEX IF NOT EXISTS keepsake_message_user ON keepsakes(message_id,user_id);
CREATE INDEX IF NOT EXISTS report_expiry ON reports(expires,id);
CREATE INDEX IF NOT EXISTS message_sender ON messages(sender,id);
CREATE UNIQUE INDEX IF NOT EXISTS conversation_pair ON conversations(
 (CASE WHEN sender < recipient THEN sender ELSE recipient END),
 (CASE WHEN sender < recipient THEN recipient ELSE sender END));
