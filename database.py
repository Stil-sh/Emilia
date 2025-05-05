import sqlite3
from datetime import datetime

def init_db():
    """Инициализирует БД."""
    conn = sqlite3.connect("arts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sent_arts (
            art_url TEXT PRIMARY KEY,
            sent_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_art_sent(art_url: str) -> bool:
    """Проверяет, был ли арт отправлен ранее."""
    conn = sqlite3.connect("arts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_arts WHERE art_url = ?", (art_url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def mark_art_as_sent(art_url: str):
    """Добавляет арт в БД."""
    conn = sqlite3.connect("arts.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sent_arts (art_url, sent_at) VALUES (?, ?)",
        (art_url, datetime.now())
    )
    conn.commit()
    conn.close()
