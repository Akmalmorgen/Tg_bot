# who_anonim_bot/keyboards/keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard(is_admin: bool=False):
    kb = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")],
    ]
    if is_admin:
        kb.append([KeyboardButton("⚙️ Админ-панель")])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def anon_link_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🔄 Сменить ссылку"), KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def anon_owner_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🔎 Показать подключённых")],
            [KeyboardButton("🔄 Сменить ссылку"), KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def roulette_gender_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def roulette_search_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("❌ Отмена")],
            [KeyboardButton("⚠️ Пожаловаться"), KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def roulette_chat_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("⏭ След. собеседник"), KeyboardButton("🔎 След. поиск")],
            [KeyboardButton("⏹ Стоп"), KeyboardButton("⚠️ Пожаловаться")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

# inline for link-mode messages (owner sees these under every anon message)
def owner_inline_buttons(session_id: str):
    kb = [
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{session_id}"),
            InlineKeyboardButton("⚠️ Пожаловаться", callback_data=f"report:{session_id}")
        ]
    ]
    return InlineKeyboardMarkup(kb)

def report_reason_keyboard(session_id: str):
    kb = [
        [
            InlineKeyboardButton("🧨 Мат", callback_data=f"report_reason:{session_id}:mat"),
            InlineKeyboardButton("📨 Спам", callback_data=f"report_reason:{session_id}:spam"),
        ],
        [
            InlineKeyboardButton("🔞 18+", callback_data=f"report_reason:{session_id}:18plus"),
            InlineKeyboardButton("⚡ Угроза", callback_data=f"report_reason:{session_id}:threat"),
        ],
        [InlineKeyboardButton("🔙 Отмена", callback_data=f"report_cancel:{session_id}")]
    ]
    return InlineKeyboardMarkup(kb)
