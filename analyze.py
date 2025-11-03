"""
analyze.py

Fetches records from the database and produces summaries:
- List of entries
- Total screen time overall
- Average daily screen time (based on days with records)
- Per-day total (and alert if any day exceeds threshold)
- Per-category totals

Edit DB credentials or THRESHOLD_HOURS as needed.
"""
from mysql.connector import connect, Error
import numpy as np
from collections import defaultdict

# --- Edit these credentials to match your MySQL server ---
HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "screentime_db"
TABLE_NAME = "usage_log"

# Alert threshold (hours per day)
THRESHOLD_HOURS = 6.0


def fetch_records():
    sql = f"SELECT entry_date, category, hours_spent, remarks FROM {TABLE_NAME} ORDER BY entry_date"
    try:
        with connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
        return rows
    except Error as e:
        print("Database error:", e)
        return None


def analyze(rows):
    if not rows:
        print("No records found.")
        return

    # Print all rows
    print("\nScreen Time Records:\n")
    for r in rows:
        print(f"Date: {r[0]} | Category: {r[1]} | Hours: {r[2]:.2f} | Remarks: {r[3]}")

    # Per-day totals
    per_day = defaultdict(float)
    per_category = defaultdict(float)
    for r in rows:
        date_key = r[0].isoformat() if hasattr(r[0], 'isoformat') else str(r[0])
        per_day[date_key] += float(r[2])
        per_category[r[1]] += float(r[2])

    day_totals = list(per_day.values())
    total_hours = sum(day_totals)

    print("\nSummary Report:")
    print(f"Total Screen Time: {total_hours:.2f} hours")
    if day_totals:
        print(f"Average Screen Time (per day with records): {np.mean(day_totals):.2f} hours/day")
        print(f"Max Screen Time (single day): {max(day_totals):.2f} hours")

    # Per-day breakdown
    print("\nPer-day totals:")
    for d in sorted(per_day.keys()):
        val = per_day[d]
        alert = " ⚠️" if val > THRESHOLD_HOURS else ""
        print(f"{d}: {val:.2f} hours{alert}")

    # Per-category breakdown
    print("\nPer-category totals:")
    for cat, val in per_category.items():
        print(f"{cat}: {val:.2f} hours")

    # Alerts
    if np.mean(day_totals) > THRESHOLD_HOURS:
        print("\n⚠️ Average daily screen time exceeds threshold! Consider reducing usage.")

    heavy_days = [d for d, v in per_day.items() if v > THRESHOLD_HOURS]
    if heavy_days:
        print("\nDays exceeding threshold:")
        for d in heavy_days:
            print(f"- {d}: {per_day[d]:.2f} hours")


if __name__ == "__main__":
    rows = fetch_records()
    analyze(rows)
