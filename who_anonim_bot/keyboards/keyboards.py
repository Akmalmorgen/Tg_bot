from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ─────────────────────────
# Главное меню
# ─────────────────────────
def main_menu_keyboard(is_admin: bool = False):
    keyboard = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]

    if is_admin:
        keyboard.append([KeyboardButton("⚙️ Админ-панель")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# ─────────────────────────
# Моя анонимная ссылка
# ─────────────────────────
def anon_link_keyboard():
    keyboard = [
        [KeyboardButton("🔄 Сменить ссылку")],
        [KeyboardButton("⬅️ Назад")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# ─────────────────────────
# Выбор пола (рулетка)
# ─────────────────────────
def gender_keyboard():
    keyboard = [
        [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
        [KeyboardButton("⬅️ Назад")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# ─────────────────────────
# Поиск собеседника
# ─────────────────────────
def roulette_search_keyboard():
    keyboard = [
        [KeyboardButton("❌ Отмена")],
        [KeyboardButton("⬅️ Назад")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# ─────────────────────────
# Рулетка — чат
# ─────────────────────────
def roulette_chat_keyboard():
    keyboard = [
        [KeyboardButton("⏭ След. собеседник")],
        [KeyboardButton("⏹ Стоп")],
        [KeyboardButton("⚠️ Пожаловаться")],
        [KeyboardButton("⬅️ Назад")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# ─────────────────────────
# Админ-панель
# ─────────────────────────
def admin_panel_keyboard():
    keyboard = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("👥 Пользователи")],
        [KeyboardButton("⚠️ Жалобы"), KeyboardButton("🗑 Очистить жалобы")],
        [KeyboardButton("📢 Рассылка"), KeyboardButton("🔗 Все ссылки")],
        [KeyboardButton("🚫 Забанить"), KeyboardButton("✅ Разбанить")],
        [KeyboardButton("⬅️ Назад")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


# ─────────────────────────
# Inline — Анонимное сообщение по ссылке
# (ТОЛЬКО ЗДЕСЬ inline)
# ─────────────────────────
def anon_message_inline(session_id: str):
    keyboard = [
        [
            InlineKeyboardButton(
                text="💬 Ответить",
                callback_data=f"reply:{session_id}"
            ),
            InlineKeyboardButton(
                text="⚠️ Пожаловаться",
                callback_data=f"report:{session_id}"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
