from .database import get_db


# ========================================
# 🔹 СОЗДАНИЕ / ОБНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
# ========================================
async def add_user(user_id: int, username: str = None):
    """Создаёт пользователя, если его ещё нет"""
    db = await get_db()
    await db.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (user_id, username)
    )
    await db.commit()
    await db.close()


async def update_username(user_id: int, username: str):
    """Обновляет username"""
    db = await get_db()
    await db.execute(
        "UPDATE users SET username = ? WHERE user_id = ?",
        (username, user_id)
    )
    await db.commit()
    await db.close()


# ========================================
# 🔹 СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЯ
# ========================================
async def set_state(user_id: int, state: str):
    """Сохранить новое состояние"""
    db = await get_db()
    await db.execute(
        "UPDATE users SET state = ? WHERE user_id = ?",
        (state, user_id)
    )
    await db.commit()
    await db.close()


async def get_state(user_id: int):
    """Получить состояние"""
    db = await get_db()
    cursor = await db.execute(
        "SELECT state FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()
    return row[0] if row else None


# ========================================
# 🔹 БАН / РАЗБАН
# ========================================
async def is_banned(user_id: int) -> bool:
    """Проверка — забанен ли пользователь"""
    db = await get_db()
    cursor = await db.execute(
        "SELECT banned FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()
    return bool(row[0]) if row else False


async def ban_user(user_id: int):
    """Забанить"""
    db = await get_db()
    await db.execute(
        "UPDATE users SET banned = 1 WHERE user_id = ?",
        (user_id,)
    )
    await db.commit()
    await db.close()


async def unban_user(user_id: int):
    """Разбанить"""
    db = await get_db()
    await db.execute(
        "UPDATE users SET banned = 0 WHERE user_id = ?",
        (user_id,)
    )
    await db.commit()
    await db.close()
