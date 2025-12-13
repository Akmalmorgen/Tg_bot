from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from keyboards.keyboards import get_main_menu
from states.states import UserState
from db.links import get_owner_by_link
from db.anon_chat import (
    set_anon_session,
    get_owner_for_anon,
)
from db.users import set_state


def register_anon_chat_handlers(application):
    application.add_handler(CommandHandler("start", start_with_link))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, anon_chat_message)
    )


# ─────────────────────────────────────
# /start с параметром ссылки
# ─────────────────────────────────────
async def start_with_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    # обычный /start — не тут
    if not args:
        return

    link_id = args[0]
    owner_id = get_owner_by_link(link_id)

    if not owner_id:
        await update.message.reply_text(
            "❌ Ссылка недействительна или устарела.",
            reply_markup=get_main_menu()
        )
        return

    if owner_id == user_id:
        await update.message.reply_text(
            "❌ Это ваша собственная ссылка.",
            reply_markup=get_main_menu()
        )
        return

    # сохраняем сессию
    set_anon_session(from_user=user_id, owner_id=owner_id)
    set_state(user_id, UserState.ANON_CHAT)

    await update.message.reply_text(
        "✅ <b>Анонимный чат начат</b>\n\n"
        "💬 Напишите сообщение — оно будет отправлено анонимно.",
        parse_mode="HTML"
    )

    await context.bot.send_message(
        owner_id,
        "📨 <b>Новое анонимное сообщение</b>\n"
        "Ожидаю текст…",
        parse_mode="HTML"
    )


# ─────────────────────────────────────
# Сообщения от анонима
# ─────────────────────────────────────
async def anon_chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    owner_id = get_owner_for_anon(user_id)
    if not owner_id:
        return

    await context.bot.send_message(
        owner_id,
        f"👤 <b>Аноним:</b>\n\n{text}",
        parse_mode="HTML"
    )

    await update.message.reply_text("✅ Сообщение отправлено")
