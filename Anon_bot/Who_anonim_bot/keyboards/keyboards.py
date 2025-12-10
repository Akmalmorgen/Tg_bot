from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["🔗 Моя анон-ссылка"],
            ["🎲 Рулетка"],
            ["💬 Помощь"]
        ],
        resize_keyboard=True
    )

def admin_menu():
    return ReplyKeyboardMarkup(
        [
            ["📊 Статистика", "👥 Пользователи"],
            ["⚠️ Жалобы", "🗑 Очистить жалобы"],
            ["📢 Рассылка", "🔗 Все ссылки"],
            ["🚫 Забанить", "✅ Разбанить"],
            ["🧽 Удалить неактивные ссылки (7 дней)"],
            ["⬅️ Назад"]
        ],
        resize_keyboard=True
    )

def link_manage_menu():
    return ReplyKeyboardMarkup(
        [
            ["🔄 Сменить ссылку"],
            ["⬅️ Назад"]
        ],
        resize_keyboard=True
    )

def roulette_gender_menu():
    return ReplyKeyboardMarkup(
        [
            ["👨 Мужчина", "👩 Женщина"],
            ["⬅️ Назад"]
        ],
        resize_keyboard=True
    )

def roulette_chat_menu():
    return ReplyKeyboardMarkup(
        [
            ["⏭ След. собеседника"],
            ["⛔ Стоп"],
            ["⚠ Пожаловаться"],
            ["⬅️ Назад"]
        ],
        resize_keyboard=True
    )

def roulette_search_menu():
    return ReplyKeyboardMarkup(
        [
            ["❌ Отмена"],
            ["⚠ Пожаловаться"],
            ["⬅️ Назад"]
        ],
        resize_keyboard=True
    )

def link_message_inline(session_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{session_id}"),
                InlineKeyboardButton("⚠ Пожаловаться", callback_data=f"report:{session_id}")
            ]
        ]
    )

def link_report_reasons(session_id):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔘 Мат", callback_data=f"r1:{session_id}")],
            [InlineKeyboardButton("🔘 Спам", callback_data=f"r2:{session_id}")],
            [InlineKeyboardButton("🔘 18+", callback_data=f"r3:{session_id}")],
            [InlineKeyboardButton("🔘 Угроза", callback_data=f"r4:{session_id}")]
        ]
          )
