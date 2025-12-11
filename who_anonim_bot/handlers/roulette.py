from telegram import Update
from telegram.ext import ContextTypes

from db.roulette import (
    set_gender,
    get_gender,
    add_to_queue,
    pop_from_queue,
    link_users,
    unlink_users,
    get_partner,
)

from db.users import set_state
from db.complaints import add_complaint

from states.states import (
    ROULETTE_GENDER,
    ROULETTE_SEARCH,
    ROULETTE_CHAT,
    MAIN_MENU
)

from keyboards.keyboards import (
    gender_select_kb,
    roulette_search_kb,
    roulette_chat_kb,
    main_menu_kb
)

from logger.logger import get_logger
logger = get_logger()


# =====================================================
# 🔹 Старт рулетки
# =====================================================
async def start_roulette_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await set_state(user_id, ROULETTE_GENDER)

    await update.message.reply_text(
        "🎲 <b>Выберите ваш пол:</b>",
        parse_mode="HTML",
        reply_markup=gender_select_kb()
    )


# =====================================================
# 🔹 Выбор пола
# =====================================================
async def choose_gender(update: Update, context: ContextTypes.DEFAULT_TYPE, gender: str):
    user_id = update.effective_user.id

    await set_gender(user_id, gender)
    await set_state(user_id, ROULETTE_SEARCH)

    # пытаемся найти собеседника противоположного пола
    partner_id = await pop_from_queue("F" if gender == "M" else "M")

    if partner_id:
        # соединяем
        await link_users(user_id, partner_id)
        await set_state(user_id, ROULETTE_CHAT)
        await set_state(partner_id, ROULETTE_CHAT)

        # сообщаем двоим
        await update.message.reply_text(
            "🔗 <b>Собеседник найден!</b>\nНачните переписку 👇",
            parse_mode="HTML",
            reply_markup=roulette_chat_kb()
        )

        await context.bot.send_message(
            partner_id,
            "🔗 <b>Собеседник найден!</b>\nНачните переписку 👇",
            parse_mode="HTML",
            reply_markup=roulette_chat_kb()
        )
        return

    # если нет собеседника — ставим в очередь
    await add_to_queue(user_id, gender)

    await update.message.reply_text(
        "⏳ <b>Поиск собеседника...</b>",
        parse_mode="HTML",
        reply_markup=roulette_search_kb()
    )


# =====================================================
# 🔹 Отмена поиска
# =====================================================
async def cancel_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await unlink_users(user_id)
    await set_state(user_id, MAIN_MENU)

    await update.message.reply_text(
        "❌ Поиск отменён.",
        reply_markup=main_menu_kb()
    )


# =====================================================
# 🔹 Сообщения в рулетке
# =====================================================
async def roulette_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    partner_id = await get_partner(user_id)

    if not partner_id:
        await update.message.reply_text(
            "❌ Собеседник отключился.",
            reply_markup=main_menu_kb()
        )
        await set_state(user_id, MAIN_MENU)
        return

    await context.bot.send_message(
        partner_id,
        f"💬 {text}"
    )


# =====================================================
# 🔹 Следующий собеседник
# =====================================================
async def next_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    gender = await get_gender(user_id)

    # отключаем текущего
    partner_id = await get_partner(user_id)

    if partner_id:
        await unlink_users(user_id)
        await unlink_users(partner_id)

        await context.bot.send_message(
            partner_id,
            "👋 Собеседник вышел.",
            reply_markup=main_menu_kb()
        )
        await set_state(partner_id, MAIN_MENU)

    # ищем нового
    await choose_gender(update, context, gender)


# =====================================================
# 🔹 Стоп — завершить чат
# =====================================================
async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner_id = await get_partner(user_id)

    if partner_id:
        await unlink_users(user_id)
        await unlink_users(partner_id)

        await context.bot.send_message(
            partner_id,
            "👋 Собеседник завершил чат.",
            reply_markup=main_menu_kb()
        )
        await set_state(partner_id, MAIN_MENU)

    await update.message.reply_text(
        "Чат завершён.",
        reply_markup=main_menu_kb()
    )

    await set_state(user_id, MAIN_MENU)


# =====================================================
# 🔹 Пожаловаться
# =====================================================
async def roulette_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner_id = await get_partner(user_id)

    if not partner_id:
        await update.message.reply_text("❌ Собеседника нет.")
        return

    await add_complaint(reporter=user_id, reported=partner_id, reason="roulette")

    await update.message.reply_text("⚠️ Жалоба отправлена.")
