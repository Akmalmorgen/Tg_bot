from db.database import get_db


async def add_user(user_id: int):
    db = await get_db()
    await db.execute(
        "INSERT OR IGNORE INTO users (user_id, state) VALUES (?, ?)",
        (user_id, "MAIN_MENU")
    )
    await db.commit()
    await db.close()


async def get_user_state(user_id: int) -> str:
    db = await get_db()
    cursor = await db.execute(
        "SELECT state FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    if row:
        return row[0]
    return "MAIN_MENU"


async def set_user_state(user_id: int, state: str):
    db = await get_db()
    await db.execute(
        "UPDATE users SET state = ? WHERE user_id = ?",
        (state, user_id)
    )
    await db.commit()
    await db.close()


async def user_exists(user_id: int) -> bool:
    db = await get_db()
    cursor = await db.execute(
        "SELECT 1 FROM users WHERE user_id = ?",
        (user_id,)
    )
    exists = await cursor.fetchone() is not None
    await db.close()
    return exists
