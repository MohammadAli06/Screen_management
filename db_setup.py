"""
db_setup.py

Creates the MySQL database and usage_log table for the Screen Time Management project.

Edit HOST, USER, PASSWORD if necessary.
"""
from mysql.connector import connect, Error

# --- Edit these credentials to match your MySQL server ---
HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "screentime_db"
TABLE_NAME = "usage_log"


def create_database_and_table():
    try:
        with connect(host=HOST, user=USER, password=PASSWORD) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
                cursor.execute(f"USE {DB_NAME}")

                create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    entry_id INT AUTO_INCREMENT PRIMARY KEY,
                    entry_date DATE NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    hours_spent FLOAT NOT NULL,
                    remarks VARCHAR(255)
                )
                """
                cursor.execute(create_table_sql)
        print(f"Database '{DB_NAME}' and table '{TABLE_NAME}' are ready.")
    except Error as e:
        print("Error while creating database/table:", e)


if __name__ == "__main__":
    create_database_and_table()
