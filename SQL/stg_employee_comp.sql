
-- DROP + CREATE stg_employee_comp
DROP TABLE IF EXISTS stg_employee_comp CASCADE;

CREATE TABLE stg_employee_comp (
    emp_id           SERIAL PRIMARY KEY,
    full_name        VARCHAR(100),
    department       VARCHAR(100),
    job_title        VARCHAR(100),
    full_or_part     VARCHAR(50),
    salary_or_hourly CHAR(6),
    salary           NUMERIC(12,2) DEFAULT 0,
    hourly_rate      NUMERIC(10,2) DEFAULT 0,
    weekly_hours     INTEGER DEFAULT 40,
    load_ts          TIMESTAMPTZ DEFAULT NOW(),
);

-- DROP + CREATE rejects
DROP TABLE IF EXISTS rejects CASCADE;

CREATE TABLE rejects (
    rejected_id SERIAL PRIMARY KEY,
    raw_record JSON,
    error_reason TEXT,
    load_ts TIMESTAMPTZ DEFAULT NOW(),
    source_file TEXT
);


-- DROP + CREATE audit_logs
DROP TABLE IF EXISTS audit_logs CASCADE;

CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    changed_by TEXT DEFAULT CURRENT_USER,
    new_data JSONB,
    old_data JSONB
);


-- TRIGGER FUNCTION FOR AUDIT LOGGING
CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (table_name, action_type, new_data)
        VALUES (TG_TABLE_NAME, 'INSERT', row_to_json(NEW));

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (table_name, action_type, old_data, new_data)
        VALUES (TG_TABLE_NAME, 'UPDATE', row_to_json(OLD), row_to_json(NEW));

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (table_name, action_type, old_data)
        VALUES (TG_TABLE_NAME, 'DELETE', row_to_json(OLD));
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ADD TRIGGERS TO TABLES

-- stg_employee_comp trigger
DROP TRIGGER IF EXISTS trg_stg_employee_comp_audit ON stg_employee_comp;

CREATE TRIGGER trg_stg_employee_comp_audit
AFTER INSERT OR UPDATE OR DELETE ON stg_employee_comp
FOR EACH ROW EXECUTE FUNCTION log_changes();

-- rejects trigger
DROP TRIGGER IF EXISTS trg_rejects_audit ON rejects;

CREATE TRIGGER trg_rejects_audit
AFTER INSERT OR UPDATE OR DELETE ON rejects
FOR EACH ROW EXECUTE FUNCTION log_changes();

-- VERIFICATION QUERIES
SELECT COUNT(*) AS total_stg_rows FROM stg_employee_comp;
SELECT COUNT(*) AS total_rejected_rows FROM rejects;
SELECT * FROM stg_employee_comp LIMIT 1000;

-- View audit log
SELECT * FROM audit_logs ORDER BY log_id DESC LIMIT 25;


TRUNCATE TABLE stg_employee_comp RESTART IDENTITY CASCADE;
TRUNCATE TABLE rejects RESTART IDENTITY CASCADE;