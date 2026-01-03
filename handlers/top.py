from telegram import Update
from telegram.ext import ContextTypes
from db import players_cache
from keyboards import back_to_nav


async def top_trophies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players = list(players_cache.find().sort("trophies", -1))
    text = "🏆 Топ по кубкам:\n\n"

    for i, p in enumerate(players, 1):
        text += f"{i}. {p['name']} — {p['trophies']}\n"

    await update.callback_query.edit_message_caption(
        caption=text,
        reply_markup=back_to_nav()
    )
