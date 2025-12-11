from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# === Главное меню ===
def get_main_menu():
    keyboard = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Меню анонимной ссылки ===
def get_anon_link_menu():
    keyboard = [
        [KeyboardButton("🔄 Сменить ссылку")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Inline-кнопки для анонимных сообщений ===
def get_anon_reply_buttons(session_id):
    keyboard = [
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{session_id}"),
            InlineKeyboardButton("⚠️ Пожаловаться", callback_data=f"report:{session_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# === Меню рулетки (поиск собеседника) ===
def get_search_cancel():
    keyboard = [
        [KeyboardButton("❌ Отменить"), KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Меню при найденном собеседнике ===
def get_roulette_menu():
    keyboard = [
        [KeyboardButton("⏭ След. собеседник")],
        [KeyboardButton("⛔ Стоп")],
        [KeyboardButton("⚠️ Пожаловаться")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Выбор пола ===
def get_gender_menu():
    keyboard = [
        [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Админ панель ===
def get_admin_menu():
    keyboard = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("👥 Пользователи")],
        [KeyboardButton("⚠️ Жалобы"), KeyboardButton("🗑 Очистить жалобы")],
        [KeyboardButton("📢 Рассылка"), KeyboardButton("🔗 Все ссылки")],
        [KeyboardButton("🚫 Забанить"), KeyboardButton("✅ Разбанить")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# === Кнопка Отмена ===
def get_cancel_keyboard():
    keyboard = [[KeyboardButton("❌ Отменить")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
