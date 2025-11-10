"""
Configuration file for database credentials.
Edit these values to match your MySQL server setup.
"""

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "screentime_db"
}

# Application Settings
APP_TITLE = "Screen Time Management System"
THRESHOLD_HOURS = 6.0  # Alert threshold for daily screen time
