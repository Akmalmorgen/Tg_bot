from telegram.ext import CommandHandler
from keyboards.keyboards import main_menu
from db.users import add_user, is_banned
from states.states import set_state

async def cmd_start(update, context):
    user = update.effective_user
    await add_user(user.id)

    if await is_banned(user.id):
        await update.message.reply_text("🚫 Вы заблокированы.")
        return

    welcome = (
        "╔═══════════════════════════╗\n"
        "║   👻 <b>Who?Anonim™</b> Bot   ║\n"
        "╚═══════════════════════════╝\n\n"
        f"Привет, <b>{user.first_name}</b>! 🎭\n\n"
        "Ты можешь:\n"
        "🔗 Создать анонимную ссылку\n"
        "🎲 Найти собеседника в рулетке\n"
        "💬 Общаться полностью анонимно\n\n"
        "Выберите действие ниже:"
    )

    await update.message.reply_text(
        welcome,
        parse_mode="HTML",
        reply_markup=main_menu()
    )

    await set_state(user.id, "MAIN_MENU")

def register_start_handlers(app):
    app.add_handler(CommandHandler("start", cmd_start))
