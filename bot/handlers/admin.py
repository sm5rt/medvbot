# bot/handlers/admin.py
import asyncio
from datetime import datetime, timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from bot.services.db import (
    get_all_users, get_cache_by_tag, log_club_event,
    get_recent_history, set_custom_norm, update_season_config
)

SEASON_START, SEASON_END, ZERO_NORM = range(3)
SET_CUSTOM_NORM = range(1)

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🗓️ Сезон", callback_data="admin_season")],
        [InlineKeyboardButton("📜 История", callback_data="admin_history")],
        [InlineKeyboardButton("🐻 Мы (нормы)", callback_data="admin_we")]
    ]
    await update.callback_query.edit_message_text(
        "👮 *Админ-панель*", 
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# --- /season ---
async def admin_season_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("🗓️ Введите дату начала сезона (ДД.ММ.ГГГГ):")
    return SEASON_START

async def season_start_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dt = datetime.strptime(update.message.text.strip(), "%d.%m.%Y")
        context.user_data["new_season"] = {"start": dt.replace(tzinfo=timezone.utc)}
        await update.message.reply_text("🗓️ Введите дату окончания сезона (ДД.ММ.ГГГГ ЧЧ:ММ):")
        return SEASON_END
    except:
        await update.message.reply_text("❌ Неверный формат. Попробуйте: 01.01.2026")
        return SEASON_START

async def season_end_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dt = datetime.strptime(update.message.text.strip(), "%d.%m.%Y %H:%M")
        context.user_data["new_season"]["end"] = dt.replace(tzinfo=timezone.utc)
        await update.message.reply_text("🔢 Введите порог нулевой нормы (кубков, например 15000):")
        return ZERO_NORM
    except:
        await update.message.reply_text("❌ Неверный формат. Пример: 05.02.2026 10:24")
        return SEASON_END

async def zero_norm_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        threshold = int(update.message.text.strip())
        season = context.user_data["new_season"]
        update_season_config(
            start=season["start"].isoformat(),
            end=season["end"].isoformat(),
            threshold=threshold
        )
        await update.message.reply_text("✅ Сезон обновлён!")
        return ConversationHandler.END
    except:
        await update.message.reply_text("❌ Введите число.")
        return ZERO_NORM

# --- /history ---
async def admin_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = get_recent_history()
    if not history:
        await update.callback_query.message.reply_text("📜 История пуста.")
        return

    text = "📜 *Последние события:*\n"
    for h in history:
        action = {"joined": "вошёл", "left": "вышел", "registered": "зарегистрировался"}[h["action"]]
        ts = datetime.fromisoformat(h["timestamp"]).strftime("%d.%m.%Y %H:%M")
        text += f"{ts} — {h.get('brawl_tag', '?')} {action}\n"
    await update.callback_query.message.reply_text(text, parse_mode="Markdown")

# --- /we ---
async def admin_we(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_all_users()
    cache = {u["brawl_tag"]: get_cache_by_tag(u["brawl_tag"]) for u in users}
    buttons = []
    for u in users:
        name = cache[u["brawl_tag"]]["name"] if cache[u["brawl_tag"]] else u["brawl_tag"]
        buttons.append([InlineKeyboardButton(name, callback_data=f"set_norm_{u['brawl_tag']}")])
    await update.callback_query.message.reply_text(
        "🐻 *Выберите игрока для настройки нормы:*",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def start_set_norm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tag = query.data.split("_", 2)[2]
    context.user_data["norm_tag"] = tag
    await query.message.reply_text("🔢 Введите новую норму (0 — использовать общую):")
    return SET_CUSTOM_NORM

async def set_custom_norm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tag = context.user_data["norm_tag"]
    try:
        value = int(update.message.text.strip())
        if value <= 0:
            set_custom_norm(tag, None)
            msg = "🔄 Норма сброшена к общей."
        else:
            set_custom_norm(tag, value)
            msg = f"✅ Норма установлена: {value}"
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text("❌ Введите число.")
    return ConversationHandler.END
