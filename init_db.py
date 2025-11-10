"""
Simple script to initialize the database.
Run this before starting the Streamlit app for the first time.
"""
from database import initialize_database

print("Initializing Screen Time Management Database...")
print("-" * 50)

success, message = initialize_database()

if success:
    print("✅ SUCCESS:", message)
    print("\nYou can now run the Streamlit app with:")
    print("    streamlit run app.py")
else:
    print("❌ ERROR:", message)
    print("\nPlease check your database credentials in config.py")
