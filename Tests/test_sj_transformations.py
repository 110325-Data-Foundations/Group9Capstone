import sys
import os

# Make Python see the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Python.sj_transformations import calculate_standardized_salary

def test_salary_takes_precedence():
    # If both somehow exist, salary should be chosen
    assert calculate_standardized_salary(100000, 50, 40) == 100000

def test_hourly_calculation():
    # $50/hr * 40hrs * 52wks = $104,000
    assert calculate_standardized_salary(None, 50, 40) == 104000

def test_hourly_default_hours():
    # If no hours provided, default to 40
    # $10/hr * 40hrs * 52wks = $20,800
    assert calculate_standardized_salary(0, 10, None) == 20800