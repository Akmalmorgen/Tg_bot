from .database import get_db


# ======================================
# 🔹 Создать анонимный чат
# user_id — тот, кто зашёл по ссылке
# owner_id — владелец ссылки
# ======================================
async def create_session(user_id: int, owner_id: int):
    db = await get_db()

    await db.execute(
        "INSERT INTO anon_sessions (user_id, owner_id) VALUES (?, ?)",
        (user_id, owner_id)
    )

    await db.commit()
    await db.close()


# ======================================
# 🔹 Получить владельца ссылки по user_id
# Если человек пишет — надо понять кому
# ======================================
async def get_owner(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT owner_id FROM anon_sessions WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ======================================
# 🔹 Получить анонима, который пишет владельцу
# Нужен когда владелец хочет ответить
# ======================================
async def get_partner_for_owner(owner_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT user_id FROM anon_sessions WHERE owner_id = ? ORDER BY id DESC LIMIT 1",
        (owner_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ======================================
# 🔹 Удалить чат (выйти)
# ======================================
async def delete_session(user_id: int):
    db = await get_db()
    await db.execute(
        "DELETE FROM anon_sessions WHERE user_id = ? OR owner_id = ?",
        (user_id, user_id)
    )
    await db.commit()
    await db.close()


# ======================================
# 🔹 Проверка есть ли активный чат
# ======================================
async def is_in_chat(user_id: int) -> bool:
    db = await get_db()
    cursor = await db.execute(
        "SELECT 1 FROM anon_sessions WHERE user_id = ? OR owner_id = ?",
        (user_id, user_id)
    )
    row = await cursor.fetchone()
    await db.close()

    return row is not None
