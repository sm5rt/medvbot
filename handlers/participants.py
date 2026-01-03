from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db import users, players_cache
from utils import format_date, days_in_club
from keyboards import back_to_nav


async def participants(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = []
    for user in users.find():
        buttons.append([
            InlineKeyboardButton(
                user["player_name"],
                callback_data=f"player:{user['player_tag']}"
            )
        ])

    await update.callback_query.edit_message_caption(
        caption="👥 Участники клуба",
        reply_markup=InlineKeyboardMarkup(buttons + [[
            InlineKeyboardButton("🔙 Назад", callback_data="nav:main")
        ]])
    )
