
CREATE TABLE employee_comp (
    emp_id           SERIAL PRIMARY KEY,
    full_name        VARCHAR(100),
    department       VARCHAR(100),
    job_title        VARCHAR(100),
    full_or_part     VARCHAR(50),       -- 'F'/'P' or 'FULL TIME'/'PART TIME'
    salary_or_hourly CHAR(6),
    salary           NUMERIC(12,2) DEFAULT 0, -- annual salary (nullable)
    hourly_rate      NUMERIC(10,2) DEFAULT 0, -- hourly rate (nullable)
    --generated columns cannot be written to directly. it 
    weekly_hours     INTEGER DEFAULT 40,       -- 10, 20, 35, 40 (nullable)
    est_annual_pay   NUMERIC(12,2), -- feature-engineered (optional)
    load_ts          TIMESTAMPTZ DEFAULT NOW(),
    department_avg   NUMERIC(12,2)  -- feature-engineered (optional)
);

CREATE TABLE rejects (
    rejected_id SERIAL PRIMARY KEY,
    raw_record JSON,
    error_reason TEXT,
    load_ts TIMESTAMPTZ DEFAULT NOW(),
    source_file TEXT
);