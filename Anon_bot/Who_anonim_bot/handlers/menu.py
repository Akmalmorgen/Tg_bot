from telegram.ext import MessageHandler, filters
from states.states import get_state, set_state
from keyboards.keyboards import main_menu
from handlers.anon_link import show_my_link
from handlers.roulette import start_roulette
from handlers.admin import open_admin_panel

async def menu_router(update, context):
    user_id = update.effective_user.id
    text = update.message.text
    state = await get_state(user_id)

    if text == "🔗 Моя анон-ссылка":
        return await show_my_link(update, context)

    if text == "🎲 Рулетка":
        return await start_roulette(update, context)

    if text == "💬 Помощь":
        help_text = (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 <b>ПОМОЩЬ</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Нужна помощь, партнёрство или доработка?\n"
            "👉 @who_mercy\n"
        )
        return await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=main_menu())

    if text == "⚙️ Админ-панель":
        return await open_admin_panel(update, context)

def register_menu_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT, menu_router))
