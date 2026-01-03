import asyncio
from datetime import datetime, timezone
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from bot.services.db import get_db
from bot.services.season import get_season_config, calculate_progress

async def participants_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = get_db()
    users = await asyncio.to_thread(lambda: list(db["users"].find({})))
    cache = {p["brawl_tag"]: p for p in await asyncio.to_thread(lambda: list(db["players_cache"].find({})))}

    buttons = []
    for user in users:
        name = cache.get(user["brawl_tag"], {}).get("name", user["brawl_tag"])
        buttons.append([InlineKeyboardButton(name, callback_data=f"player_{user['brawl_tag']}")])
    buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_navigator")])

    if update.callback_query:
        await update.callback_query.edit_message_text(
            "👥 *Список участников:*", 
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await update.message.reply_text(
            "👥 *Список участников:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

async def show_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tag = query.data.split("_", 1)[1]

    db = get_db()
    user = await asyncio.to_thread(db["users"].find_one, {"brawl_tag": tag})
    if not user:
        await query.edit_message_text("❌ Игрок не найден.")
        return

    cache = await asyncio.to_thread(db["players_cache"].find_one, {"brawl_tag": tag})
    if not cache:
        await query.edit_message_text("❌ Данные игрока временно недоступны.")
        return

    season = await get_season_config()
    prog = calculate_progress(season, user, cache["trophies"])

    # Дни в клубе
    joined = user["joined_club_at"]
    now = datetime.now(timezone.utc)
    days_in_club = (now - joined).days

    # Дней до конца сезона
    end = season["end_date"]
    delta = end - now
    total_hours = int(delta.total_seconds() // 3600) if now < end else 0
    days_left = delta.days if now < end else 0

    text = (
        f"🐻 *Ник в игре:* {cache['name']}\n"
        f"🔖 *ID аккаунта:* #{tag}\n"
        f"🏰 *Клуб:* {cache.get('club', {}).get('name', '—')}\n"
        f"📅 *В клубе с:* {joined.strftime('%d/%m/%Y')} ({days_in_club} дней)\n\n"
        f"📊 *Сезонная статистика:*\n"
        f"Норма трофеев: {prog['norm']}\n"
        f"Начало сезона: {prog['start']} кубков\n"
        f"Текущий прогресс: {prog['current']} (+{prog['gained']})\n"
        f"✅ Норма выполнена: {'да' if prog['done'] else 'нет'}\n"
        f"⏳ Дней до конца сезона: {days_left} дней ({total_hours} ч)"
    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Назад к списку", callback_data="participants_list")]
        ])
    )