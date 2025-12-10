# who_anonim_bot/db/anon_chat.py
import random, time
from .database import get_conn

def _gen_session():
    return str(random.randint(1000000, 9999999))

async def create_anon_session(anon_user_id: int, owner_id: int):
    session_id = _gen_session()
    anon_tag = str(random.randint(1000, 9999))
    created_at = int(time.time())
    async with await get_conn() as db:
        await db.execute("INSERT INTO anon_sessions(session_id, anon_user_id, owner_id, anon_tag, created_at) VALUES(?,?,?,?,?)",
                         (session_id, anon_user_id, owner_id, anon_tag, created_at))
        await db.commit()
    return session_id, anon_tag

async def get_session(session_id: str):
    async with await get_conn() as db:
        cur = await db.execute("SELECT session_id, anon_user_id, owner_id, anon_tag, created_at FROM anon_sessions WHERE session_id=?", (session_id,))
        return await cur.fetchone()

async def get_latest_session_for_anon(anon_user_id: int):
    async with await get_conn() as db:
        cur = await db.execute("SELECT session_id, owner_id, anon_tag FROM anon_sessions WHERE anon_user_id=? ORDER BY created_at DESC LIMIT 1", (anon_user_id,))
        return await cur.fetchone()
