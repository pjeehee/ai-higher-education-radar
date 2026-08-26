CREATE TABLE sources (source_id TEXT PRIMARY KEY, name TEXT, official_domain TEXT, priority TEXT, family TEXT);
CREATE TABLE candidates (candidate_id TEXT PRIMARY KEY, source_id TEXT, url TEXT, title TEXT, discovered_at TEXT, fingerprint TEXT, status TEXT);
CREATE TABLE evidence (record_id TEXT PRIMARY KEY, institution TEXT, topic TEXT, title TEXT, fact TEXT, source_url TEXT, authority TEXT, verified_at TEXT, status TEXT);
CREATE TABLE revisions (revision_id TEXT PRIMARY KEY, record_id TEXT, changed_at TEXT, field_name TEXT, old_value TEXT, new_value TEXT, reason TEXT);
