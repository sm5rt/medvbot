from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def back_to_nav():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧭 Навигация", callback_data="nav:main")]
    ])


def navigator():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Участники", callback_data="nav:participants")],
        [InlineKeyboardButton("🏆 Топ", callback_data="nav:top:trophies")],
        [InlineKeyboardButton("🧸 Клуб", callback_data="nav:club")],
        [InlineKeyboardButton("❓ Помощь", callback_data="nav:help")]
    ])