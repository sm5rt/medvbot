from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from config import ADMIN_USER_ID

async def navigator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        message_func = query.edit_message_caption if query.message.caption else query.edit_message_text
        photo_func = query.edit_message_media if query.message.photo else None
    else:
        message_func = update.message.reply_text
        photo_func = None

    keyboard = [
        [InlineKeyboardButton("👥 Участники", callback_data="participants_list")],
        [InlineKeyboardButton("🏆 Топ", callback_data="top_trophies")],
        [InlineKeyboardButton("🏰 Клуб", callback_data="club_info")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help_info")]
    ]
    if update.effective_user.id == ADMIN_USER_ID:
        keyboard.append([InlineKeyboardButton("👮 Админка", callback_data="admin_menu")])

    caption = "🧭 *Медвежий навигатор*\nВыбери, куда отправимся!"
    if photo_func:
        from pathlib import Path
        photo_path = Path("assets/navigator.jpg")
        if photo_path.exists():
            from telegram import InputMediaPhoto
            await photo_func(InputMediaPhoto(photo_path.open("rb"), caption=caption, parse_mode="Markdown"))
            await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
            return

    await message_func(caption, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")