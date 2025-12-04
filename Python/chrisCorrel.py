import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_correlation(df):

    df_corr = df.copy()

    # Convert to numeric if needed
    numeric_cols = ["salary", "hourly_rate", "weekly_hours"]
    for col in numeric_cols:
        df_corr[col] = pd.to_numeric(df_corr[col], errors="coerce")

    # Department size
    dept_size = df_corr["department"].value_counts()
    df_corr["department_size"] = df_corr["department"].map(dept_size)

    # Department average pay
    dept_avg = df_corr.groupby("department")["annual_comp"].mean()
    df_corr["department_avg_pay"] = df_corr["department"].map(dept_avg)

    # Choose only your requested columns
    cols = [
        "salary",
        "hourly_rate",
        "weekly_hours",
        "department_size",
        "department_avg_pay"
    ]

    corr = df_corr[cols].corr()

    # Plot
    plt.figure(figsize=(10, 7))
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )
    plt.title("Correlation Heatmap: Selected Job & Department Variables", fontsize=18)
    plt.tight_layout()
    plt.show()
