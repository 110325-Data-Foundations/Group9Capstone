DROP TABLE stg_rejects;

CREATE TABLE employee_comp (
    emp_id           SERIAL PRIMARY KEY,
    full_name        VARCHAR,
    department       TEXT,
    job_title        TEXT,
    full_or_part     TEXT,          -- 'F'/'P' or 'FULL TIME'/'PART TIME'
    salary           NUMERIC(12,2), -- annual salary (nullable)
    hourly_rate      NUMERIC(10,2), -- hourly rate (nullable)
    weekly_pay        INTEGER,       -- 10, 20, 35, 40 (nullable)
    load_ts          TIMESTAMPTZ DEFAULT NOW(),
    source_file      TEXT
);

CREATE TABLE rejects (
    rejected_id SERIAL PRIMARY KEY,
    raw_record JSONB,
    error_reason TEXT,
    load_ts TIMESTAMPTZ DEFAULT NOW(),
    source_file TEXT
);