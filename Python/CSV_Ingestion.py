import pandas as pd
from sqlalchemy import create_engine #creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os
import json
import zachCalculations as zach

#Step 1: Load our environment variable(s) from our .env file
load_dotenv()

# Step 2: Create our database connection
engine = create_engine(os.getenv('DATABASE_URL'))

#Load CSV
df = pd.read_csv("Data/Current_Employee_Names__Salaries__and_Position_Titles.csv")

#Load JSON
#jsondf = pd.read_json("Data/CapstoneJsonFile.json")

# Rename CSV -> DB columns
df = df.rename(columns={
    "Name": "full_name",
    "Job Titles": "job_title",
    "Department": "department",
    "Full or Part-Time": "full_or_part",
    "Salary or Hourly": "salary_or_hourly",
    "Typical Hours": "weekly_hours",
    "Annual Salary": "salary",
    "Hourly Rate": "hourly_rate"
})
labels=list(df.columns)

# Add required NULL columns 
df["est_annual_pay"] = None 
df["department_avg"] = None 


# Avoid NaN numeric issues
# df["salary"] = df["salary"].fillna(0)
# df["hourly_rate"] = df["hourly_rate"].fillna(0)
# df["weekly_hours"] = df["weekly_hours"].fillna(40)

#Creating functions to fill the df with actual numbers instead of 0

for idx, row in df.iterrows():
    salary = row["salary"]
    hourly_rate = row["hourly_rate"]
    weekly_hours = row["weekly_hours"]

    if pd.isna(salary) and not pd.isna(hourly_rate) and not pd.isna(weekly_hours):
        df.at[idx, "salary"] = zach.calculate_salary(hourly_rate, weekly_hours)

    if pd.isna(hourly_rate) and not pd.isna(salary):
        df.at[idx, "hourly_rate"] = zach.calculate_hourly(salary)

    if pd.isna(weekly_hours):
        df.at[idx, "weekly_hours"] = 40

# Required fields for ingestion
required_cols = ["full_name", "department", "job_title"]

valid_rows = []
reject_rows = []
seen=set() # This is for checking for duplicate rows
for idx, row in df.iterrows():
    try:
        # Validate required fields
        for col in required_cols:
            if pd.isna(row[col]):
                raise ValueError(f"Missing {col}")

        # Check for duplicates
        row_tuple=tuple(row.items())
        if row_tuple in seen:
            raise ValueError("Duplicate row.")
        seen.add(row_tuple)

        valid_rows.append(row)
 
    except Exception as e:

        # Replace NaN/None with None so JSON is valid
        clean_row = {
            # If v is null or none, replaces it with None so it can be
            # serialized into JSON
            #After check, replaces values with None so JSON is valid
            k: (None if pd.isna(v) or v is None else v)
            for k, v in row.items()
            #Every None will be a null in the database
        }
        reject_rows.append({
            "raw_record": json.dumps(clean_row),  # now safe JSON
            "error_reason": str(e),
            "source_file": "employee_csv"
        })

        # reject_rows.append({
        #     # default=str should handle empty values
        #     "raw_record": json.dumps(row.to_dict(), default=str),
        #     "error_reason": str(e),
        #     "source_file": "employee_csv"
        # })

valid_df = pd.DataFrame(valid_rows)
reject_df = pd.DataFrame(reject_rows)

# Match DB column order
valid_df = valid_df[[
    "full_name",
    "department",
    "job_title",
    "full_or_part",
    "salary_or_hourly",
    "salary",
    "hourly_rate",
    "weekly_hours",
    "est_annual_pay",
    "department_avg"
]]

# Load valid rows into stg_employee_comp table
if not valid_df.empty:
    valid_df.to_sql("stg_employee_comp", engine, if_exists="append", index=False)
    print(f"Inserted {len(valid_df)} valid rows.")

# Load rejected rows into rejects table 
if not reject_df.empty:
    reject_df.to_sql("rejects", engine, if_exists="append", index=False)
    print(f"Inserted {len(reject_df)} rejected rows.")

