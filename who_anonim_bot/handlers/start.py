from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from keyboards.keyboards import get_main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Добро пожаловать в Who?Anonim™",
        reply_markup=get_main_menu()
    )


def register_start_handlers(app):
    app.add_handler(CommandHandler("start", start))
