from pymongo import MongoClient
from config import MONGO_URI

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGO_URI)
        _db = _client["brawl_bears"]
    return _db