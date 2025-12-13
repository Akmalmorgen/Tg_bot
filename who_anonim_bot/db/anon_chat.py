import random
from db.database import get_db


def generate_anon_id() -> str:
    """
    Генерирует ID анонима вида: 3456
    """
    return str(random.randint(1000, 9999))


async def create_anon_session(owner_id: int, sender_id: int) -> str:
    """
    Создаёт анонимную сессию между отправителем и владельцем ссылки.
    Возвращает anon_id (одинаковый для всей переписки).
    """
    db = await get_db()

    # Проверяем, есть ли уже сессия
    cursor = await db.execute(
        """
        SELECT anon_id FROM anon_sessions
        WHERE owner_id = ? AND sender_id = ?
        """,
        (owner_id, sender_id)
    )
    row = await cursor.fetchone()
    if row:
        await db.close()
        return row[0]

    anon_id = generate_anon_id()

    await db.execute(
        """
        INSERT INTO anon_sessions (anon_id, owner_id, sender_id)
        VALUES (?, ?, ?)
        """,
        (anon_id, owner_id, sender_id)
    )
    await db.commit()
    await db.close()

    return anon_id


async def get_anon_by_sender(sender_id: int) -> tuple | None:
    """
    Получить владельца ссылки и anon_id по отправителю
    """
    db = await get_db()
    cursor = await db.execute(
        """
        SELECT anon_id, owner_id FROM anon_sessions
        WHERE sender_id = ?
        """,
        (sender_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    if row:
        return row  # (anon_id, owner_id)
    return None


async def get_sender_by_anon(owner_id: int, anon_id: str) -> int | None:
    """
    Получить sender_id по anon_id (для ответа владельца)
    """
    db = await get_db()
    cursor = await db.execute(
        """
        SELECT sender_id FROM anon_sessions
        WHERE owner_id = ? AND anon_id = ?
        """,
        (owner_id, anon_id)
    )
    row = await cursor.fetchone()
    await db.close()

    if row:
        return row[0]
    return None


async def close_anon_session(sender_id: int):
    """
    Закрыть анонимную сессию (например, если ссылка сменена)
    """
    db = await get_db()
    await db.execute(
        "DELETE FROM anon_sessions WHERE sender_id = ?",
        (sender_id,)
    )
    await db.commit()
    await db.close()
