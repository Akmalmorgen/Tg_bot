import secrets
from .database import Database


# ───────────────
# Анонимные ссылки
# ───────────────

def generate_link_code() -> str:
    """
    Генерирует уникальный код ссылки
    """
    return secrets.token_hex(4)  # например: a9f3c21b


async def create_or_get_link(user_id: int) -> str:
    """
    Возвращает существующую ссылку пользователя
    или создаёт новую
    """
    async with Database.connect() as db:
        cursor = await db.execute(
            "SELECT link_code FROM anon_links WHERE owner_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        link_code = generate_link_code()

        await db.execute(
            """
            INSERT INTO anon_links (owner_id, link_code)
            VALUES (?, ?)
            """,
            (user_id, link_code),
        )
        await db.commit()

        return link_code


async def change_link(user_id: int) -> str:
    """
    Сменить анонимную ссылку
    """
    new_code = generate_link_code()

    async with Database.connect() as db:
        await db.execute(
            """
            UPDATE anon_links
            SET link_code = ?
            WHERE owner_id = ?
            """,
            (new_code, user_id),
        )
        await db.commit()

    return new_code


async def get_owner_by_code(link_code: str) -> int | None:
    """
    Получить владельца ссылки по коду
    """
    async with Database.connect() as db:
        cursor = await db.execute(
            "SELECT owner_id FROM anon_links WHERE link_code = ?",
            (link_code,),
        )
        row = await cursor.fetchone()
        return row[0] if row else None


async def delete_link(user_id: int):
    """
    Удалить ссылку пользователя
    """
    async with Database.connect() as db:
        await db.execute(
            "DELETE FROM anon_links WHERE owner_id = ?",
            (user_id,),
        )
        await db.commit()
