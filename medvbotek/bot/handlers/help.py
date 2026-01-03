from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from pathlib import Path

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "*ʕ·ᴥ·ʔмедвежата🐻 — Справка*\n\n"
        "*/start* — приветствие\n"
        "*/navigator* — главное меню\n"
        "*/participants* — список участников с деталями\n"
        "*/top* — топ по кубкам и прогрессу\n"
        "*/club* — информация о клубе\n"
        "*/help* — эта справка\n\n"
        "Админ-команды:\n"
        "*/season* — настроить сезон\n"
        "*/history* — история входов/выходов\n"
        "*/we* — настроить индивидуальные нормы"
    )
    photo_path = Path("assets/help.jpg")
    if photo_path.exists():
        await update.message.reply_photo(
            photo=photo_path.open("rb"),
            caption=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_navigator")]])
        )
    else:
        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_navigator")]])
        )