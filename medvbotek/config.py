import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
BRAWL_API_TOKEN = os.getenv("BRAWL_API_TOKEN")
CLUB_TAG = os.getenv("CLUB_TAG")

ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID")) if os.getenv("ADMIN_USER_ID") else None
NORM = int(os.getenv("NORM", 3000))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
