from telegram import Update
from telegram.ext import ContextTypes
from keyboards import navigator
from config import ASSETS_PATH
from utils import get_photo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=get_photo(f"{ASSETS_PATH}/start.jpg"),
        caption="🐻 Добро пожаловать в клуб ʕ·ᴥ·ʔмедвежата🐻",
        reply_markup=navigator()
    )
