from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters

from keyboards.keyboards import (
    get_main_menu,
)
from states.states import UserState
from db.users import set_state


def register_menu_handlers(application):
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router)
    )


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # --- МОЯ АНОН-ССЫЛКА ---
    if text == "🔗 Моя анон-ссылка":
        from handlers.anon_link import show_my_link
        await show_my_link(update, context)
        return

    # --- РУЛЕТКА ---
    if text == "🎲 Рулетка":
        from handlers.roulette import start_roulette
        await start_roulette(update, context)
        return

    # --- ПОМОЩЬ ---
    if text == "💬 Помощь":
        help_text = (
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 <b>ПОМОЩЬ</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "По всем вопросам:\n"
            "• Помощь\n"
            "• Доработки\n"
            "• Партнёрство\n\n"
            "📱 @who_mercy\n"
            "━━━━━━━━━━━━━━━━━━━━━━━"
        )

        await update.message.reply_text(
            help_text,
            parse_mode="HTML",
            reply_markup=get_main_menu()
        )
        return

    # --- НАЗАД В МЕНЮ ---
    if text == "⬅️ Назад" or text == "🔙 Назад":
        set_state(user_id, UserState.MAIN_MENU)
        await update.message.reply_text(
            "🏠 Главное меню",
            reply_markup=get_main_menu()
        )
        return
