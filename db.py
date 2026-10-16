import sqlite3
import os

DB_PATH = os.environ["DB_PATH"]

def get_conn():
    con = sqlite3.connect(os.environ["DB_PATH"])
    con.row_factory = sqlite3.Row
    return con

def init_db():
    os.makedirs(os.path.dirname(os.environ["DB_PATH"]), exist_ok=True)
    with get_conn() as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.executescript("""
            CREATE TABLE IF NOT EXISTS rower_cardio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                distance_m REAL,
                avg_500_m INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS weight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                weight_kg REAL NOT NULL,
                body_fat REAL,
                muscle_mass REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)