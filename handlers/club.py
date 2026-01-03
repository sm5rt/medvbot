from telegram import Update
from telegram.ext import ContextTypes
from brawl_api import get_club
from keyboards import back_to_nav


async def club_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    club = get_club()
    text = (
        f"🧸 {club['name']}\n"
        f"Тег: {club['tag']}\n"
        f"Участники: {club['membersCount']}\n"
        f"Кубки: {club['trophies']}"
    )

    await update.callback_query.edit_message_caption(
        caption=text,
        reply_markup=back_to_nav()
    )
