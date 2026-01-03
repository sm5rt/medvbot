import asyncio
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from bot.services.db import get_db
from bot.services.season import get_season_config, calculate_progress

async def top_trophies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = get_db()
    users = await asyncio.to_thread(lambda: list(db["users"].find({})))
    cache = {p["brawl_tag"]: p for p in await asyncio.to_thread(lambda: list(db["players_cache"].find({})))}

    players = []
    for u in users:
        c = cache.get(u["brawl_tag"])
        if c:
            players.append((c["name"], c["trophies"], u["brawl_tag"]))
    players.sort(key=lambda x: x[1], reverse=True)

    text = "🏆 *Топ по кубкам:*\n"
    for i, (name, trophies, tag) in enumerate(players[:10], 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        text += f"{medal} {name} — {trophies}\n"

    await _send_top_message(update, text, "trophy")

async def top_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = get_db()
    users = await asyncio.to_thread(lambda: list(db["users"].find({})))
    cache = {p["brawl_tag"]: p for p in await asyncio.to_thread(lambda: list(db["players_cache"].find({})))}
    season = await get_season_config()

    players = []
    for u in users:
        c = cache.get(u["brawl_tag"])
        if c:
            prog = calculate_progress(season, u, c["trophies"])
            players.append((c["name"], prog["gained"], prog["percent"], u["brawl_tag"]))
    players.sort(key=lambda x: x[1], reverse=True)

    text = "📈 *Топ по прогрессу:*\n"
    for i, (name, gained, percent, tag) in enumerate(players[:10], 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        text += f"{medal} {name} — +{gained} ({percent}%)\n"

    await _send_top_message(update, text, "progress")

async def _send_top_message(update, text, mode):
    buttons = []
    if mode == "trophy":
        buttons.append([InlineKeyboardButton("📊 К топу прогресса", callback_data="top_progress")])
    else:
        buttons.append([InlineKeyboardButton("🏆 К топу кубков", callback_data="top_trophies")])
    buttons.append([InlineKeyboardButton("🔙 Назад в навигатор", callback_data="back_to_navigator")])

    photo_path = "assets/top.jpg"
    from pathlib import Path
    if Path(photo_path).exists():
        await update.callback_query.message.reply_photo(
            photo=open(photo_path, "rb"),
            caption=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await update.callback_query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )