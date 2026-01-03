from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from config import BOT_TOKEN
from handlers.start import start
from handlers.navigator import nav_handler
from handlers.participants import participants
from handlers.top import top_trophies
from handlers.club import club_info
from handlers.help import help_cmd
from jobs import update_players_cache, check_club_changes


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))

app.add_handler(CallbackQueryHandler(nav_handler, pattern="^nav:"))
app.add_handler(CallbackQueryHandler(participants, pattern="^nav:participants"))
app.add_handler(CallbackQueryHandler(top_trophies, pattern="^nav:top"))
app.add_handler(CallbackQueryHandler(club_info, pattern="^nav:club"))

app.job_queue.run_repeating(update_players_cache, interval=300, first=10)
app.job_queue.run_repeating(check_club_changes, interval=300, first=20)

app.run_polling()
