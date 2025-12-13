from enum import Enum, auto


class UserState(Enum):
    MAIN_MENU = auto()

    # 🔗 Анонимная ссылка
    MY_ANON_LINK = auto()
    CHANGE_LINK = auto()

    # 👻 Анонимное общение по ссылке
    ANON_CHAT = auto()

    # 🎲 Рулетка
    ROULETTE_GENDER = auto()
    ROULETTE_SEARCH = auto()
    ROULETTE_CHAT = auto()

    # ⚙️ Админ
    ADMIN_PANEL = auto()
    ADMIN_BROADCAST = auto()
    ADMIN_BAN = auto()
    ADMIN_UNBAN = auto()
