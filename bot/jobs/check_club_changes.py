# bot/jobs/check_club_changes.py
import asyncio
from telegram.ext import ContextTypes
from bot.services.brawl_api import get_club
from bot.services.db import get_all_users, delete_user_by_tag, log_club_event
from config import CLUB_TAG

async def check_club_changes(context: ContextTypes.DEFAULT_TYPE):
    try:
        club_data = await asyncio.to_thread(get_club, CLUB_TAG)
        current_tags = {m["tag"].lstrip("#") for m in club_data["members"]}

        users = get_all_users()
        registered_tags = {u["brawl_tag"] for u in users}

        # Вышедшие из клуба
        left_tags = registered_tags - current_tags
        for tag in left_tags:
            delete_user_by_tag(tag)
            log_club_event(tag, "left")

    except Exception as e:
        print(f"⚠️ Ошибка в check_club_changes: {e}")
