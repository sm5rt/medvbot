from telegram import Update
from telegram.ext import ContextTypes
from keyboards import back_to_nav


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ Команды бота:\n/start\n/navigator\n/participants\n/top\n/club",
        reply_markup=back_to_nav()
    )
