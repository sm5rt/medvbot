from telegram import Update
from telegram.ext import ContextTypes
from pathlib import Path

PHOTO_PATH = Path("assets/start.jpg")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "Привет, медвежонок! 🐾\n"
        "Ты в клубе *ʕ·ᴥ·ʔмедвежата🐻*!\n\n"
        "Используй /navigator, чтобы начать!"
    )
    if PHOTO_PATH.exists():
        await update.message.reply_photo(
            photo=PHOTO_PATH.open("rb"),
            caption=caption,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(caption, parse_mode="Markdown")