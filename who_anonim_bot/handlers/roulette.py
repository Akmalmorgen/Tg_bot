# who_anonim_bot/handlers/roulette.py

from telegram.ext import MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

from db.users import get_user_state, set_user_state
from db.roulette import (
    add_to_queue,
    remove_from_queue,
    find_partner_for,
    set_active_pair,
    get_partner,
    clear_session
)
from states.states import (
    CHOOSING_GENDER,
    SEARCHING_ROULETTE,
    IN_ROULETTE,
    MAIN_MENU
)

# -----------------------
# К Е Й Б О Р Д Ы
# -----------------------

def gender_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def search_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("❌ Отмена")],
            [KeyboardButton("⚠️ Пожаловаться"), KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def chat_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("⏭ След"), KeyboardButton("⛔ Стоп")],
            [KeyboardButton("⚠️ Пожаловаться")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def fast_search_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("👨 Поиск М"), KeyboardButton("👩 Поиск Ж")],
            [KeyboardButton("🎲 Поиск любой")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )


# -----------------------
# Н А Ч А Л О   Р У Л Е Т К И
# -----------------------

async def start_roulette(update, context):
    uid = update.effective_user.id
    await set_user_state(uid, CHOOSING_GENDER)

    await update.message.reply_text(
        "🎲 Выберите ваш пол для поиска:",
        reply_markup=gender_keyboard()
    )


# -----------------------
# В Ы Б О Р   П О Л А
# -----------------------

async def choose_gender(update, context):
    uid = update.effective_user.id
    txt = update.message.text

    if txt == "👨 Мужчина":
        gender = "M"
    elif txt == "👩 Женщина":
        gender = "F"
    else:
        return

    # добавляем в очередь
    await add_to_queue(uid, gender)
    await set_user_state(uid, SEARCHING_ROULETTE)

    await update.message.reply_text(
        "🔍 Поиск собеседника...",
        reply_markup=search_keyboard()
    )

    # пробуем найти пару
    partner = await find_partner_for(uid, gender)

    if partner:
        # создаём пару
        await set_active_pair(uid, partner)
        await set_active_pair(partner, uid)

        await set_user_state(uid, IN_ROULETTE)
        await set_user_state(partner, IN_ROULETTE)

        await remove_from_queue(uid)
        await remove_from_queue(partner)

        # отправляем обоим
        await update.message.reply_text(
            "✅ Собеседник найден!",
            reply_markup=chat_keyboard()
        )

        await context.bot.send_message(
            partner,
            "✅ Собеседник найден!",
            reply_markup=chat_keyboard()
        )


# -----------------------
# С О О Б Щ Е Н И Я  В  Ч А Т Е
# -----------------------

async def roulette_message(update, context):
    uid = update.effective_user.id

    partner = await get_partner(uid)
    if not partner:
        await update.message.reply_text("❌ Собеседник не найден.")
        return

    try:
        await context.bot.send_message(
            partner,
            f"💬 Сообщение: {update.message.text}"
        )
    except:
        pass


# -----------------------
# С Л Е Д У Ю Щ И Й
# -----------------------

async def next_partner(update, context):
    uid = update.effective_user.id

    partner = await get_partner(uid)
    if partner:
        await clear_session(uid)
        await clear_session(partner)

        await context.bot.send_message(partner, "👋 Собеседник завершил чат.")

    await set_user_state(uid, CHOOSING_GENDER)

    await update.message.reply_text(
        "Выберите пол для нового поиска:",
        reply_markup=gender_keyboard()
    )


# -----------------------
# С Т О П
# -----------------------

async def stop_chat(update, context):
    uid = update.effective_user.id
    partner = await get_partner(uid)

    if partner:
        await clear_session(uid)
        await clear_session(partner)
        await context.bot.send_message(partner, "👋 Чат завершён.")

    await set_user_state(uid, MAIN_MENU)

    # Показываем кнопки быстрого поиска
    await update.message.reply_text(
        "Чат завершён. Хотите начать новый?",
        reply_markup=fast_search_keyboard()
    )


# -----------------------
# П О М О Щ Ь / Ж А Л О Б А
# -----------------------

async def roulette_complaint(update, context):
    uid = update.effective_user.id
    partner = await get_partner(uid)

    if not partner:
        await update.message.reply_text("❌ Некому отправить жалобу.")
        return

    # Запись жалобы
    from db.complaints import add_complaint

    await add_complaint(
        reporter_id=uid,
        reported_id=partner,
        offender_anon_tag="roulette",
        reason="default",
        chat_type="roulette"
    )

    await update.message.reply_text("⚠️ Жалоба отправлена.")


# -----------------------
# Р Е Г И С Т Р А Т О Р
# -----------------------

def register_roulette_handlers(app):

    # запуск рулетки из главного меню
    app.add_handler(MessageHandler(filters.Regex("^🎲 Рулетка$"), start_roulette))

    # выбор пола
    app.add_handler(MessageHandler(filters.Regex("^👨 Мужчина$|^👩 Женщина$"), choose_gender))

    # поиск — отмена
    app.add_handler(MessageHandler(filters.Regex("^❌ Отмена$"), stop_chat))

    # найденный чат: след
    app.add_handler(MessageHandler(filters.Regex("^⏭ След$"), next_partner))

    # найденный чат: стоп
    app.add_handler(MessageHandler(filters.Regex("^⛔ Стоп$"), stop_chat))

    # жалоба
    app.add_handler(MessageHandler(filters.Regex("^⚠️ Пожаловаться$"), roulette_complaint))

    # сообщения в рулетке
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roulette_message))
