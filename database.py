"""
Database operations module for Screen Time Management System.
Handles all MySQL database interactions.
"""
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
import pandas as pd
from config import DB_CONFIG


def get_connection():
    """Create and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise Exception(f"Database connection error: {e}")


def initialize_database():
    """Create database and tables if they don't exist."""
    try:
        # Connect without database first
        temp_config = DB_CONFIG.copy()
        db_name = temp_config.pop("database")
        
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Create usage_log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_log (
                entry_id INT AUTO_INCREMENT PRIMARY KEY,
                entry_date DATE NOT NULL,
                category VARCHAR(50) NOT NULL,
                hours_spent FLOAT NOT NULL,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_date (entry_date),
                INDEX idx_category (category)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Database initialized successfully!"
    except Error as e:
        return False, f"Database initialization error: {e}"


def add_entry(entry_date, category, hours_spent, remarks=""):
    """Add a new screen time entry to the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO usage_log (entry_date, category, hours_spent, remarks)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (entry_date, category, hours_spent, remarks))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Entry added successfully!"
    except Error as e:
        return False, f"Error adding entry: {e}"


def get_all_entries():
    """Fetch all entries from the database."""
    try:
        conn = get_connection()
        query = """
            SELECT entry_id, entry_date, category, hours_spent, remarks
            FROM usage_log
            ORDER BY entry_date DESC, entry_id DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Error as e:
        raise Exception(f"Error fetching entries: {e}")


def get_date_range_entries(start_date, end_date):
    """Fetch entries within a date range."""
    try:
        conn = get_connection()
        query = """
            SELECT entry_id, entry_date, category, hours_spent, remarks
            FROM usage_log
            WHERE entry_date BETWEEN %s AND %s
            ORDER BY entry_date DESC
        """
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        return df
    except Error as e:
        raise Exception(f"Error fetching entries: {e}")


def get_daily_totals():
    """Get total hours per day."""
    try:
        conn = get_connection()
        query = """
            SELECT entry_date, SUM(hours_spent) as total_hours
            FROM usage_log
            GROUP BY entry_date
            ORDER BY entry_date
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Error as e:
        raise Exception(f"Error fetching daily totals: {e}")


def get_category_totals():
    """Get total hours per category."""
    try:
        conn = get_connection()
        query = """
            SELECT category, SUM(hours_spent) as total_hours
            FROM usage_log
            GROUP BY category
            ORDER BY total_hours DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Error as e:
        raise Exception(f"Error fetching category totals: {e}")


def get_statistics():
    """Get overall statistics."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Total hours
        cursor.execute("SELECT SUM(hours_spent) as total FROM usage_log")
        total = cursor.fetchone()['total'] or 0
        
        # Total entries
        cursor.execute("SELECT COUNT(*) as count FROM usage_log")
        count = cursor.fetchone()['count'] or 0
        
        # Average daily usage
        cursor.execute("""
            SELECT AVG(daily_total) as avg_daily
            FROM (
                SELECT SUM(hours_spent) as daily_total
                FROM usage_log
                GROUP BY entry_date
            ) as daily_totals
        """)
        avg_daily = cursor.fetchone()['avg_daily'] or 0
        
        # Date range
        cursor.execute("""
            SELECT MIN(entry_date) as first_date, MAX(entry_date) as last_date
            FROM usage_log
        """)
        date_range = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'total_hours': float(total),
            'total_entries': int(count),
            'avg_daily_hours': float(avg_daily),
            'first_date': date_range['first_date'],
            'last_date': date_range['last_date']
        }
    except Error as e:
        raise Exception(f"Error fetching statistics: {e}")


def delete_entry(entry_id):
    """Delete an entry by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM usage_log WHERE entry_id = %s", (entry_id,))
        
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected > 0:
            return True, "Entry deleted successfully!"
        else:
            return False, "Entry not found."
    except Error as e:
        return False, f"Error deleting entry: {e}"


def insert_sample_data():
    """Insert sample data for demonstration."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        sample_entries = [
            (date(2025, 11, 1), 'Study', 3.5, 'Online classes'),
            (date(2025, 11, 1), 'Social Media', 2.0, 'Instagram and Twitter'),
            (date(2025, 11, 2), 'Gaming', 4.0, 'Weekend gaming session'),
            (date(2025, 11, 2), 'Study', 2.5, 'Homework and assignments'),
            (date(2025, 11, 3), 'Entertainment', 1.5, 'YouTube videos'),
            (date(2025, 11, 3), 'Social Media', 2.5, 'WhatsApp and Instagram'),
            (date(2025, 11, 4), 'Study', 4.0, 'Exam preparation'),
            (date(2025, 11, 4), 'Gaming', 1.5, 'Mobile games'),
            (date(2025, 11, 5), 'Work', 5.0, 'Project work'),
            (date(2025, 11, 5), 'Entertainment', 2.0, 'Netflix'),
        ]
        
        query = """
            INSERT INTO usage_log (entry_date, category, hours_spent, remarks)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(query, sample_entries)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Inserted {len(sample_entries)} sample entries!"
    except Error as e:
        return False, f"Error inserting sample data: {e}"
