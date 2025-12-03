import pandas as pd
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

# We want to compare the average hourly pay of part time and full time by department
# Created a DF with average hourly by salary, full time, and part time grouped by department

filtered = df[
    ((df['full_or_part'] == 'F') & (df['salary_or_hourly'] == 'HOURLY')) |
    (df['salary_or_hourly'] == 'SALARY') | ((df['full_or_part'] == 'P') & 
    (df['salary_or_hourly'] == 'HOURLY'))
]

avgHourly = filtered.groupby(['department','salary_or_hourly','full_or_part'])['hourly_rate'].mean()
# print(avgHourly)
avgHourly_df = avgHourly.reset_index()

filtered2 = df[
    ((df['full_or_part'] == 'F') & (df['salary_or_hourly'] == 'HOURLY')) |
    ((df['full_or_part'] == 'P') & (df['salary_or_hourly'] == 'HOURLY')) |
    (df['salary_or_hourly'] == 'SALARY')
]

departments_with_part_time = df.loc[df['full_or_part'] == 'P', 'department'].unique()

# Filter avgHourly_df to only those departments
avgHourly_df = avgHourly_df[avgHourly_df['department'].isin(departments_with_part_time)]


# This calculates the average overall of the part time, full time, and salaried hourly rates
avgOverall = filtered.groupby(['salary_or_hourly','full_or_part'])['hourly_rate'].mean().reset_index()


#The below code goes through the df and cleans up the appearance of the columns and column names
def label_row(row):
    if row['salary_or_hourly'] == 'HOURLY' and row['full_or_part'] == 'F':
        return 'Full-Time Hourly'
    elif row['salary_or_hourly'] == 'HOURLY' and row['full_or_part'] == 'P':
        return 'Part-Time Hourly'
    elif row['salary_or_hourly'] == 'SALARY':
        return 'Salaried'
    else:
        return 'Other'

avgOverall['category'] = avgOverall.apply(label_row, axis=1)

# Step 4: Display results
print(avgOverall[['category','hourly_rate']])





# Pivot so each category becomes a column
pivot_df = avgHourly_df.pivot_table(
    index='department',
    columns=['salary_or_hourly','full_or_part'],
    values='hourly_rate'
)

# Plot grouped bar chart to show average hourly wage by department
pivot_df.plot(kind='bar', figsize=(10,6))

plt.xlabel('Departments With Part Time Employees')
plt.ylabel('Average Hourly Rate')
plt.title('Average Hourly Rate by Department (Only Departments with Part-Time Employees)')
plt.xticks(rotation=45,fontsize=8)
for label in plt.gca().get_xticklabels():
    label.set_horizontalalignment('right')   # ha='right'

# plt.tick_params(axis='x',which='major',pad=15)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

