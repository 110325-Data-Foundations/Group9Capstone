# Chicago Employee Compensation Analysis
# Data Engineering Capstone – Analysis Subsystem

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
from adjustText import adjust_text


# Shorten Long Chicago Department Names

def shorten(name: str) -> str:
    name = name.replace("CHICAGO ", "CHI ")
    name = name.replace("DEPARTMENT OF ", "Dept. ")
    name = name.replace("DEPARTMENT", "Dept.")
    name = name.replace("OFFICE OF ", "Office ")
    name = name.replace("COMMISSION ", "Comm. ")
    return name


# Load Environment + Database

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_sql_table("stg_employee_comp", engine)


# Feature Engineering – Standardized Compensation
# Converts salary/hourly rate → annual compensation
def standardize_pay(row):
    """Convert salary or hourly pay into a unified annual compensation value."""
    if row["salary"] and row["salary"] > 0:
        return float(row["salary"])
    if row["hourly_rate"] and row["hourly_rate"] > 0:
        hrs = row["weekly_hours"] if row["weekly_hours"] else 40
        return float(row["hourly_rate"] * hrs * 52)
    return 0

df["annual_comp"] = df.apply(standardize_pay, axis=1)



# Department Summary Statistics
# Creates mean, median, std deviation, IQR, min/max, count
dept_stats = df.groupby("department")["annual_comp"].agg(
    mean="mean",
    median="median",
    std="std",
    min="min",
    max="max",
    count="count"
).reset_index()

# Add Interquartile Range (75th percentile - 25th percentile)
dept_stats["IQR"] = (
    df.groupby("department")["annual_comp"].quantile(0.75).values
    - df.groupby("department")["annual_comp"].quantile(0.25).values
)



# GRAPH 1 — Scatter Plot 
# Mean vs Median Compensation (bubble size = dept size)
top_pay     = dept_stats.nlargest(5, "mean")
low_pay     = dept_stats.nsmallest(5, "median")
largest     = dept_stats.nlargest(5, "count")
high_spread = dept_stats.nlargest(5, "std")

# Combine all highlight groups into one unique set
highlight = pd.concat([top_pay, low_pay, largest, high_spread]).drop_duplicates("department")

plt.figure(figsize=(14, 9))
ax = plt.gca()

# Primary visible scatter (color + bubble size)
visible_scatter = ax.scatter(
    dept_stats["mean"],
    dept_stats["median"],
    s=dept_stats["count"] / 30,
    c=dept_stats["std"],
    cmap="coolwarm",
    alpha=0.5,
    edgecolors="black",
    linewidth=0.6
)

# Highlighted departments (bold outline)
highlight_colors = plt.cm.coolwarm(
    (highlight["std"] - dept_stats["std"].min()) /
    (dept_stats["std"].max() - dept_stats["std"].min())
)

ax.scatter(
    highlight["mean"],
    highlight["median"],
    s=highlight["count"] / 25,
    color=highlight_colors,
    edgecolors="white",
    linewidth=1.4,
    zorder=10
)

# Trendline
sns.regplot(
    data=dept_stats,
    x="mean", y="median",
    scatter=False,
    color="black",
    line_kws={"linewidth": 2, "alpha": 0.7}
)

# Add colorbar
norm = plt.Normalize(dept_stats["std"].min(), dept_stats["std"].max())
sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.02)
cbar.set_label("Pay Variability (Std Dev)", fontsize=11)

# Dept size legend
for s in [5000, 10000, 15000, 20000]:
    plt.scatter([], [], s=s/30, color="gray", alpha=0.5, label=f"{s:,}")

legend = plt.legend(
    title="Department Size (Employees)",
    loc="upper left",
    frameon=True
)
ax.add_artist(legend)

# Label highlighted points
texts = []
for _, row in highlight.iterrows():
    texts.append(
        plt.text(
            row["mean"], row["median"], shorten(row["department"]),
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="black", lw=0.8)
        )
    )

adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray", lw=0.7))


# Interactive hover layer (invisible scatter)
# Allows mouse hover to show department details
hover_scatter = ax.scatter(
    dept_stats["mean"],
    dept_stats["median"],
    s=dept_stats["count"] / 30,
    alpha=0,       # invisible
    picker=True
)

# Attach metadata for tooltip usage
hover_scatter._dept_labels = dept_stats["department"].tolist()
hover_scatter._mean_vals = dept_stats["mean"].tolist()
hover_scatter._median_vals = dept_stats["median"].tolist()
hover_scatter._counts = dept_stats["count"].tolist()

cursor = mplcursors.cursor(hover_scatter, hover=True)

@cursor.connect("add")
def on_add(sel):
    i = sel.index
    dept = hover_scatter._dept_labels[i]
    meanv = hover_scatter._mean_vals[i]
    medv = hover_scatter._median_vals[i]
    cnt = hover_scatter._counts[i]

    sel.annotation.set(text=
        f"{shorten(dept)}\n"
        f"Mean:   ${meanv:,.0f}\n"
        f"Median: ${medv:,.0f}\n"
        f"Employees: {cnt:,}"
    )
    sel.annotation.get_bbox_patch().set(
        fc="white", ec="black", alpha=0.9
    )


plt.title("Chicago Departments – Mean vs Median Compensation", fontsize=16, fontweight="bold")
plt.xlabel("Mean Annual Compensation ($)")
plt.ylabel("Median Annual Compensation ($)")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout(pad=2)
plt.show()


# GRAPH 2 — Boxplot of Top 10 Largest Departments
# Shows salary spread for top 10 largest departments
top10 = dept_stats.nlargest(10, "count")["department"].tolist()
df_top10 = df[df["department"].isin(top10)]

plt.figure(figsize=(14, 9))
sns.boxplot(
    data=df_top10,
    x="annual_comp",
    y="department",
    hue="department",
    palette="Set3",
    linewidth=1.1,
    showfliers=True,
    legend=False
)

plt.title("Salary Distribution – Top 10 Largest Chicago Departments", fontsize=16, fontweight="bold")
plt.xlabel("Annual Compensation ($)")
plt.ylabel("Department")

plt.yticks(
    ticks=range(len(top10)),
    labels=[shorten(d) for d in top10],
    fontsize=10,
    rotation=25,
    ha="right"
)

plt.grid(True, linestyle="--", alpha=0.3)
plt.gcf().subplots_adjust(left=0.32)
plt.tight_layout(pad=2)
plt.show()


# Summary Tables
print("\n=== Top 5 Highest Paying Departments (by Mean) ===\n")
print(dept_stats.nlargest(5, "mean")[["department", "mean", "median"]])

print("\n=== Top 5 Departments With Highest Pay Variability (Std Dev) ===\n")
print(dept_stats.nlargest(5, "std")[["department", "std"]])

print("\n=== Top 5 Largest Departments (# Employees) ===\n")
print(dept_stats.nlargest(5, "count")[["department", "count"]])
