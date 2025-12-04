# Chicago Employee Compensation Analysis
# Data Engineering Capstone – Analysis Subsystem

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns
from Python.chrisCorrel import plot_correlation


# Shorten long department names

def shorten(name: str) -> str:
    name = name.replace("CHICAGO ", "CHI ")
    name = name.replace("DEPARTMENT OF ", "Dept. ")
    name = name.replace("DEPARTMENT", "Dept.")
    name = name.replace("OFFICE OF ", "Office ")
    name = name.replace("COMMISSION ", "Comm. ")
    return name


# Convert salary or hourly rate into annual pay

def standardize_pay(row):
    if pd.notna(row["salary"]) and row["salary"] > 0:
        return float(row["salary"])

    if pd.notna(row["hourly_rate"]) and row["hourly_rate"] > 0:
        hours = row["weekly_hours"]
        if pd.isna(hours) or hours <= 0:
            hours = 40  # default
        return float(row["hourly_rate"] * hours * 52)

    return 0.0


# Load Data

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
df = pd.read_sql_table("stg_employee_comp", engine)

df["annual_comp"] = df.apply(standardize_pay, axis=1)


# Department Summary Stats

dept_stats = (
    df.groupby("department")["annual_comp"]
      .agg(["mean", "median", "std", "min", "max", "count"])
      .reset_index()
)

dept_stats["IQR"] = (
    df.groupby("department")["annual_comp"].quantile(0.75).values -
    df.groupby("department")["annual_comp"].quantile(0.25).values
)


# Graph 1: Simple Scatter Plot

def plot_scatter(dept_stats):

    plt.figure(figsize=(13, 8))

    # Scatter: mean vs median
    plt.scatter(
        dept_stats["mean"],
        dept_stats["median"],
        s=dept_stats["count"] / 30,  # bubble size
        c=dept_stats["std"],         # color = variability
        cmap="coolwarm",
        alpha=0.6,
        edgecolors="black"
    )

    # Trendline
    sns.regplot(
        data=dept_stats,
        x="mean",
        y="median",
        scatter=False,
        color="black"
    )

    # Highlight top 5 largest departments
    largest = dept_stats.nlargest(5, "count")
    for _, row in largest.iterrows():
        plt.text(
            row["mean"], row["median"],
            shorten(row["department"]),
            fontsize=9,
            ha="center",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="black")
        )

    plt.colorbar(label="Variability (Std Dev)")

    plt.title("Mean vs Median Pay by Department", fontsize=15)
    plt.xlabel("Mean Annual Compensation ($)")
    plt.ylabel("Median Annual Compensation ($)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# Graph 2: Salary Boxplot for Top 10 Departments

def plot_boxplot(df, dept_stats):
    # Top 10 departments by employee count
    top10 = (
        dept_stats.nlargest(10, "count")
                  .sort_values("median")["department"]  # <-- FIX: sort by median
    )

    # Filter DF
    df_top = df[df["department"].isin(top10)]

    # Define order explicitly (IMPORTANT)
    order = list(top10)

    plt.figure(figsize=(14, 9))

    sns.boxplot(
        data=df_top,
        x="annual_comp",
        y="department",
        order=order,
        palette="Set2",
        showfliers=True,
        flierprops=dict(
            marker='o',
            markersize=6,
            markerfacecolor='black',
            markeredgecolor='black'
        )
    )

    # Pretty labels
    plt.yticks(
        ticks=range(len(order)),
        labels=[shorten(d) for d in order]
    )

    plt.title("Salary Spread - Top 10 Largest Departments", fontsize=16)
    plt.xlabel("Annual Compensation ($)", fontsize=14)
    plt.ylabel("Department", fontsize=14)
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

# Print
def print_summaries():
    print("\n=== Top 5 Highest Paying Departments (mean) ===\n")
    print(dept_stats.nlargest(5, "mean")[["department", "mean", "median"]])

    print("\n=== Highest Pay Variability (std) ===\n")
    print(dept_stats.nlargest(5, "std")[["department", "std"]])

    print("\n=== Largest Departments (count) ===\n")
    print(dept_stats.nlargest(5, "count")[["department", "count"]])


plot_scatter(dept_stats)
plot_boxplot(df, dept_stats)
print_summaries()
plot_correlation(df)
