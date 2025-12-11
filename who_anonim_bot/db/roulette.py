from .database import get_db


# ================================
# 🔹 Сохранить пол пользователя
# M — мужчина, F — женщина
# ================================
async def set_gender(user_id: int, gender: str):
    db = await get_db()
    await db.execute(
        "UPDATE users SET gender = ? WHERE user_id = ?",
        (gender, user_id)
    )
    await db.commit()
    await db.close()


# ================================
# 🔹 Получить пол пользователя
# ================================
async def get_gender(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT gender FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ================================
# 🔹 Добавить пользователя в очередь
# ================================
async def join_queue(user_id: int, gender: str):
    db = await get_db()
    await db.execute(
        "INSERT INTO roulette_queue (user_id, gender) VALUES (?, ?)",
        (user_id, gender)
    )
    await db.commit()
    await db.close()


# ================================
# 🔹 Найти пару с противоположным полом
# ================================
async def find_partner(for_gender: str):
    db = await get_db()

    # Ищем того, кто ищет тебя
    cursor = await db.execute(
        """
        SELECT user_id 
        FROM roulette_queue 
        WHERE gender != ? 
        ORDER BY id ASC 
        LIMIT 1
        """,
        (for_gender,)
    )

    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ================================
# 🔹 Удалить из очереди
# ================================
async def leave_queue(user_id: int):
    db = await get_db()
    await db.execute(
        "DELETE FROM roulette_queue WHERE user_id = ?",
        (user_id,)
    )
    await db.commit()
    await db.close()


# ================================
# 🔹 Создать активный чат рулетки
# ================================
async def create_pair(user1: int, user2: int):
    db = await get_db()

    await db.execute(
        "INSERT INTO roulette_pairs (user_id, partner_id) VALUES (?, ?)",
        (user1, user2)
    )
    await db.execute(
        "INSERT INTO roulette_pairs (user_id, partner_id) VALUES (?, ?)",
        (user2, user1)
    )

    await db.commit()
    await db.close()


# ================================
# 🔹 Получить собеседника по user_id
# ================================
async def get_partner(user_id: int):
    db = await get_db()

    cursor = await db.execute(
        "SELECT partner_id FROM roulette_pairs WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ================================
# 🔹 Завершить чат рулетки
# ================================
async def end_chat(user_id: int):
    db = await get_db()

    await db.execute(
        "DELETE FROM roulette_pairs WHERE user_id = ? OR partner_id = ?",
        (user_id, user_id)
    )

    await db.commit()
    await db.close()


# ================================
# 🔹 Проверка: есть ли активный чат?
# ================================
async def is_in_chat(user_id: int) -> bool:
    db = await get_db()
    cursor = await db.execute(
        "SELECT 1 FROM roulette_pairs WHERE user_id = ?",
        (user_id,)
    )
    is_chat = await cursor.fetchone()
    await db.close()

    return is_chat is not None
