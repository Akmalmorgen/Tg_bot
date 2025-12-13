import random
import string
from db.database import get_db


def generate_link_code(length: int = 8) -> str:
    """Генерирует уникальный код ссылки"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


async def get_user_link(user_id: int) -> str | None:
    db = await get_db()
    cursor = await db.execute(
        "SELECT link_code FROM anon_links WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    if row:
        return row[0]
    return None


async def create_link(user_id: int) -> str:
    db = await get_db()

    # если ссылка уже есть — возвращаем её
    cursor = await db.execute(
        "SELECT link_code FROM anon_links WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    if row:
        await db.close()
        return row[0]

    # создаём новую
    while True:
        code = generate_link_code()
        cursor = await db.execute(
            "SELECT 1 FROM anon_links WHERE link_code = ?",
            (code,)
        )
        exists = await cursor.fetchone()
        if not exists:
            break

    await db.execute(
        "INSERT INTO anon_links (user_id, link_code) VALUES (?, ?)",
        (user_id, code)
    )
    await db.commit()
    await db.close()

    return code


async def change_link(user_id: int) -> str:
    db = await get_db()

    while True:
        new_code = generate_link_code()
        cursor = await db.execute(
            "SELECT 1 FROM anon_links WHERE link_code = ?",
            (new_code,)
        )
        exists = await cursor.fetchone()
        if not exists:
            break

    await db.execute(
        "UPDATE anon_links SET link_code = ? WHERE user_id = ?",
        (new_code, user_id)
    )
    await db.commit()
    await db.close()

    return new_code


async def get_owner_by_code(link_code: str) -> int | None:
    db = await get_db()
    cursor = await db.execute(
        "SELECT user_id FROM anon_links WHERE link_code = ?",
        (link_code,)
    )
    row = await cursor.fetchone()
    await db.close()

    if row:
        return row[0]
    return None
