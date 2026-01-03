import asyncio
from db import players_cache, users, club_history, utcnow
from brawl_api import get_club, get_player


async def update_players_cache(context):
    club = await asyncio.to_thread(get_club)
    for member in club.get("members", []):
        tag = member["tag"].replace("#", "")
        player = await asyncio.to_thread(get_player, tag)
        players_cache.update_one(
            {"player_tag": tag},
            {"$set": {
                "player_tag": tag,
                "name": player["name"],
                "trophies": player["trophies"],
                "club": player.get("club"),
                "updated_at": utcnow()
            }},
            upsert=True
        )


async def check_club_changes(context):
    club = await asyncio.to_thread(get_club)
    current_tags = {m["tag"].replace("#", "") for m in club["members"]}
    saved_users = list(users.find())

    for user in saved_users:
        if user["player_tag"] not in current_tags:
            users.delete_one({"player_tag": user["player_tag"]})
            club_history.insert_one({
                "player_tag": user["player_tag"],
                "player_name": user["player_name"],
                "action": "leave",
                "timestamp": utcnow()
            })
