import requests
from config import BRAWL_API_TOKEN

BASE_URL = "https://api.brawlstars.com/v1"
HEADERS = {
    "Authorization": f"Bearer {BRAWL_API_TOKEN}",
    "Accept": "application/json"
}

def get_player(tag: str):
    url = f"{BASE_URL}/players/%23{tag}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_club(tag: str):
    url = f"{BASE_URL}/clubs/%23{tag}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()