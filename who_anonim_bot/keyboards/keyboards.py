from telegram import ReplyKeyboardMarkup, KeyboardButton

# === Главное меню ===
def main_menu_keyboard(is_admin=False):
    buttons = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]

    if is_admin:
        buttons.append([KeyboardButton("⚙️ Админ-панель")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# === Выбор пола для рулетки ===
def gender_select_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )


# === Кнопки во время поиска собеседника ===
def roulette_search_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("❌ Отмена")],
            [KeyboardButton("⚠ Пожаловаться")],
            [KeyboardButton("⬅️ Назад")],
        ],
        resize_keyboard=True
    )


# === Кнопки когда собеседник найден ===
def roulette_chat_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("⏭ След. собеседник"), KeyboardButton("⛔ Стоп")],
            [KeyboardButton("⚠ Пожаловаться")],
            [KeyboardButton("⬅️ Назад")],
        ],
        resize_keyboard=True
    )


# === Меню анонимной ссылки ===
def anon_link_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🔄 Сменить ссылку")],
            [KeyboardButton("⬅️ Назад")],
        ],
        resize_keyboard=True
    )
