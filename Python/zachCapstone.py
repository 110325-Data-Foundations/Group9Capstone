import pandas as pd
from sqlalchemy import create_engine #this creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os

#Step 1: Load our environment variable(s) from our .env file
load_dotenv()

database_url = os.getenv('DATABASE_URL')

#print(database_url) Printing to make sure the url gets grabbed

#Step 2: Create our database connection
engine=create_engine(database_url)

# #Step 3: Read from table (that already exists)
# #an example of a simple query
# first_df=pd.read_sql("SELECT * FROM album LIMIT 5;",engine)
# print(first_df)

# #If we just want everything in a table we can just use pandas
# #to ask for the table
# genre_df=pd.read_sql_table('genre',engine)
# print(genre_df)