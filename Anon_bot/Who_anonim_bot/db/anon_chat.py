from .database import get_db

async def create_session(session_id, owner_id, guest_id):
    async with await get_db() as db:
        await db.execute("""
            INSERT INTO anon_sessions (session_id, owner_id, guest_id)
            VALUES (?, ?, ?)
        """, (session_id, owner_id, guest_id))
        await db.commit()

async def get_session(session_id):
    async with await get_db() as db:
        cur = await db.execute("SELECT * FROM anon_sessions WHERE session_id=?", (session_id,))
        return await cur.fetchone()

async def close_session(session_id):
    async with await get_db() as db:
        await db.execute("UPDATE anon_sessions SET active=0 WHERE session_id=?", (session_id,))
        await db.commit()
