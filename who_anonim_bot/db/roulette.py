# Очереди поиска
queue_male: list[int] = []
queue_female: list[int] = []
queue_any: list[int] = []

# Активные чаты: user_id -> partner_id
active_chats: dict[int, int] = {}


def add_to_queue(user_id: int, gender: str):
    """
    Добавить пользователя в очередь поиска
    gender: M / F / ANY
    """
    remove_from_queues(user_id)

    if gender == "M":
        queue_male.append(user_id)
    elif gender == "F":
        queue_female.append(user_id)
    else:
        queue_any.append(user_id)


def remove_from_queues(user_id: int):
    """Удалить пользователя из всех очередей"""
    for q in (queue_male, queue_female, queue_any):
        if user_id in q:
            q.remove(user_id)


def try_match(user_id: int, gender: str) -> int | None:
    """
    Пытается найти собеседника.
    Возвращает partner_id или None
    """
    if gender == "M":
        targets = queue_female + queue_any
    elif gender == "F":
        targets = queue_male + queue_any
    else:
        targets = queue_male + queue_female + queue_any

    for partner_id in targets:
        if partner_id != user_id:
            _connect_users(user_id, partner_id)
            return partner_id

    return None


def _connect_users(user1: int, user2: int):
    """Создаёт активный чат"""
    remove_from_queues(user1)
    remove_from_queues(user2)

    active_chats[user1] = user2
    active_chats[user2] = user1


def get_partner(user_id: int) -> int | None:
    """Получить собеседника"""
    return active_chats.get(user_id)


def stop_chat(user_id: int) -> int | None:
    """
    Завершить чат.
    Возвращает ID собеседника
    """
    partner = active_chats.pop(user_id, None)
    if partner:
        active_chats.pop(partner, None)
    return partner
