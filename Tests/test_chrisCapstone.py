import sys
import os
import pandas as pd
import pytest

# Make Python find project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Python.chrisCapstone import shorten, standardize_pay

# Test shorten()

def test_shorten_basic_replacements():
    assert shorten("CHICAGO FIRE DEPARTMENT") == "CHI FIRE Dept."
    assert shorten("DEPARTMENT OF WATER MANAGEMENT") == "Dept. WATER MANAGEMENT"
    assert shorten("OFFICE OF THE MAYOR") == "Office THE MAYOR"


def test_shorten_no_change():
    assert shorten("PARK DISTRICT") == "PARK DISTRICT"


# Test standardize_pay()

def test_standardize_salary_priority():
    row = pd.Series({"salary": 80000, "hourly_rate": 50, "weekly_hours": 40})
    assert standardize_pay(row) == 80000.0


def test_standardize_hourly():
    row = pd.Series({"salary": 0, "hourly_rate": 40, "weekly_hours": 40})
    assert standardize_pay(row) == 40 * 40 * 52


def test_standardize_default_hours():
    row = pd.Series({"salary": 0, "hourly_rate": 20, "weekly_hours": None})
    assert standardize_pay(row) == 20 * 40 * 52


def test_standardize_zero_fallback():
    row = pd.Series({"salary": 0, "hourly_rate": 0, "weekly_hours": 0})
    assert standardize_pay(row) == 0.0