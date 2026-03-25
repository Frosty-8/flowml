import sqlite3
import uuid
from datetime import datetime

DB_PATH = "flowml.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        path TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_dataset(name, dtype, path):
    dataset_id = str(uuid.uuid4())

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO datasets (id, name, type, path, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (dataset_id, name, dtype, path, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return dataset_id


def get_dataset(dataset_id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM datasets WHERE id = ?", (dataset_id,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "type": row[2],
        "path": row[3]
    }