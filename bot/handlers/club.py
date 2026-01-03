import asyncio
from datetime import datetime, timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.services.db import get_db
from bot.services.season import get_season_config
from pathlib import Path

async def club_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = get_db()
    users_coll = db["users"]
    cache_coll = db["players_cache"]
    season = await get_season_config()

    # Считаем участников
    total_members = await asyncio.to_thread(users_coll.count_documents, {})
    cache = await asyncio.to_thread(lambda: list(cache_coll.find({})))
    online_count = len([p for p in cache if p.get("last_updated", datetime.min).replace(tzinfo=timezone.utc) > 
                        datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)])

    # Трофеи клуба — сумма из кэша
    total_trophies = sum(p["trophies"] for p in cache)

    # Сезонная прибавка (требует хранения total_trophies на старте — упростим)
    # В данном проекте: не храним, поэтому покажем только текущие

    # Сколько выполнило норму
    completed = 0
    for user in await asyncio.to_thread(lambda: list(users_coll.find({}))):
        player_cache = next((p for p in cache if p["brawl_tag"] == user["brawl_tag"]), None)
        if not player_cache:
            continue
        from bot.services.season import calculate_progress
        prog = calculate_progress(season, user, player_cache["trophies"])
        if prog["done"]:
            completed += 1

    end_date = season["end_date"]
    now = datetime.now(timezone.utc)
    if now > end_date:
        days_left = 0
    else:
        delta = end_date - now
        days_left = delta.days

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