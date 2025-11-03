Screen Time Management System
=============================

Simple Python project for Class XI Informatics Practices (065).

This project helps students track daily screen time, store records in a MySQL database, and generate simple summaries and alerts.

Features
- Create MySQL database and table
- Add daily usage records (date, category, hours, remarks)
- Analyze stored records: total, average, per-day totals, per-category totals, and alerts when usage exceeds a threshold

Requirements
- Python 3.7+
- MySQL Server running locally (or accessible host)
- Install Python packages from `requirements.txt`

Quick setup
1. Edit credentials in each script (or in your environment): open `db_setup.py` and set HOST, USER, PASSWORD as needed.
2. Install dependencies (PowerShell):

```powershell
python -m pip install -r requirements.txt
```

3. Create database and table:

```powershell
python db_setup.py
```

4. (Optional) Populate sample data:

```powershell
python sample_data.py
```

5. Add a usage entry interactively:

```powershell
python add_entry.py
```

6. View analysis report:

```powershell
python analyze.py
```

Notes and assumptions
- Scripts use `mysql-connector-python` to talk to MySQL. Change DB credentials at the top of each script or set up environment variables as preferred.
- No CSV import/export is included (per request).
- Threshold for alerting is 6.0 hours/day by default; change `THRESHOLD_HOURS` in `analyze.py`.

Files added
- `db_setup.py` — creates database and `usage_log` table
- `add_entry.py` — interactive insertion of daily usage
- `analyze.py` — prints summaries and alerts
- `sample_data.py` — inserts demo records for demo
- `requirements.txt` — project dependencies

If you'd like, I can:
- Add a simple GUI (Tkinter) for inputs
- Add per-user support and login
- Add matplotlib charts for visual reports
