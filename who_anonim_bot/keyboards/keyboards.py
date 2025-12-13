from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ─────────────────────
# 🔹 Главное меню
# ─────────────────────
def main_menu_keyboard(is_admin: bool = False):
    keyboard = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]

    if is_admin:
        keyboard.append([KeyboardButton("⚙️ Админ-панель")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# 🔗 Моя анонимная ссылка
# ─────────────────────
def anon_link_keyboard():
    keyboard = [
        [KeyboardButton("🔄 Сменить ссылку")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# 🎲 Выбор пола (рулетка)
# ─────────────────────
def roulette_gender_keyboard():
    keyboard = [
        [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
        [KeyboardButton("🔎 Любой")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# 🔍 Поиск собеседника
# ─────────────────────
def roulette_search_keyboard():
    keyboard = [
        [KeyboardButton("❌ Отмена")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# 💬 Чат в рулетке
# ─────────────────────
def roulette_chat_keyboard():
    keyboard = [
        [KeyboardButton("⏭ След. собеседник")],
        [KeyboardButton("⛔ Стоп")],
        [KeyboardButton("⚠️ Пожаловаться")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# ⚙️ Админ-панель
# ─────────────────────
def admin_panel_keyboard():
    keyboard = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("👥 Пользователи")],
        [KeyboardButton("⚠️ Жалобы"), KeyboardButton("🗑 Очистить жалобы")],
        [KeyboardButton("📢 Рассылка"), KeyboardButton("🔗 Все ссылки")],
        [KeyboardButton("🚫 Забанить"), KeyboardButton("✅ Разбанить")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# 📢 Рассылка (админ)
# ─────────────────────
def broadcast_keyboard():
    keyboard = [
        [KeyboardButton("❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ─────────────────────
# 👻 Inline — Анонимное сообщение
# ТОЛЬКО здесь inline-кнопки
# ─────────────────────
def anon_message_inline(anon_id: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="💬 Ответить",
                callback_data=f"reply:{anon_id}"
            ),
            InlineKeyboardButton(
                text="⚠️ Пожаловаться",
                callback_data=f"complaint:{anon_id}"
            )
        ]
    ])


# ─────────────────────
# 🚨 Причины жалобы (inline)
# ─────────────────────
def complaint_reasons_inline(anon_id: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔞 18+", callback_data=f"reason:18+:{anon_id}")],
        [InlineKeyboardButton("🤬 Мат", callback_data=f"reason:mat:{anon_id}")],
        [InlineKeyboardButton("📨 Спам", callback_data=f"reason:spam:{anon_id}")],
        [InlineKeyboardButton("⚠️ Угроза", callback_data=f"reason:threat:{anon_id}")]
    ])
