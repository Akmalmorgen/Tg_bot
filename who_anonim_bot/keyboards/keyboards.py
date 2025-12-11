from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ===============================
# 🔹 Главное меню
# ===============================
def main_menu(is_admin: bool = False):
    kb = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]

    if is_admin:
        kb.append([KeyboardButton("⚙️ Админ-панель")])

    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


# ===============================
# 🔹 Моя анонимная ссылка
# ===============================
def my_link_menu():
    kb = [
        [KeyboardButton("🔄 Сменить ссылку")],
        [KeyboardButton("⬅️ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


# ===============================
# 🔹 Inline кнопки в анонимном чате
#   (только для владельца ссылки!)
# ===============================
def anon_owner_inline_buttons(session_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{session_id}"),
            InlineKeyboardButton("⚠️ Пожаловаться", callback_data=f"report:{session_id}")
        ]
    ])


# ===============================
# 🔹 Жалоба на анонима — выбор причины
# ===============================
def report_reason_keyboard(session_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🧨 Мат", callback_data=f"reason:{session_id}:mat"),
            InlineKeyboardButton("📨 Спам", callback_data=f"reason:{session_id}:spam"),
        ],
        [
            InlineKeyboardButton("🔞 18+", callback_data=f"reason:{session_id}:18"),
            InlineKeyboardButton("⚡ Угроза", callback_data=f"reason:{session_id}:threat"),
        ],
        [InlineKeyboardButton("❌ Отмена", callback_data="cancel_report")]
    ])


# ===============================
# 🔹 Рулетка — выбор пола
# ===============================
def gender_keyboard():
    kb = [
        [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
        [KeyboardButton("⬅️ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


# ===============================
# 🔹 Поиск собеседника (в очереди)
# ===============================
def roulette_search_keyboard():
    kb = [
        [KeyboardButton("❌ Отмена"), KeyboardButton("⬅️ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


# ===============================
# 🔹 Рулетка — активный чат
# ===============================
def roulette_chat_keyboard():
    kb = [
        [KeyboardButton("⏭ След. собеседник")],
        [KeyboardButton("⛔ Стоп"), KeyboardButton("⚠️ Пожаловаться")],
        [KeyboardButton("⬅️ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)


# ===============================
# 🔹 Админ-панель
# ===============================
def admin_menu_keyboard():
    kb = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("👥 Пользователи")],
        [KeyboardButton("⚠️ Жалобы"), KeyboardButton("🗑 Очистить жалобы")],
        [KeyboardButton("📢 Рассылка"), KeyboardButton("🔗 Все ссылки")],
        [KeyboardButton("🚫 Забанить"), KeyboardButton("✅ Разбанить")],
        [KeyboardButton("⬅️ Назад в меню")]
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)
