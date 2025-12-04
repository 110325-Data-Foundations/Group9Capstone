import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_correlation(df):

    df_corr = df.copy()

    # Full-time vs part-time
    df_corr["full_time_num"] = df_corr["full_or_part"].apply(
        lambda x: 1 if x == "F" else 0
    )

    # Salary job vs hourly job
    df_corr["salary_job_num"] = df_corr["salary_or_hourly"].apply(
        lambda x: 1 if str(x).upper() == "SALARY" else 0
    )

    # Department size (how many employees each department has)
    dept_size = df_corr["department"].value_counts()
    df_corr["department_size"] = df_corr["department"].map(dept_size)

    # Department average pay (this is very meaningful)
    dept_avg = df_corr.groupby("department")["annual_comp"].mean()
    df_corr["department_avg_pay"] = df_corr["department"].map(dept_avg)

    # Only include numeric columns that matter
    cols = [
        "annual_comp",
        "salary",
        "hourly_rate",
        "weekly_hours",
        "full_time_num",
        "salary_job_num",
        "department_size",
        "department_avg_pay"
    ]

    corr = df_corr[cols].corr()

    plt.figure(figsize=(11, 8))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )

    plt.title(
        "Correlation Heatmap: Pay Drivers & Job Types",
        fontsize=16
    )
    plt.tight_layout(pad=2.0)
    plt.show()
