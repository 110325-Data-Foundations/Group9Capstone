import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sj_transformations import calculate_standardized_salary, calculate_cv
from sqlalchemy import create_engine #this creates our database engine
from dotenv import load_dotenv #lets us read from our .env file
import os
from adjustText import adjust_text

# PIP INSTALL REQUIREMENTS: adjustText, 

# Load our environment variable(s) from our .env file
load_dotenv()
database_url = os.getenv('DATABASE_URL')
# Create our database connection
engine=create_engine(database_url)

# #If we just want everything in a table we can just use pandas to ask for the table
df=pd.read_sql_table('stg_employee_comp',engine)

# Apply the Salary Standardization
df['total_comp'] = df.apply(
    lambda x: calculate_standardized_salary(
        x['salary'],
        x['hourly_rate'],
        x['weekly_hours']
    ), axis=1
)

# Group by Department
# Need mean salary, std, and employee count
dept_stats = df.groupby('department')['total_comp'].agg(
    ['mean', 'std', 'count']
).reset_index()

# Filter out very small departments that would mess with spread calculations
dept_stats = dept_stats[dept_stats['count'] >= 5]

# Use CV function
dept_stats['inequality_score'] = dept_stats.apply(
    lambda row: calculate_cv(row['mean'], row['std']
        ), axis=1
)

# Testing the output
print("Most unequal departments:")
print(dept_stats.sort_values('inequality_score', ascending=False).head())

# s = size of dots scaled down by 10 for visibility
plt.scatter(
    dept_stats['mean'],
    dept_stats['inequality_score'],
    s=dept_stats['count'] / 2,
    alpha=0.5,
    c='teal'
)

# Fancy part: Auto-Labeling Outliers
# Dont label every dot, instead only label ones that are High CV and High Pay Avg

# !!! SETUP CATEGORIES FOR LABELING !!!

def assign_category(row):
    # Assigns a color based category (priority based)
    if row['inequality_score'] > 40:
        return 'High Inequality'
    elif row['mean'] > 120000:
        return 'High Pay'
    elif 85000< row['mean'] < 100000 and 25 < row['inequality_score'] < 35:
        return 'Anchor Department'
    else:
        return 'Normal'

# Create the new column to hold these categories
dept_stats['label_category'] = dept_stats.apply(assign_category, axis=1)

# Color Legend
color_map = {
    'High Inequality': 'tomato',
    'High Pay': 'springgreen',
    'Anchor Department': 'cornflowerblue',
    'Normal': 'gainsboro'
}

# Scatterplot time
plt.figure(figsize=(14, 10))

# Must loop through to plot category separately to create legend
for category, color in color_map.items():
    subset = dept_stats[dept_stats['label_category'] == category]
    plt.scatter(
        subset['mean'],
        subset['inequality_score'],
        s=subset['count'], # Bubble size
        alpha=0.6, 
        c=color, # Color from map
        linewidth=0.5,
        label=category # Legend label
    )

# Plot formatting
plt.title('Chicago Departments: Average Pay vs. Salary Spread', fontsize=16)
plt.xlabel('Average Annual Compensation ($)', fontsize=12)
plt.ylabel('Inequality Score (Coefficient of Variance %)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.4)

lgnd = plt.legend(title='Department Categories', fontsize=10, loc='upper right')
# Fixing legend circle sizes
for handle in lgnd.legend_handles:
    handle.set_sizes([50])

label_subset = dept_stats[dept_stats['label_category'] != 'Normal']

texts = []
for i, row in label_subset.iterrows():
    texts.append(
        plt.text(
            row['mean'],
            row['inequality_score'],
            row['department'],
            fontsize=9,
            fontweight='bold',
            color='black'
        )
    )

# This is the way to adjust labels to minimize overlap with adjustText
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black', lw=1.0))

plt.tight_layout()   
plt.show()