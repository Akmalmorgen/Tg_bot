from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from keyboards.keyboards import get_main_menu
from db.users import add_user
from db.links import handle_start_link


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    await add_user(user.id, user.username)

    # если переход по анонимной ссылке
    if context.args:
        code = context.args[0]
        if await handle_start_link(update, context, code):
            return

    welcome_text = (
        "╔═══════════════════════════╗\n"
        "║   👻 Who?Anonim™ Bot   ║\n"
        "╚═══════════════════════════╝\n\n"
        f"Привет, {user.first_name}! 🎭\n\n"
        "🔐 Я бот для анонимного общения.\n"
        "Ты можешь:\n\n"
        "🔗 Создать свою анонимную ссылку\n"
        "🎲 Общаться в случайной рулетке\n"
        "💬 Оставаться полностью анонимным\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 Выберите действие ниже:"
    )

    await context.bot.send_message(
        chat_id=chat_id,
        text=welcome_text,
        reply_markup=get_main_menu(user.id)
    )


def register_start_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
