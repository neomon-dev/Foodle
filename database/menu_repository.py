import json
from datetime import datetime, timezone

from database.db import get_connection, initialize_database


initialize_database()


def save_session(title, source_language, target_language, menu_data, notes=""):
    conn = get_connection()
    try:
        payload = json.dumps(menu_data, ensure_ascii=False)
        cursor = conn.execute(
            """
            INSERT INTO translation_sessions (created_at, title, source_language, target_language, menu_data, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                title,
                source_language,
                target_language,
                payload,
                notes,
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def list_sessions():
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, created_at, title, source_language, target_language, notes
            FROM translation_sessions
            ORDER BY id DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_session(session_id):
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT id, created_at, title, source_language, target_language, menu_data, notes
            FROM translation_sessions
            WHERE id = ?
            """,
            (session_id,),
        ).fetchone()
        if row is None:
            return None
        payload = dict(row)
        payload["menu_data"] = json.loads(payload["menu_data"])
        return payload
    finally:
        conn.close()


def delete_session(session_id):
    conn = get_connection()
    try:
        conn.execute(
            "DELETE FROM translation_sessions WHERE id = ?",
            (session_id,),
        )
        conn.commit()
        return True
    finally:
        conn.close()
