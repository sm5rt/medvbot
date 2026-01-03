from telegram import Update
from telegram.ext import ContextTypes
from keyboards import navigator
from config import ASSETS_PATH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open(f"{ASSETS_PATH}/start.jpg", "rb"),
        caption="🐻 Добро пожаловать в клуб ʕ·ᴥ·ʔмедвежата🐻",
        reply_markup=navigator()
    )
