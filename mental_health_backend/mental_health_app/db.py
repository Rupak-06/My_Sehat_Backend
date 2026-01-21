import sqlite3
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

DB_NAME = "app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Risk Events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS risk_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message_id INTEGER,
            risk_level TEXT NOT NULL,
            self_harm_detected BOOLEAN NOT NULL,
            keyword_score INTEGER,
            reasons_json TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(message_id) REFERENCES messages(id)
        )
    ''')

    # Daily Summary table
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            summary_text TEXT,
            risk_level TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Helper functions for persistence

def save_message(user_id: str, role: str, text: str) -> int:
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute(
        "INSERT INTO messages (user_id, role, text, created_at) VALUES (?, ?, ?, ?)",
        (user_id, role, text, created_at)
    )
    msg_id = c.lastrowid
    conn.commit()
    conn.close()
    return msg_id

def save_risk_event(user_id: str, message_id: Optional[int], risk_level: str, self_harm_detected: bool, keyword_score: int, reasons: List[str]):
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    reasons_json = json.dumps(reasons)
    c.execute(
        '''INSERT INTO risk_events 
           (user_id, message_id, risk_level, self_harm_detected, keyword_score, reasons_json, created_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (user_id, message_id, risk_level, int(self_harm_detected), keyword_score, reasons_json, created_at)
    )
    conn.commit()
    conn.close()

def save_daily_summary(user_id: str, date: str, summary_text: str, risk_level: str):
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute(
        '''INSERT INTO daily_summaries 
           (user_id, date, summary_text, risk_level, created_at) 
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, date, summary_text, risk_level, created_at)
    )
    conn.commit()
    conn.close()

def get_daily_summary(user_id: str, date: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM daily_summaries WHERE user_id = ? AND date = ?", (user_id, date))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None
