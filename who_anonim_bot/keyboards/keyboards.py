from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard(is_admin=False):
    buttons = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]

    if is_admin:
        buttons.append([KeyboardButton("⚙️ Админ-панель")])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
