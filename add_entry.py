"""
add_entry.py

Interactive script to add a screen time usage entry to the database.

Edit the DB credentials at top if needed.
"""
from mysql.connector import connect, Error
from datetime import datetime

# --- Edit these credentials to match your MySQL server ---
HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "screentime_db"
TABLE_NAME = "usage_log"


def prompt_entry():
    date_str = input("Enter date (YYYY-MM-DD) [default: today]: ").strip()
    if not date_str:
        entry_date = datetime.today().date()
    else:
        try:
            entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return None

    category = input("Enter category (Study/Social Media/Entertainment/Gaming/etc.): ").strip()
    if not category:
        print("Category cannot be empty.")
        return None

    hours_str = input("Enter hours spent (e.g. 2.5): ").strip()
    try:
        hours = float(hours_str)
        if hours < 0 or hours > 24:
            print("Hours should be between 0 and 24.")
            return None
    except ValueError:
        print("Invalid number for hours.")
        return None

    remarks = input("Any remarks (optional): ").strip()

    return (entry_date, category, hours, remarks)


def insert_entry(entry):
    sql = f"INSERT INTO {TABLE_NAME} (entry_date, category, hours_spent, remarks) VALUES (%s, %s, %s, %s)"
    try:
        with connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, entry)
            conn.commit()
        print("Record inserted successfully.")
    except Error as e:
        print("Database error:", e)


if __name__ == "__main__":
    print("Add a screen time entry")
    entry = prompt_entry()
    if entry:
        insert_entry(entry)
