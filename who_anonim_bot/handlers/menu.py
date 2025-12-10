# who_anonim_bot/handlers/menu.py
from telegram.ext import MessageHandler, filters
from keyboards.keyboards import main_menu_keyboard
from db.users import get_user_state, set_user_state
from handlers.anon_link import show_my_link
from handlers.roulette import start_roulette
from handlers.admin import open_admin_panel

async def menu_router(update, context):
    text = update.message.text
    uid = update.effective_user.id

    if text == "🔗 Моя анон-ссылка":
        return await show_my_link(update, context)
    if text == "🎲 Рулетка":
        return await start_roulette(update, context)
    if text == "💬 Помощь":
        await update.message.reply_text("Для помощи и доработок: @who_mercy", reply_markup=main_menu_keyboard(uid in context.bot.bot_data.get("admins", [])))
    if text == "⚙️ Админ-панель":
        return await open_admin_panel(update, context)

def register_menu_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))
