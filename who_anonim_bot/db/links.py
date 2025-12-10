# who_anonim_bot/db/links.py
import random, time
from .database import get_conn

def _gen_link():
    return str(random.randint(100000, 999999))

async def get_link_for_user(user_id: int):
    async with await get_conn() as db:
        cur = await db.execute("SELECT link_id FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        if row and row[0]:
            return row[0]
        # create new
        link_id = _gen_link()
        created_at = int(time.time())
        await db.execute("UPDATE users SET link_id=? WHERE user_id=?", (link_id, user_id))
        await db.execute("INSERT OR REPLACE INTO links(link_id, owner_id, created_at) VALUES(?,?,?)", (link_id, user_id, created_at))
        await db.commit()
        return link_id

async def change_link_for_user(user_id: int):
    async with await get_conn() as db:
        # remove old
        cur = await db.execute("SELECT link_id FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        if row and row[0]:
            await db.execute("DELETE FROM links WHERE link_id=?", (row[0],))
        link_id = _gen_link()
        created_at = int(time.time())
        await db.execute("UPDATE users SET link_id=? WHERE user_id=?", (link_id, user_id))
        await db.execute("INSERT OR REPLACE INTO links(link_id, owner_id, created_at) VALUES(?,?,?)", (link_id, user_id, created_at))
        await db.commit()
        return link_id

async def get_owner_by_link(link_id: str):
    async with await get_conn() as db:
        cur = await db.execute("SELECT owner_id FROM links WHERE link_id=?", (link_id,))
        row = await cur.fetchone()
        return row[0] if row else None
