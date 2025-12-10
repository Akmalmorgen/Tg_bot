# who_anonim_bot/handlers/start.py
from telegram.ext import CommandHandler
from keyboards.keyboards import main_menu_keyboard
from db.users import ensure_user
from db.users import get_user_state, set_user_state

async def cmd_start(update, context):
    user = update.effective_user
    await ensure_user(user.id, user.first_name or "Аноним")
    await set_user_state(user.id, "MAIN_MENU")
    await update.message.reply_text(
        f"Привет, {user.first_name or 'Аноним'}!",
        reply_markup=main_menu_keyboard(user.id in context.bot.bot_data.get("admins", []))
    )

def register_start_handlers(app):
    app.add_handler(CommandHandler("start", cmd_start))
