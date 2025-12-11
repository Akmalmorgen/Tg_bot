from .database import Database

async def get_state(user_id):
    async with Database.connect() as db:
        cur = await db.execute("SELECT state FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None

async def set_state(user_id, state):
    async with Database.connect() as db:
        await db.execute(
            "INSERT INTO users (user_id, state) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET state = excluded.state",
            (user_id, state),
        )
        await db.commit()

async def set_gender(user_id, gender):
    async with Database.connect() as db:
        await db.execute(
            "UPDATE users SET gender = ? WHERE user_id = ?",
            (gender, user_id),
        )
        await db.commit()

async def get_gender(user_id):
    async with Database.connect() as db:
        cur = await db.execute("SELECT gender FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return row[0] if row else None

async def set_partner(user_id, partner_id):
    async with Database.connect() as db:
        await db.execute(
            "UPDATE users SET in_chat_with = ? WHERE user_id = ?",
            (partner_id, user_id)
        )
        await db.commit()

async def get_partner(user_id):
    async with Database.connect() as db:
        cur = await db.execute(
            "SELECT in_chat_with FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else None

async def clear_partner(user_id):
    await set_partner(user_id, None)
