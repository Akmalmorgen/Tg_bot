import random
import time
from .database import get_db

def generate_code():
    return "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(8))

async def create_or_update_link(user_id):
    code = generate_code()
    async with await get_db() as db:
        await db.execute("""
            INSERT INTO anon_links (user_id, link_code, last_active)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET link_code=?, last_active=?
        """, (user_id, code, int(time.time()), code, int(time.time())))
        await db.commit()
    return code

async def get_user_link(user_id):
    async with await get_db() as db:
        cur = await db.execute("SELECT link_code FROM anon_links WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None

async def touch_link(user_id):
    async with await get_db() as db:
        await db.execute("UPDATE anon_links SET last_active=? WHERE user_id=?", (int(time.time()), user_id))
        await db.commit()

async def delete_old_links(days=7):
    threshold = int(time.time()) - days * 86400
    async with await get_db() as db:
        await db.execute("DELETE FROM anon_links WHERE last_active < ?", (threshold,))
        await db.commit()

async def get_all_links():
    async with await get_db() as db:
        cur = await db.execute("SELECT user_id, link_code FROM anon_links")
        return await cur.fetchall()
