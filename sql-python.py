import pandas as pd
from sqlalchemy import create_engine #creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os 
import json 

# Step 1: Load our environment variable(s) from our .env file
load_dotenv() #lowecase L 

database_url = os.getenv('DATABASE_URL')

# print(database_url)- just a sanity check 

# Step 2: Create our database connection
engine = create_engine(database_url)

# Load CSV
csv_path = "Data/Current_Employee_Names__Salaries__and_Position_Titles.csv"
df = pd.read_csv(csv_path)

# --- Rename columns to match table ---
df = df.rename(columns={
    "Name": "full_name",
    "Department": "department",
    "Job Titles": "job_title",
    "Full or Part-Time": "full_or_part",
    "Typical Hours": "frequency",
    "Annual Salary": "salary",
    "Hourly Rate": "hourly_rate",
    "Salary or Hourly": "salary_or_hourly"
})

# Basic validation
valid_rows = []
reject_rows = []

# Write to db
df.to_sql("stg_employee_comp", engine, if_exists="append", index=False)

print("Inserted rows:", len(df))