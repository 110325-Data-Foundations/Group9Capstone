    
    
CREATE TABLE stg_employee_comp (
    emp_id           SERIAL PRIMARY KEY,
    full_name        VARCHAR(50),
    department       VARCHAR(50),
    job_title        VARCHAR(50),
    full_or_part     VARCHAR(25),       -- 'F'/'P' or 'FULL TIME'/'PART TIME'
    salary_or_hourly CHAR(6),
    salary           NUMERIC(12,2) GENERATED ALWAYS AS (hourly_rate * weekly_hours) STORED -- annual salary (nullable)
    hourly_rate      NUMERIC(10,2) GENERATED ALWAYS AS (salary / 40) STORED, -- hourly rate (nullable)
    --generated columns cannot be written to directly. it 
    weekly_hours     INTEGER DEFAULT 40,       -- 10, 20, 35, 40 (nullable)
    est_annual_pay   NUMERIC(12,2), -- feature-engineered (optional)
    load_ts          TIMESTAMPTZ DEFAULT NOW(),
    department_avg   NUMERIC(12,2)  -- feature-engineered (optional)
);

CREATE TABLE stg_rejects (
    rejected_id SERIAL PRIMARY KEY,
    raw_record JSON,
    error_reason TEXT,
    load_ts TIMESTAMPTZ DEFAULT NOW(),
    source_file TEXT
);