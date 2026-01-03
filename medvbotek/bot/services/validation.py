from bot.services.brawl_api import get_player
from config import CLUB_TAG

def is_player_in_club(brawl_tag: str) -> bool:
    try:
        player = get_player(brawl_tag)
        club = player.get("club")
        return club and club.get("tag", "").lstrip("#") == CLUB_TAG
    except:
        return False