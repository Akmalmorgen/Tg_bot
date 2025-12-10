# who_anonim_bot/db/complaints.py
import time
from .database import get_conn

async def add_complaint(reporter_id: int, reported_id: int, offender_anon_tag: str, reason: str, chat_type: str):
    async with await get_conn() as db:
        await db.execute("INSERT INTO complaints(reporter_id, reported_id, offender_anon_tag, reason, date, chat_type) VALUES(?,?,?,?,?,?)",
                         (reporter_id, reported_id, offender_anon_tag, reason, int(time.time()), chat_type))
        await db.commit()

async def list_complaints(limit: int = 50):
    async with await get_conn() as db:
        cur = await db.execute("SELECT id, reporter_id, reported_id, offender_anon_tag, reason, date FROM complaints ORDER BY id DESC LIMIT ?", (limit,))
        return await cur.fetchall()

async def clear_complaints():
    async with await get_conn() as db:
        await db.execute("DELETE FROM complaints")
        await db.commit()
