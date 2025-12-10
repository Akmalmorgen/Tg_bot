from telegram import Update
from telegram.ext import ContextTypes

from keyboards import main_menu
from users import add_user
from config import BOT_NAME


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Записываем пользователя в базу
    await add_user(user_id)

    welcome_text = (
        "╔══════════════════════╗\n"
        f"     👻 <b>{BOT_NAME}</b> Bot\n"
        "╚══════════════════════╝\n\n"
        f"Привет, <b>{user.first_name}</b>!\n\n"
        "🔐 Я бот для анонимного общения.\n"
        "Ты можешь:\n"
        "• общаться по анонимной ссылке\n"
        "• искать людей в рулетке\n"
        "• оставаться полностью скрытым\n\n"
        "Выбери действие 👇"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )
