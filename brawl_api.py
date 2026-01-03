import requests
from config import BRAWL_API_TOKEN

BASE_URL = "https://api.brawlstars.com/v1"
HEADERS = {
    "Authorization": f"Bearer {BRAWL_API_TOKEN}"
}


def get_club():
    return requests.get(
        f"{BASE_URL}/clubs/%23{CLUB_TAG}",
        headers=HEADERS,
        timeout=10
    ).json()


def get_player(tag: str):
    tag = tag.replace("#", "")
    return requests.get(
        f"{BASE_URL}/players/%23{tag}",
        headers=HEADERS,
        timeout=10
    ).json()