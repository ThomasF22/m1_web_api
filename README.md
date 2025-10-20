# FastAPI app (User API + UI simple)

This project is a small FastAPI application using SQLModel and MySQL (via PyMySQL).

Prerequisites
- Python 3.11+ (recommended)
- MySQL server running locally (or adjust DATABASE_URL in `database.py`)

Quick start (PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create the database and tables

- Ensure MySQL server is running and a database named `2025_M1` exists. If it does not, create it in MySQL:

```powershell
# open mysql shell (example; adapt if you use a password)
mysql -u root -p
-- then inside mysql shell:
CREATE DATABASE IF NOT EXISTS `2025_M1` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

4. Initialize tables (uses `DATABASE_URL` from `database.py`)

```powershell
python init_db.py
```

5. Run the app with Uvicorn

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/ in your browser.

Notes
- If your MySQL server requires a password or different user, update `DATABASE_URL` in `database.py`.
- For production, do not use `--reload` and configure a proper ASGI server/process manager.