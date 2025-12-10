# who_anonim_bot/db/roulette.py
from .database import get_conn

async def add_to_queue(user_id: int, gender: str):
    async with await get_conn() as db:
        await db.execute("INSERT OR REPLACE INTO roulette_queue(user_id, gender) VALUES(?,?)", (user_id, gender))
        await db.commit()

async def remove_from_queue(user_id: int):
    async with await get_conn() as db:
        await db.execute("DELETE FROM roulette_queue WHERE user_id=?", (user_id,))
        await db.commit()

async def find_partner_for(user_id: int, gender: str):
    # find first user of opposite gender
    opposite = "F" if gender == "M" else "M"
    async with await get_conn() as db:
        cur = await db.execute("SELECT user_id FROM roulette_queue WHERE gender=? AND user_id!=? LIMIT 1", (opposite, user_id))
        row = await cur.fetchone()
        return row[0] if row else None

async def set_active_pair(user_id: int, partner_id: int):
    async with await get_conn() as db:
        await db.execute("INSERT OR REPLACE INTO roulette_sessions(user_id, partner_id) VALUES(?,?)", (user_id, partner_id))
        await db.execute("INSERT OR REPLACE INTO roulette_sessions(user_id, partner_id) VALUES(?,?)", (partner_id, user_id))
        await db.commit()

async def get_partner(user_id: int):
    async with await get_conn() as db:
        cur = await db.execute("SELECT partner_id FROM roulette_sessions WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None

async def clear_session(user_id: int):
    partner = await get_partner(user_id)
    async with await get_conn() as db:
        await db.execute("DELETE FROM roulette_sessions WHERE user_id IN (?,?)", (user_id, partner if partner else -1))
        await db.commit()
