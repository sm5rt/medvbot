# bot/services/db.py
import sqlite3
import os
from threading import Lock

DB_PATH = os.getenv("DB_PATH", "data.db")
_lock = Lock()

def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with _lock:
        conn = get_db()
        cur = conn.cursor()

        # Таблица пользователей
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                brawl_tag TEXT UNIQUE,
                brawl_name TEXT,
                joined_club_at TEXT,
                joined_bot_at TEXT,
                season_start_trophies INTEGER,
                custom_norm INTEGER
            )
        ''')

        # Кэш игроков
        cur.execute('''
            CREATE TABLE IF NOT EXISTS players_cache (
                brawl_tag TEXT PRIMARY KEY,
                name TEXT,
                trophies INTEGER,
                club_name TEXT,
                last_updated TEXT
            )
        ''')

        # История клуба
        cur.execute('''
            CREATE TABLE IF NOT EXISTS club_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brawl_tag TEXT,
                action TEXT,
                timestamp TEXT
            )
        ''')

        # Сезон
        cur.execute('''
            CREATE TABLE IF NOT EXISTS season_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                start_date TEXT,
                end_date TEXT,
                zero_norm_threshold INTEGER
            )
        ''')

        conn.commit()
        conn.close()
