import os
import sqlite3
from pathlib import Path

from config import DB_PATH


def _resolve_db_path():
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection():
    db_path = _resolve_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS translation_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                title TEXT NOT NULL,
                source_language TEXT NOT NULL,
                target_language TEXT NOT NULL,
                menu_data TEXT NOT NULL,
                notes TEXT DEFAULT ''
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
