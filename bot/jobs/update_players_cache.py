import asyncio
from datetime import datetime, timezone
from telegram.ext import ContextTypes
from bot.services.brawl_api import get_player
from bot.services.db import get_db

async def update_players_cache(context: ContextTypes.DEFAULT_TYPE):
    try:
        db = get_db()
        users_coll = db["users"]
        cache_coll = db["players_cache"]

        users = await asyncio.to_thread(lambda: list(users_coll.find({})))
        for user in users:
            try:
                player = await asyncio.to_thread(get_player, user["brawl_tag"])
                cache_entry = {
                    "brawl_tag": user["brawl_tag"],
                    "name": player["name"],
                    "trophies": player["trophies"],
                    "club": player.get("club", {}),
                    "last_updated": datetime.now(timezone.utc)
                }
                await asyncio.to_thread(
                    cache_coll.replace_one,
                    {"brawl_tag": user["brawl_tag"]},
                    cache_entry,
                    upsert=True
                )
            except Exception as e:
                print(f"❌ Не удалось обновить кэш для {user['brawl_tag']}: {e}")

    except Exception as e:
        print(f"⚠️ Ошибка в update_players_cache: {e}")