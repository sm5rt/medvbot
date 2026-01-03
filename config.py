import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
BRAWL_API_TOKEN = os.getenv("BRAWL_API_TOKEN")
CLUB_TAG = os.getenv("CLUB_TAG")

ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", 0))
DEFAULT_NORM = int(os.getenv("NORM", 3000))
MONGO_URI = os.getenv("MONGO_URI")

ASSETS_PATH = "assets"
