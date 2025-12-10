from .database import get_db

async def add_user(user_id):
    async with await get_db() as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def set_gender(user_id, gender):
    async with await get_db() as db:
        await db.execute("UPDATE users SET gender=? WHERE user_id=?", (gender, user_id))
        await db.commit()

async def get_user_gender(user_id):
    async with await get_db() as db:
        cur = await db.execute("SELECT gender FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None

async def ban_user(user_id):
    async with await get_db() as db:
        await db.execute("UPDATE users SET banned=1 WHERE user_id=?", (user_id,))
        await db.commit()

async def unban_user(user_id):
    async with await get_db() as db:
        await db.execute("UPDATE users SET banned=0 WHERE user_id=?", (user_id,))
        await db.commit()

async def is_banned(user_id):
    async with await get_db() as db:
        cur = await db.execute("SELECT banned FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        return row[0] == 1 if row else False

async def count_users():
    async with await get_db() as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        row = await cur.fetchone()
        return row[0]
