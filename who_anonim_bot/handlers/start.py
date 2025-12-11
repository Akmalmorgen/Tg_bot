from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from keyboards.keyboards import main_menu_keyboard
from config.settings import BOT_USERNAME
from db.users import add_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await add_user(user.id)

    text = (
        "👻 *Who?Anonim Bot*\n\n"
        "Добро пожаловать!\n\n"
        "🔗 Анонимная ссылка\n"
        "🎲 Рулетка\n"
        "💬 Помощь\n\n"
        "Выберите действие ↓"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )


def register_start_handlers(app):
    app.add_handler(CommandHandler("start", start))
