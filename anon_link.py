import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from keyboards import anon_link_menu, main_menu
from links import get_or_create_link, regenerate_link
from anon_chat_handler import active_anon_chats
from users import add_user


async def show_my_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать пользователю его анонимную ссылку"""
    user_id = update.effective_user.id
    await add_user(user_id)

    link_id = await get_or_create_link(user_id)
    link = f"https://t.me/{context.bot.username}?start={link_id}"

    # сколько людей в анонимном чате сейчас
    active_count = sum(1 for uid, owner in active_anon_chats.items() if owner == user_id)

    text = (
        "🔗 <b>Ваша анонимная ссылка</b>\n\n"
        f"<code>{link}</code>\n"
        f"ID: <code>{link_id}</code>\n\n"
        f"👥 Активных анонимных собеседников: <b>{active_count}</b>\n\n"
        "Вы можете сменить ссылку, но все текущие анонимные чаты будут завершены."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=anon_link_menu()
    )


async def change_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Смена ссылки пользователя"""
    user_id = update.effective_user.id

    new_link = await regenerate_link(user_id)

    link = f"https://t.me/{context.bot.username}?start={new_link}"

    text = (
        "🔄 <b>Ссылка успешно изменена!</b>\n\n"
        f"Новая ссылка:\n<code>{link}</code>\n\n"
        "Старая ссылка теперь недействительна."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=anon_link_menu()
    )
