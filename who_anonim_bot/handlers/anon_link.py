import random
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from keyboards.keyboards import get_anon_link_menu, get_main_menu
from states.states import UserState
from db.links import (
    get_or_create_link,
    regenerate_link,
    get_owner_by_link,
)
from db.anon_chat import (
    set_anon_session,
    get_last_anon_partner,
)
from db.users import set_state


def register_anon_link_handlers(application):
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, anon_link_router)
    )


# ─────────────────────────────────────
# Роутер раздела "Моя анон-ссылка"
# ─────────────────────────────────────
async def anon_link_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # --- СМЕНИТЬ ССЫЛКУ ---
    if text == "🔄 Сменить ссылку":
        link = regenerate_link(user_id)

        await update.message.reply_text(
            "✅ <b>Ссылка обновлена</b>\n\n"
            f"🔗 https://t.me/{context.bot.username}?start={link}",
            parse_mode="HTML",
            reply_markup=get_anon_link_menu()
        )
        return

    # --- НАЗАД В МЕНЮ ---
    if text in ("⬅️ Назад", "🔙 Назад"):
        set_state(user_id, UserState.MAIN_MENU)
        await update.message.reply_text(
            "🏠 Главное меню",
            reply_markup=get_main_menu()
        )
        return

    # --- ОТВЕТ АНОНИМУ ---
    last_partner = get_last_anon_partner(user_id)
    if last_partner:
        await context.bot.send_message(
            last_partner,
            f"💬 <b>Ответ:</b>\n\n{text}",
            parse_mode="HTML"
        )
        await update.message.reply_text("✅ Ответ отправлен")
        return
