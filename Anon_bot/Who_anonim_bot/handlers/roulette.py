from telegram.ext import MessageHandler, filters
from keyboards.keyboards import (
    roulette_gender_menu,
    roulette_search_menu,
    roulette_chat_menu,
    main_menu
)
from db.roulette import (
    set_gender,
    find_partner,
    set_busy,
    clear_partner,
    get_partner
)
from states.states import (
    ROULETTE_CHOOSE_GENDER,
    ROULETTE_SEARCHING,
    ROULETTE_CHAT
)


# --- 1. Запуск рулетки из меню ---
async def start_roulette(update, context):
    user_id = update.effective_user.id

    await update.message.reply_text(
        "🎲 <b>Рулетка!</b>\n\nВыберите ваш пол:",
        parse_mode="HTML",
        reply_markup=roulette_gender_menu()
    )

    context.user_data["state"] = ROULETTE_CHOOSE_GENDER
    return ROULETTE_CHOOSE_GENDER


# --- 2. Выбор пола ---
async def choose_gender(update, context):
    user_id = update.effective_user.id
    text = update.message.text

    if text not in ["👨 Мужчина", "👩 Женщина"]:
        return

    gender = "m" if text == "👨 Мужчина" else "f"
    await set_gender(user_id, gender)

    await update.message.reply_text(
        "🔍 Ищу собеседника...",
        reply_markup=roulette_search_menu()
    )

    context.user_data["state"] = ROULETTE_SEARCHING

    # ПОИСК ПАРТНЁРА
    partner = await find_partner(user_id)

    if partner:
        # если найден — связываем
        await set_busy(user_id, partner)
        await set_busy(partner, user_id)

        await update.message.reply_text(
            "✅ Собеседник найден!",
            reply_markup=roulette_chat_menu()
        )

        await context.bot.send_message(
            partner,
            "🎯 Вы подключены к новому собеседнику!",
            reply_markup=roulette_chat_menu()
        )

        context.user_data["state"] = ROULETTE_CHAT
        return ROULETTE_CHAT

    return ROULETTE_SEARCHING


# --- 3. Отмена поиска ---
async def cancel_search(update, context):
    user_id = update.effective_user.id

    await update.message.reply_text(
        "❌ Поиск остановлен.\nВыберите новый тип поиска:",
        reply_markup=roulette_gender_menu()
    )

    context.user_data["state"] = ROULETTE_CHOOSE_GENDER
    return ROULETTE_CHOOSE_GENDER


# --- 4. Сообщения в чате рулетки ---
async def roulette_chat(update, context):
    user_id = update.effective_user.id
    partner = await get_partner(user_id)

    if not partner:
        await update.message.reply_text(
            "😕 Ваш собеседник покинул чат.",
            reply_markup=roulette_gender_menu()
        )
        context.user_data["state"] = ROULETTE_CHOOSE_GENDER
        return ROULETTE_CHOOSE_GENDER

    # пересылаем текст/медиа
    if update.message.text:
        await context.bot.send_message(partner, update.message.text)
    else:
        try:
            await update.message.copy_to(partner)
        except:
            pass


# --- 5. Следующий собеседник ---
async def next_partner(update, context):
    user_id = update.effective_user.id
    partner = await get_partner(user_id)

    if partner:
        await context.bot.send_message(partner, "⛔ Собеседник вышел.")
        await clear_partner(partner)

    await clear_partner(user_id)

    await update.message.reply_text(
        "🔄 Ищу нового собеседника…",
        reply_markup=roulette_search_menu()
    )

    context.user_data["state"] = ROULETTE_SEARCHING

    # ищем нового
    new = await find_partner(user_id)

    if new:
        await set_busy(user_id, new)
        await set_busy(new, user_id)

        await update.message.reply_text(
            "🎯 Новый собеседник найден!",
            reply_markup=roulette_chat_menu()
        )

        await context.bot.send_message(
            new,
            "🎯 Вас подключили к новому собеседнику!",
            reply_markup=roulette_chat_menu()
        )

        context.user_data["state"] = ROULETTE_CHAT
        return ROULETTE_CHAT

    return ROULETTE_SEARCHING


# --- 6. Стоп / Выход из чата ---
async def stop_chat(update, context):
    user_id = update.effective_user.id
    partner = await get_partner(user_id)

    if partner:
        await context.bot.send_message(partner, "⛔ Собеседник завершил чат.")
        await clear_partner(partner)

    await clear_partner(user_id)

    await update.message.reply_text(
        "⛔ Чат завершён.\nВыберите поиск:",
        reply_markup=roulette_gender_menu()
    )

    context.user_data["state"] = ROULETTE_CHOOSE_GENDER
    return ROULETTE_CHOOSE_GENDER


# --- 7. Жалоба ---
async def roulette_report(update, context):
    await update.message.reply_text(
        "⚠ Жалоба отправлена!",
        reply_markup=roulette_chat_menu()
    )


# --- РЕГИСТРАЦИЯ ХЕНДЛЕРОВ ---
def register_roulette_handlers(app):

    app.add_handler(
        MessageHandler(
            filters.Regex("^👨 Мужчина$|^👩 Женщина$"),
            choose_gender
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^❌ Отмена$"),
            cancel_search
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^⏭ След. собеседника$"),
            next_partner
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^⛔ Стоп$"),
            stop_chat
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("^⚠ Пожаловаться$"),
            roulette_report
        )
    )

    # Основной чат рулетки — ловим ВСЕ сообщения
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            roulette_chat
        )
  )
