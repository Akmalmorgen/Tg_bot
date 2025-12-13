from telegram import Update
from telegram.ext import ContextTypes

from keyboards.keyboards import get_main_menu
from states.states import UserState
from db.users import set_state, get_state

from handlers.anon_link import show_my_link
from handlers.roulette import start_roulette
from handlers.start import show_help


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    state = get_state(user_id)

    if text == "🔙 Назад":
        set_state(user_id, UserState.MAIN_MENU)
        await update.message.reply_text(
            "🏠 Главное меню",
            reply_markup=get_main_menu()
        )
        return

    if state == UserState.MAIN_MENU:
        if text == "🔗 Моя анон-ссылка":
            await show_my_link(update, context)

        elif text == "🎲 Рулетка":
            await start_roulette(update, context)

        elif text == "💬 Помощь":
            await show_help(update, context)

        else:
            await update.message.reply_text(
                "❗ Используйте кнопки ниже",
                reply_markup=get_main_menu()
            )
