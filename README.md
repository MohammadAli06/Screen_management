# 📱 Screen Time Management System

A beautiful and interactive web application built with **Streamlit** to track, analyze, and manage your daily screen time usage. Perfect for Class XI Informatics Practices (065) project!

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

## ✨ Features

### 📊 Interactive Dashboard

- Real-time statistics and key metrics
- Beautiful visualizations with charts and graphs
- Daily screen time trends with threshold alerts
- Category-wise usage breakdown (pie and bar charts)
- Track days exceeding healthy usage limits

### ➕ Easy Data Entry

- User-friendly form with validation
- Pre-defined categories (Study, Work, Social Media, Gaming, etc.)
- Date picker and time input
- Optional remarks for each entry

### 📋 Records Management

- View all entries in a clean table format
- Filter by date range
- Search and sort functionality
- Delete unwanted entries

### 🔍 Analysis & Insights

- Detailed usage statistics
- Highest and lowest usage days
- Category insights with percentages
- Weekly usage patterns
- Smart recommendations based on your habits
- Health threshold monitoring

### 🎨 Beautiful UI

- Modern, responsive design
- Colorful charts and visualizations using Plotly
- Smooth animations and interactions
- Mobile-friendly interface

## 🛠️ Technologies Used

- **Frontend:** Streamlit (Python web framework)
- **Database:** MySQL
- **Data Visualization:** Plotly Express
- **Data Processing:** Pandas, NumPy
- **Database Connector:** mysql-connector-python

## 📋 Prerequisites

Before running the application, make sure you have:

1. **Python 3.7 or higher** installed
2. **MySQL Server** installed and running
3. **Git** (optional, for cloning)

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/MohammadAli06/Screen_management.git
cd Screen_management
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- streamlit
- mysql-connector-python
- pandas
- plotly
- numpy

### Step 3: Configure Database Credentials

Edit the `config.py` file and update your MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",           # Your MySQL username
    "password": "your_password",  # Your MySQL password
    "database": "screentime_db"
}
```

### Step 4: Initialize Database

**Option A: Using the helper script**

```bash
python init_db.py
```

**Option B: Using the Web App**

1. Run the app (see Step 5)
2. Go to "Settings" page in the sidebar
3. Click "🔄 Initialize Database"

### Step 5: Run the Application

Start the Streamlit web server:

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

If it doesn't open automatically, manually navigate to that URL.

## 📖 Usage Guide

### First Time Setup

1. **Initialize Database**
   - Go to Settings → Click "Initialize Database"
   - Wait for success message

2. **Add Sample Data (Optional)**
   - Go to Settings → Click "Insert Sample Data"
   - This adds 10 sample entries for testing

3. **Start Adding Your Data**
   - Go to "Add Entry" page
   - Fill in the form and submit

### Daily Usage

1. **Add Today's Screen Time**
   - Navigate to "Add Entry"
   - Select date (defaults to today)
   - Choose category and enter hours
   - Add optional remarks
   - Click "Add Entry"

2. **View Dashboard**
   - Check your daily trends
   - Monitor category breakdown
   - See if you're exceeding thresholds

3. **Analyze Your Habits**
   - Go to "Analysis" page
   - Review insights and recommendations
   - Check weekly patterns
   - Get personalized tips

4. **Manage Records**
   - View all entries in "View Records"
   - Filter by date range
   - Delete incorrect entries

## 📁 Project Structure

```
Screen_management/
│
├── app.py                 # Main Streamlit application
├── database.py            # Database operations module
├── config.py              # Configuration (DB credentials, settings)
├── init_db.py             # Database initialization helper
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🗄️ Database Schema

**Database:** `screentime_db`

**Table:** `usage_log`

| Column       | Type          | Description                    |
|--------------|---------------|--------------------------------|
| entry_id     | INT (PK)      | Auto-increment primary key     |
| entry_date   | DATE          | Date of usage                  |
| category     | VARCHAR(50)   | Activity category              |
| hours_spent  | FLOAT         | Hours spent (decimal allowed)  |
| remarks      | TEXT          | Optional notes                 |
| created_at   | TIMESTAMP     | Record creation timestamp      |

## 🎯 Features Breakdown

### Dashboard Page

- **4 Key Metrics Cards:** Total hours, entries, average daily, days tracked
- **Line Chart:** Daily screen time trend with threshold line
- **Pie Chart:** Category distribution
- **Bar Chart:** Category breakdown by hours
- **Alerts:** Days exceeding threshold

### Add Entry Page

- Form with date picker, category dropdown, hours input
- Input validation
- Success animations
- Clear on submit

### View Records Page

- Paginated data table
- Date range filtering
- Show all records option
- Delete functionality with ID input

### Analysis Page

- Summary statistics (highest/lowest days, averages)
- Top categories with progress bars
- Weekly usage pattern chart
- Smart recommendations
- Health insights

### Settings Page

- Database initialization button
- Sample data insertion
- About section with app info

## 💡 Customization

### Change Alert Threshold

Edit `config.py`:

```python
THRESHOLD_HOURS = 6.0  # Change to your preferred limit
```

### Add More Categories

Edit the category list in `app.py` (around line 164):

```python
category = st.selectbox(
    "Category",
    options=["Study", "Work", "Your New Category", ...]
)
```

### Modify Color Scheme

Update the CSS in `app.py` (around line 23):

```python
st.markdown("""
    <style>
    /* Your custom CSS here */
    </style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### Database Connection Error

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:**

- Check your MySQL username and password in `config.py`
- Ensure MySQL server is running
- Verify user has necessary privileges

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**

```bash
pip install -r requirements.txt
```

### Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:**

```bash
streamlit run app.py --server.port 8502
```

### Database Does Not Exist

**Error:** `Unknown database 'screentime_db'`

**Solution:**

- Go to Settings page and click "Initialize Database"
- Or run `python init_db.py`

## 🎓 Educational Value

This project demonstrates:

- **Python Programming:** Functions, error handling, data structures
- **Database Operations:** SQL queries, CRUD operations, data aggregation
- **Web Development:** Interactive UI, forms, navigation
- **Data Visualization:** Charts, graphs, statistical displays
- **Data Analysis:** Calculating averages, trends, patterns
- **Software Design:** Modular code, separation of concerns

Perfect for Class XI Informatics Practices (065) syllabus covering:

- Python with MySQL connectivity
- Data handling with Pandas
- NumPy for calculations
- Web-based project implementation

## 📸 Screenshots

### Dashboard

Beautiful visualizations showing daily trends, category breakdown in pie and bar charts, and key metrics at a glance.

### Add Entry Form

Simple, intuitive data entry with validation and error handling, plus success confirmations.

### Analysis Page

Detailed insights and recommendations, weekly patterns, and health alerts.

## 🔮 Future Enhancements

Possible additions:

- 📊 Export data to CSV/Excel
- 📧 Email reports
- 👥 Multi-user support with login
- 📱 Mobile app version
- 🎯 Goal setting and tracking
- 📅 Calendar view
- 🔔 Desktop notifications for breaks
- 📈 Month-over-month comparisons

## 🤝 Contributing

This is an educational project. Feel free to:

- Add new features
- Improve visualizations
- Enhance UI/UX
- Fix bugs
- Add documentation

## 📄 License

This project is created for educational purposes as part of Class XI Informatics Practices curriculum.

## 👨‍💻 Author

**MohammadAli06**

Created for Class XI Informatics Practices (065) project.

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- Plotly for beautiful visualizations
- MySQL for reliable data storage
- The Python community for excellent libraries

---

## 📞 Quick Reference Commands

```bash
# Clone repository
git clone https://github.com/MohammadAli06/Screen_management.git

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502
```

---

**Happy Tracking! 📱📊**

Remember: The goal is not just to track screen time, but to develop healthier digital habits! 🌟

---

## ⭐ Star This Repository

If you find this project helpful, please consider giving it a star! ⭐
