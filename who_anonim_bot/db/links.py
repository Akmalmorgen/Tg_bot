import secrets
import string
from .database import Database

def _generate_code(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


async def get_or_create_link(user_id: int) -> str:
    async with Database.connect() as db:
        cursor = await db.execute(
            "SELECT link_code FROM anon_links WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        code = _generate_code()
        await db.execute(
            "INSERT INTO anon_links (user_id, link_code) VALUES (?, ?)",
            (user_id, code)
        )
        await db.commit()
        return code


async def regenerate_link(user_id: int) -> str:
    new_code = _generate_code()
    async with Database.connect() as db:
        await db.execute(
            "INSERT INTO anon_links (user_id, link_code) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET link_code = excluded.link_code",
            (user_id, new_code)
        )
        await db.commit()
    return new_code


async def get_user_by_code(code: str) -> int | None:
    async with Database.connect() as db:
        cursor = await db.execute(
            "SELECT user_id FROM anon_links WHERE link_code = ?",
            (code,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None
