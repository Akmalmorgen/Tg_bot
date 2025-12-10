import time
from .database import get_db

async def add_complaint(from_user, to_user, reason):
    async with await get_db() as db:
        await db.execute("""
            INSERT INTO complaints (from_user, to_user, reason, timestamp)
            VALUES (?, ?, ?, ?)
        """, (from_user, to_user, reason, int(time.time())))
        await db.commit()

async def get_complaints():
    async with await get_db() as db:
        cur = await db.execute("SELECT * FROM complaints")
        return await cur.fetchall()

async def clear_complaints():
    async with await get_db() as db:
        await db.execute("DELETE FROM complaints")
        await db.commit()
