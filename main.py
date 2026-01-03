import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters, ContextTypes
)
from config import BOT_TOKEN, CLUB_TAG, ADMIN_USER_ID
from bot.handlers import start, navigator, participants, top, club, help
from bot.handlers.admin import (
    admin_menu, admin_season_start, season_start_input,
    season_end_input, zero_norm_input, admin_history,
    admin_we, start_set_norm, set_custom_norm,
    SEASON_START, SEASON_END, ZERO_NORM, SET_CUSTOM_NORM
)
from bot.jobs import check_club_changes, update_players_cache
from bot.services.season import ensure_season_config

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Обработчик "назад в навигатор"
async def back_to_navigator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await navigator.navigator(update, context)

def main():
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не задан. Проверьте переменные окружения.")

    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    application.bot_data["CLUB_TAG"] = CLUB_TAG

    # ====== Обычные команды ======
    application.add_handler(CommandHandler("start", start.start))
    application.add_handler(CommandHandler("help", help.help_handler))
    application.add_handler(CommandHandler("club", club.club_info))
    application.add_handler(CommandHandler("top", top.top_trophies))
    application.add_handler(CommandHandler("participants", participants.participants_list))
    application.add_handler(CommandHandler("navigator", navigator.navigator))

    # ====== Инлайн-навигация ======
    application.add_handler(CallbackQueryHandler(back_to_navigator, pattern="^back_to_navigator$"))
    application.add_handler(CallbackQueryHandler(participants.participants_list, pattern="^participants_list$"))
    application.add_handler(CallbackQueryHandler(participants.show_player, pattern=r"^player_[A-Z0-9]+$"))
    application.add_handler(CallbackQueryHandler(top.top_trophies, pattern="^top_trophies$"))
    application.add_handler(CallbackQueryHandler(top.top_progress, pattern="^top_progress$"))
    application.add_handler(CallbackQueryHandler(club.club_info, pattern="^club_info$"))
    application.add_handler(CallbackQueryHandler(help.help_handler, pattern="^help_info$"))

    # ====== Админка (только если задан ADMIN_USER_ID) ======
    if ADMIN_USER_ID is not None:
        application.add_handler(CommandHandler("season", admin_season_start))
        application.add_handler(CommandHandler("history", admin_history))
        application.add_handler(CommandHandler("we", admin_we))

        # Диалог настройки сезона
        season_conv = ConversationHandler(
            entry_points=[CallbackQueryHandler(admin_season_start, pattern="^admin_season$")],
            states={
                SEASON_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, season_start_input)],
                SEASON_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, season_end_input)],
                ZERO_NORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, zero_norm_input)],
            },
            fallbacks=[],
            per_user=True
        )
        application.add_handler(season_conv)

        # Диалог установки индивидуальной нормы
        norm_conv = ConversationHandler(
            entry_points=[CallbackQueryHandler(start_set_norm, pattern=r"^set_norm_[A-Z0-9]+$")],
            states={
                SET_CUSTOM_NORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_custom_norm)],
            },
            fallbacks=[],
            per_user=True
        )
        application.add_handler(norm_conv)

        application.add_handler(CallbackQueryHandler(admin_menu, pattern="^admin_menu$"))
        application.add_handler(CallbackQueryHandler(admin_history, pattern="^admin_history$"))
        application.add_handler(CallbackQueryHandler(admin_we, pattern="^admin_we$"))

    # ====== Фоновые задачи ======
    job_queue = application.job_queue
    job_queue.run_repeating(check_club_changes.check_club_changes, interval=300, first=10)   # каждые 5 мин
    job_queue.run_repeating(update_players_cache.update_players_cache, interval=300, first=20)

    # ====== Инициализация ======
    print("🔄 Инициализация бота...")
    asyncio.run(ensure_season_config())
    print("✅ Конфигурация сезона загружена.")

    # ====== Запуск ======
    print("🚀 Запуск бота...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
