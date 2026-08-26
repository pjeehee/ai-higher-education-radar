CREATE TABLE intelligence_changes (
 change_id TEXT PRIMARY KEY,
 trigger_record_id TEXT,
 artifact_type TEXT,
 artifact_key TEXT,
 before_value TEXT,
 after_value TEXT,
 scoring_version TEXT,
 changed_at TEXT,
 review_status TEXT
);
