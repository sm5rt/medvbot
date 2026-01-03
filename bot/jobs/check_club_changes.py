import asyncio
from datetime import datetime, timezone
from telegram.ext import ContextTypes
from bot.services.brawl_api import get_club
from bot.services.db import get_db
from config import CLUB_TAG

async def check_club_changes(context: ContextTypes.DEFAULT_TYPE):
    try:
        club_data = await asyncio.to_thread(get_club, CLUB_TAG)
        current_members = {m["tag"].lstrip("#"): m for m in club_data["members"]}
        current_tags = set(current_members.keys())

        db = get_db()
        users_coll = db["users"]
        cache_coll = db["players_cache"]
        history_coll = db["club_history"]

        # Получаем всех зарегистрированных
        registered = await asyncio.to_thread(lambda: list(users_coll.find({})))
        registered_tags = {u["brawl_tag"] for u in registered}

        # Новые участники (вошли в клуб, но не в боте)
        # — не регистрируем автоматически, только логируем

        # Вышедшие из клуба
        left_tags = registered_tags - current_tags
        for tag in left_tags:
            await asyncio.to_thread(users_coll.delete_one, {"brawl_tag": tag})
            await asyncio.to_thread(history_coll.insert_one, {
                "brawl_tag": tag,
                "action": "left",
                "timestamp": datetime.now(timezone.utc)
            })

        # Новые в клубе (но не в боте) — не добавляем, ждём ручной регистрации

    except Exception as e:
        print(f"⚠️ Ошибка в check_club_changes: {e}")