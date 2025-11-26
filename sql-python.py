import pandas as pd
from sqlalchemy import create_engine #creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os 

# Step 1: Load our environment variable(s) from our .env file
load_dotenv() #lowecase L 

database_url = os.getenv('DATABASE_URL')

# print(database_url)- just a sanity check 

# Step 2: Create our database connection
engine = create_engine(database_url)

# Step 3: Read from a table (that already exists)

# An example of a simple query
df = pd.read_sql("SELECT * FROM stg_employee_comp LIMIT 5", engine)
print(df)

# If we just want everything in a table, we can just use pandas
# to ask for the table
genre_df = pd.read_sql_table('stg_employee_comp', engine)

print(genre_df)

print("DB URL:", database_url)