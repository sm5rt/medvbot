# bot/jobs/update_players_cache.py
import asyncio
from telegram.ext import ContextTypes
from bot.services.brawl_api import get_player
from bot.services.db import get_all_users, save_player_cache

async def update_players_cache(context: ContextTypes.DEFAULT_TYPE):
    try:
        users = get_all_users()
        for user in users:
            try:
                player = await asyncio.to_thread(get_player, user["brawl_tag"])
                club_name = player.get("club", {}).get("name", "")
                save_player_cache(
                    tag=user["brawl_tag"],
                    name=player["name"],
                    trophies=player["trophies"],
                    club_name=club_name
                )
            except Exception as e:
                print(f"❌ Не удалось обновить кэш для {user['brawl_tag']}: {e}")
    except Exception as e:
        print(f"⚠️ Ошибка в update_players_cache: {e}")
