# bot/services/db.py
import sqlite3
import os
import json
from datetime import datetime, timezone
from threading import Lock
from config import DB_PATH

_lock = Lock()

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # для dict-подобного доступа
    return conn

def init_db():
    with _lock:
        conn = get_db()
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                brawl_tag TEXT UNIQUE NOT NULL,
                brawl_name TEXT,
                joined_club_at TEXT NOT NULL,
                joined_bot_at TEXT NOT NULL,
                season_start_trophies INTEGER NOT NULL,
                custom_norm INTEGER
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS players_cache (
                brawl_tag TEXT PRIMARY KEY,
                name TEXT,
                trophies INTEGER,
                club_name TEXT,
                last_updated TEXT
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS club_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brawl_tag TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS season_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                zero_norm_threshold INTEGER NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

# === USERS ===
def save_user(user_data):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO users (
                telegram_id, brawl_tag, brawl_name, joined_club_at,
                joined_bot_at, season_start_trophies, custom_norm
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data["telegram_id"],
            user_data["brawl_tag"],
            user_data.get("brawl_name"),
            user_data["joined_club_at"],
            user_data["joined_bot_at"],
            user_data["season_start_trophies"],
            user_data.get("custom_norm")
        ))
        conn.commit()
        conn.close()

def get_all_users():
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

def get_user_by_tag(tag):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE brawl_tag = ?", (tag,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

def delete_user_by_tag(tag):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE brawl_tag = ?", (tag,))
        conn.commit()
        conn.close()

def set_custom_norm(tag, norm):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        if norm is None:
            cur.execute("UPDATE users SET custom_norm = NULL WHERE brawl_tag = ?", (tag,))
        else:
            cur.execute("UPDATE users SET custom_norm = ? WHERE brawl_tag = ?", (norm, tag))
        conn.commit()
        conn.close()

# === PLAYERS CACHE ===
def save_player_cache(tag, name, trophies, club_name):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO players_cache (brawl_tag, name, trophies, club_name, last_updated)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (tag, name, trophies, club_name))
        conn.commit()
        conn.close()

def get_all_cache():
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM players_cache")
        rows = cur.fetchall()
        conn.close()
        return {row["brawl_tag"]: dict(row) for row in rows}

def get_cache_by_tag(tag):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM players_cache WHERE brawl_tag = ?", (tag,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

# === CLUB HISTORY ===
def log_club_event(tag, action):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO club_history (brawl_tag, action, timestamp)
            VALUES (?, ?, datetime('now'))
        ''', (tag, action))
        conn.commit()
        conn.close()

def get_recent_history(limit=20):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM club_history ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

# === SEASON ===
def init_season_config(start, end, threshold):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT OR IGNORE INTO season_config (id, start_date, end_date, zero_norm_threshold)
            VALUES (1, ?, ?, ?)
        ''', (start, end, threshold))
        conn.commit()
        conn.close()

def get_season_config():
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM season_config WHERE id = 1")
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

def update_season_config(start, end, threshold):
    with _lock:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            UPDATE season_config SET start_date = ?, end_date = ?, zero_norm_threshold = ?
            WHERE id = 1
        ''', (start, end, threshold))
        conn.commit()
        conn.close()
