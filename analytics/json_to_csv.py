import json
import os
import pandas as pd
from datetime import datetime

JSON_DIR = "data/bills_json"
CSV_PATH = "data/expenses.csv"


def infer_category(company_name):
    if not company_name:
        return "Other"

    name = company_name.lower()

    food_keywords = [
        "restaurant", "restoran", "cafe", "coffee",
        "mcdonald", "bakery", "gardenia", "food"
    ]

    shopping_keywords = [
        "mart", "store", "shop", "speed mart",
        "hardware", "d.i.y", "mr. d.i.y"
    ]

    office_keywords = [
        "stationery", "book", "office"
    ]

    if any(k in name for k in food_keywords):
        return "Food"

    if any(k in name for k in shopping_keywords):
        return "Shopping"

    if any(k in name for k in office_keywords):
        return "Office Supplies"

    return "Other"



from datetime import datetime

def normalize_date(date_str):
    if not date_str:
        return None

    date_formats = [
        "%d.%m.%Y",   # 27.03.2018
        "%d/%m/%Y",   # 27/03/2018
        "%Y-%m-%d",   # 2018-03-27
        "%d-%m-%Y",   # 27-03-2018
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    return None


def extract_rows():
    rows = []

    for filename in os.listdir(JSON_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(JSON_DIR, filename)

        with open(filepath, "r") as f:
            data = json.load(f)

        date = normalize_date(data.get("date"))

        row = {
            "date": date if date else "Unknown",
            "year": date.year if date else "Unknown",
            "company_name": data.get("company_name"),
            "total": data.get("total"),
            "category": infer_category(data.get("company_name")),
        }

        rows.append(row)

    return rows

def write_csv():
    rows = extract_rows()
    df = pd.DataFrame(rows)

    if os.path.exists(CSV_PATH):
        try:
            old_df = pd.read_csv(CSV_PATH)
            df = pd.concat([old_df, df]).drop_duplicates()
        except pd.errors.EmptyDataError:
            # CSV exists but is empty
            pass

    df.to_csv(CSV_PATH, index=False)
    print(f"✅ CSV updated: {CSV_PATH}")


if __name__ == "__main__":
    write_csv()
