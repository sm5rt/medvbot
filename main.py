# main.py
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters, ContextTypes
)
from config import BOT_TOKEN, CLUB_TAG, ADMIN_USER_ID
from bot.services.db import init_db
from bot.services.season import ensure_season_config

# Импорты хендлеров (без изменений)
from bot.handlers import start, navigator, participants, top, club, help
from bot.handlers.admin import (
    admin_menu, admin_season_start, season_start_input,
    season_end_input, zero_norm_input, admin_history,
    admin_we, start_set_norm, set_custom_norm,
    SEASON_START, SEASON_END, ZERO_NORM, SET_CUSTOM_NORM
)
from bot.jobs import check_club_changes, update_players_cache

logging.basicConfig(level=logging.INFO)

async def back_to_navigator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await navigator.navigator(update, context)

def main():
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не задан")

    init_db()
    asyncio.run(ensure_season_config())

    application = Application.builder().token(BOT_TOKEN).build()
    application.bot_data["CLUB_TAG"] = CLUB_TAG

    # ... (все хендлеры как раньше)

    job_queue = application.job_queue
    job_queue.run_repeating(check_club_changes.check_club_changes, interval=300, first=10)
    job_queue.run_repeating(update_players_cache.update_players_cache, interval=300, first=20)

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
