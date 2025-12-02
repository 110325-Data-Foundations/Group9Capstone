import sys
import os
import Python.zachCalculations as zach


# Make Python see the project root
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_calculate_salary():
    ###AAA assign, act, assert
    hourly_rate =10
    weekly_hours=40
    wages=hourly_rate*weekly_hours*52
    assert zach.calculate_salary(10,40)==wages

def test_calculate_hourly():
    salary=50000
    calc_hourly=round(float((salary/40)/52),2)
    assert zach.calculate_hourly(salary)==calc_hourly

def test_calculate_salary_avg():
    salaryList=[40000,50000,60000]
    totalSalary=0
    count=0
    for x in salaryList:
        totalSalary+=x
        count+=1
    avgSalary=totalSalary/count
    assert zach.calculate_salary_avg(salaryList)==avgSalary

