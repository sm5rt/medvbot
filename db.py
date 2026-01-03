from pymongo import MongoClient
from config import MONGO_URI
from datetime import datetime, timezone

client = MongoClient(MONGO_URI)
db = client["brawl_bot"]

users = db.users
players_cache = db.players_cache
club_history = db.club_history
season = db.season


def utcnow():
    return datetime.now(timezone.utc)