import pandas as pd
from sqlalchemy import create_engine #creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os


#Step 1: Load our environment variable(s) from our .env file
load_dotenv()

database_url = os.getenv('DATABASE_URL')
complete_df = pd.read_csv("Data/Current_Employee_Names__Salaries__and_Position_Titles.csv")

#print(database_url)

# Step 2: Create our database connection
engine = create_engine(database_url)

complete_df.to_sql(
        name='chicago_employee',  # The name of the table to create/write to
        con=engine,             # Your database connection engine
        if_exists='replace',    # Options: 'fail', 'replace', 'append'
        index=False             # Set to False to avoid writing the DataFrame index as a column
)

# Step 3: Read from a table (that already exists)


# An example of a simple query
df = pd.read_sql("SELECT * FROM chicago_employee LIMIT 1000", engine)
print(df)

# If we just want everything in a table, we can just use pandas
# to ask for the table
# genre_df = pd.read_sql_table('genre', engine)

# print(genre_df)
