from .database import get_db

async def add_to_queue(user_id, gender):
    async with await get_db() as db:
        await db.execute(
            "INSERT OR REPLACE INTO roulette_queue (user_id, gender) VALUES (?, ?)",
            (user_id, gender)
        )
        await db.commit()

async def find_partner(user_id, gender):
    async with await get_db() as db:
        cur = await db.execute(
            "SELECT user_id FROM roulette_queue WHERE user_id != ? LIMIT 1",
            (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else None

async def remove_from_queue(user_id):
    async with await get_db() as db:
        await db.execute("DELETE FROM roulette_queue WHERE user_id=?", (user_id,))
        await db.commit()

async def set_partner(user_id, partner_id):
    async with await get_db() as db:
        await db.execute("INSERT OR REPLACE INTO roulette_sessions (user_id, partner_id) VALUES (?, ?)",
                         (user_id, partner_id))
        await db.commit()

async def get_partner(user_id):
    async with await get_db() as db:
        cur = await db.execute("SELECT partner_id FROM roulette_sessions WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None

async def end_chat(user_id):
    async with await get_db() as db:
        await db.execute("DELETE FROM roulette_sessions WHERE user_id=?", (user_id,))
        await db.commit()
