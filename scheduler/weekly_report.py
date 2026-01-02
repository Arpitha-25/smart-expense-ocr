import pandas as pd
from datetime import datetime, timedelta
import os

CSV_PATH = "data/expenses.csv"
OUTPUT_DIR = "reports"


def generate_weekly_report():
    if not os.path.exists(CSV_PATH):
        print("❌ No expenses.csv found")
        return

    df = pd.read_csv(CSV_PATH)

    # Handle dates safely
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Define last week range (Mon–Sun)
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday() + 7)
    end_of_week = start_of_week + timedelta(days=6)

    weekly_df = df[
        (df["date"] >= start_of_week) &
        (df["date"] <= end_of_week)
    ]

    if weekly_df.empty:
        print("ℹ️ No expenses for last week")
        return

    total_spend = weekly_df["total"].sum()
    category_summary = weekly_df.groupby("category")["total"].sum()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    report_name = f"weekly_report_{start_of_week.date()}_{end_of_week.date()}.txt"
    report_path = os.path.join(OUTPUT_DIR, report_name)

    with open(report_path, "w") as f:
        f.write(f"Weekly Expense Report\n")
        f.write(f"Week: {start_of_week.date()} → {end_of_week.date()}\n\n")
        f.write(f"Total Spend: {total_spend:.2f}\n\n")
        f.write("Category Breakdown:\n")

        for category, amount in category_summary.items():
            f.write(f"- {category}: {amount:.2f}\n")

    print(f"✅ Weekly report generated: {report_path}")


if __name__ == "__main__":
    generate_weekly_report()