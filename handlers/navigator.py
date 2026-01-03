from telegram import Update
from telegram.ext import ContextTypes
from keyboards import navigator


async def nav_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "nav:main":
        await query.edit_message_caption(
            caption="🧭 Навигация",
            reply_markup=navigator()
        )