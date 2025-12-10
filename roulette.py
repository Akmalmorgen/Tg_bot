import random

# Очереди пользователей по полу
roulette_queue = {
    "M": [],
    "F": [],
    "ANY": []
}

# Активные чаты
active_chats = {}  # user_id : partner_id

# Пол пользователей
user_gender = {}   # user_id : M/F


def set_gender(user_id: int, gender: str):
    """Устанавливаем пол пользователя"""
    user_gender[user_id] = gender


def add_to_queue(user_id: int, gender: str):
    """Добавляет пользователя в очередь"""
    if gender == "ANY":
        roulette_queue["ANY"].append(user_id)
    else:
        roulette_queue[gender].append(user_id)


def remove_from_queue(user_id: int):
    """Удаляет из очереди"""
    for g in roulette_queue:
        if user_id in roulette_queue[g]:
            roulette_queue[g].remove(user_id)


def find_partner(gender: str):
    """Ищет подходящего собеседника"""
    if gender == "M":
        groups = ["F", "ANY"]
    elif gender == "F":
        groups = ["M", "ANY"]
    else:
        groups = ["M", "F", "ANY"]

    for g in groups:
        if roulette_queue[g]:
            return roulette_queue[g].pop(0)

    return None


def start_chat(user1: int, user2: int):
    """Создаёт активный чат"""
    active_chats[user1] = user2
    active_chats[user2] = user1


def stop_chat(user_id: int):
    """Останавливает чат"""
    if user_id in active_chats:
        partner = active_chats[user_id]
        del active_chats[user_id]

        if partner in active_chats:
            del active_chats[partner]

        return partner
    return None
