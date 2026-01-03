import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BRAWL_API_TOKEN = os.getenv("BRAWL_API_TOKEN")
CLUB_TAG = os.getenv("CLUB_TAG")

ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID")) if os.getenv("ADMIN_USER_ID") else None
NORM = int(os.getenv("NORM", 3000))
DB_PATH = os.getenv("DB_PATH", "data.db")  # путь к SQLite
