import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import zachCalculations as zach
from sqlalchemy import create_engine #this creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os
from adjustText import adjust_text


# Load our environment variable(s) from our .env file
load_dotenv()
database_url = os.getenv('DATABASE_URL')
# Create our database connection
engine=create_engine(database_url)

# #If we just want everything in a table we can just use pandas to ask for the table
df=pd.read_sql_table('stg_employee_comp',engine)

labels=list(df.columns)
#  0   "full_name",
#  1   "department",
#  2   "job_title",
#  3   "full_or_part",
#  4   "salary_or_hourly",
#  5   "salary",
#  6   "hourly_rate",
#  7   "weekly_hours",
#  8   "est_annual_pay",
#  9   "department_avg"

#