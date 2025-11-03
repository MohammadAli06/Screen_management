"""
sample_data.py

Populate the database with a few sample entries for demonstration.

Edit DB credentials at top if needed.
"""
from mysql.connector import connect, Error
from datetime import date

# --- Edit these credentials to match your MySQL server ---
HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "screentime_db"
TABLE_NAME = "usage_log"


SAMPLE_ENTRIES = [
    (date(2025, 11, 1), 'Study', 3.5, 'Online classes'),
    (date(2025, 11, 1), 'Social Media', 2.0, 'Instagram'),
    (date(2025, 11, 2), 'Gaming', 4.0, 'Weekend'),
    (date(2025, 11, 2), 'Study', 2.5, 'Homework'),
    (date(2025, 11, 3), 'Entertainment', 1.5, 'YouTube'),
    (date(2025, 11, 3), 'Social Media', 2.5, 'Chats'),
]


def insert_samples(entries):
    sql = f"INSERT INTO {TABLE_NAME} (entry_date, category, hours_spent, remarks) VALUES (%s, %s, %s, %s)"
    try:
        with connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME) as conn:
            with conn.cursor() as cursor:
                cursor.executemany(sql, entries)
            conn.commit()
        print(f"Inserted {len(entries)} sample records.")
    except Error as e:
        print("Database error:", e)


if __name__ == "__main__":
    insert_samples(SAMPLE_ENTRIES)
