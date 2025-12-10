# who_anonim_bot/db/users.py
from .database import get_conn
import aiosqlite

async def ensure_user(user_id: int, first_name: str = "Аноним"):
    async with await get_conn() as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(user_id, first_name) VALUES(?,?)",
            (user_id, first_name)
        )
        await db.commit()

async def get_user_state(user_id: int):
    async with await get_conn() as db:
        cur = await db.execute("SELECT state FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else "MAIN_MENU"

async def set_user_state(user_id: int, state: str):
    async with await get_conn() as db:
        await db.execute("UPDATE users SET state=? WHERE user_id=?", (state, user_id))
        await db.commit()

async def is_banned(user_id: int):
    async with await get_conn() as db:
        cur = await db.execute("SELECT banned FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return bool(row and row[0] == 1)

async def set_banned(user_id: int, banned: bool = True):
    async with await get_conn() as db:
        await db.execute("UPDATE users SET banned=? WHERE user_id=?", (1 if banned else 0, user_id))
        await db.commit()
