import sqlite3
import os


def get_conn():
    con = sqlite3.connect(os.environ["DB_PATH"])
    con.row_factory = sqlite3.Row
    return con

def init_db():
    os.makedirs(os.path.dirname(os.environ["DB_PATH"]), exist_ok=True)
    with get_conn() as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.executescript("""
            CREATE TABLE IF NOT EXISTS RowerCardio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                duration_min REAL,
                distance_m REAL,
                avg_500m REAL
            );
            CREATE TABLE IF NOT EXISTS ScaleWeight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                weight_kg REAL NOT NULL,
                body_fat REAL,
                muscle_mass REAL
            );
        """)