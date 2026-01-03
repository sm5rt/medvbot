# bot/handlers/club.py
import asyncio
from datetime import datetime, timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.services.db import get_all_users, get_cache_by_tag
from bot.services.season import get_season_config_async, calculate_progress
from pathlib import Path

async def club_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    cache_dict = {u["brawl_tag"]: get_cache_by_tag(u["brawl_tag"]) for u in users}

    total_members = len(users)
    online_count = sum(
        1 for cache in cache_dict.values()
        if cache and cache.get("last_updated")
    )

    total_trophies = sum(cache["trophies"] for cache in cache_dict.values() if cache)

    season = await get_season_config_async()
    completed = 0
    for user in users:
        cache = cache_dict.get(user["brawl_tag"])
        if cache:
            prog = calculate_progress(season, user, cache["trophies"])
            if prog["done"]:
                completed += 1

    end_date = datetime.fromisoformat(season["end_date"])
    now = datetime.now(timezone.utc)
    days_left = max(0, (end_date - now).days)

    text = (
        f"🏰 *Название:* ʕ·ᴥ·ʔмедвежата🐻\n"
        f"🔖 *Тег:* #{context.bot_data['CLUB_TAG']}\n"
        f"👥 *Участников:* {total_members} ({online_count} онлайн)\n"
        f"🏆 *Трофеев:* {total_trophies:,}\n"
        f"🎯 *Норму выполнили:* {completed} из {total_members}\n"
        f"📅 *Сезон:* 01.01.2026 — {end_date.strftime('%d.%m.%Y %H:%M')}\n"
        f"⏳ *До конца сезона:* {days_left} дней"
    )

    photo_path = Path("assets/club.jpg")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_navigator")]])
    if photo_path.exists():
        await update.callback_query.message.reply_photo(
            photo=photo_path.open("rb"),
            caption=text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
