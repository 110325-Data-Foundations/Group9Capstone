import pandas as pd
import os

#Creating functions to fill the df with actual numbers instead of 0

# # Avoid NaN numeric issues
# df["salary"] = df["salary"].fillna(0)
# df["hourly_rate"] = df["hourly_rate"].fillna(0)
# df["weekly_hours"] = df["weekly_hours"].fillna(40)

#Calculates salary if there is none
def calculate_salary(hourly_rate,weekly_hours):
    if hourly_rate is not None and weekly_hours is not None:
        return round(float(hourly_rate*weekly_hours*52),2)
    
#Calculates hourly if there is none
def calculate_hourly(salary):
    if salary is not None:
        return round(float((salary/40)/52),2)
    
#Calculates department average - should be used in a spot where it matches with a department name
def calculate_salary_avg(salary):
    totalSalary=0
    for y in salary:
        totalSalary+=y
    return totalSalary
