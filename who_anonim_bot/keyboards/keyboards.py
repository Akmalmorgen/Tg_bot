from telegram import ReplyKeyboardMarkup


def get_main_menu(is_admin: bool = False):
    keyboard = [
        ["🔗 Моя анон-ссылка"],
        ["🎲 Рулетка"],
        ["💬 Помощь"],
    ]

    if is_admin:
        keyboard.append(["⚙️ Админ-панель"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
