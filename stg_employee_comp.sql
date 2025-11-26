    
    
CREATE TABLE stg_employee_comp (
    emp_id           SERIAL PRIMARY KEY,
    full_name        TEXT,
    department       TEXT,
    job_title        TEXT,
    full_or_part     TEXT,          -- 'F'/'P' or 'FULL TIME'/'PART TIME'
    salary           NUMERIC(12,2), -- annual salary (nullable)
    hourly_rate      NUMERIC(10,2), -- hourly rate (nullable)
    frequency        INTEGER,       -- 10, 20, 35, 40 (nullable)
    est_annual_pay   NUMERIC(12,2), -- feature-engineered (optional)
    is_manager       BOOLEAN,       -- feature-engineered (optional)
    load_ts          TIMESTAMPTZ DEFAULT NOW(),
    source_file      TEXT
);

CREATE TABLE stg_rejects (
    rejected_id SERIAL PRIMARY KEY,
    raw_record JSONB,
    error_reason TEXT,
    load_ts TIMESTAMPTZ DEFAULT NOW(),
    source_file TEXT
);