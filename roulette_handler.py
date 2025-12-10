from telegram import Update
from telegram.ext import ContextTypes

from keyboards import roulette_gender_keyboard, roulette_wait_keyboard, roulette_chat_keyboard, main_menu
from roulette import (
    set_gender, add_to_queue, remove_from_queue,
    find_partner, start_chat, stop_chat,
    active_chats, user_gender
)
from complaints import add_complaint


async def start_gender_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Шаг 1 — выбор пола"""
    await update.message.reply_text(
        "🎲 <b>РУЛЕТКА</b>\n\nВыберите ваш пол:",
        parse_mode="HTML",
        reply_markup=roulette_gender_keyboard()
    )


async def pick_gender(update: Update, context: ContextTypes.DEFAULT_TYPE, gender: str):
    """Установка пола и начало поиска"""
    user_id = update.effective_user.id
    set_gender(user_id, gender)

    # Ищем собеседника
    partner = find_partner(gender)

    if partner is None:
        # Добавляем в очередь ожидания
        add_to_queue(user_id, gender)

        await update.message.reply_text(
            "🔍 <b>Поиск собеседника...</b>",
            parse_mode="HTML",
            reply_markup=roulette_wait_keyboard()
        )
        return

    # Если нашли — запускаем чат
    start_chat(user_id, partner)

    await update.message.reply_text(
        "✅ Собеседник найден! Можете писать.",
        reply_markup=roulette_chat_keyboard()
    )

    await context.bot.send_message(
        partner,
        "✅ Собеседник найден! Можете писать.",
        reply_markup=roulette_chat_keyboard()
    )


async def cancel_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена поиска"""
    user_id = update.effective_user.id
    remove_from_queue(user_id)

    await update.message.reply_text(
        "❌ Поиск отменён.",
        reply_markup=main_menu()
    )


async def handle_roulette_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылка сообщений между собеседниками"""
    user_id = update.effective_user.id

    if user_id not in active_chats:
        return

    partner = active_chats[user_id]

    await context.bot.send_message(
        partner,
        f"💬 Собеседник:\n{update.message.text}"
    )


async def next_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """⏭ Следующий собеседник"""

    user_id = update.effective_user.id

    # Завершаем текущий чат
    partner = stop_chat(user_id)
    if partner:
        await context.bot.send_message(
            partner,
            "👋 Собеседник покинул чат.",
            reply_markup=main_menu()
        )

    gender = user_gender.get(user_id, "ANY")
    await pick_gender(update, context, gender)


async def stop_chat_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """⛔ Стоп"""
    user_id = update.effective_user.id

    partner = stop_chat(user_id)

    if partner:
        await context.bot.send_message(
            partner,
            "👋 Собеседник завершил чат.",
            reply_markup=main_menu()
        )

    await update.message.reply_text(
        "Чат завершён.",
        reply_markup=main_menu()
    )


async def report_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """⚠ Пожаловаться"""

    user_id = update.effective_user.id

    if user_id not in active_chats:
        return

    partner = active_chats[user_id]

    add_complaint(user_id, partner, "roulette")

    await update.message.reply_text("⚠ Жалоба отправлена.")
