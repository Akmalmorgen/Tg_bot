import aiosqlite
from config.settings import DATABASE_PATH


# === Добавить пользователя ===
async def add_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, state) VALUES (?, ?)",
            (user_id, "main_menu")
        )
        await db.commit()


# === Получить состояние пользователя ===
async def get_user_state(user_id: int) -> str:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT state FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
    return row[0] if row else "main_menu"


# === Установить состояние ===
async def set_state(user_id: int, state: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET state = ? WHERE user_id = ?",
            (state, user_id)
        )
        await db.commit()


# === Получить всех пользователей ===
async def get_all_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()
    return [row[0] for row in rows]


# === Бан ===
async def ban_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET banned = 1 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


async def unban_user(user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET banned = 0 WHERE user_id = ?",
            (user_id,)
        )
        await db.commit()


async def is_banned(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT banned FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
    return row and row[0] == 1
