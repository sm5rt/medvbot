# bot/handlers/top.py
import asyncio
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from bot.services.db import get_all_users, get_cache_by_tag
from bot.services.season import get_season_config_async, calculate_progress

async def top_trophies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    cache = {u["brawl_tag"]: get_cache_by_tag(u["brawl_tag"]) for u in users}

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
    users = get_all_users()
    cache = {u["brawl_tag"]: get_cache_by_tag(u["brawl_tag"]) for u in users}
    season = await get_season_config_async()

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

    from pathlib import Path
    photo_path = Path("assets/top.jpg")
    if photo_path.exists():
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
