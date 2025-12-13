from .database import Database


# ───────────────
# Пользователь
# ───────────────

async def add_user(user_id: int):
    async with Database.connect() as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
            """,
            (user_id,),
        )
        await db.commit()


async def is_user_exists(user_id: int) -> bool:
    async with Database.connect() as db:
        cursor = await db.execute(
            "SELECT 1 FROM users WHERE user_id = ?",
            (user_id,),
        )
        return await cursor.fetchone() is not None


# ───────────────
# Состояния
# ───────────────

async def set_state(user_id: int, state: str | None):
    async with Database.connect() as db:
        await db.execute(
            """
            UPDATE users
            SET state = ?
            WHERE user_id = ?
            """,
            (state, user_id),
        )
        await db.commit()


async def get_user_state(user_id: int) -> str | None:
    async with Database.connect() as db:
        cursor = await db.execute(
            """
            SELECT state
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )
        row = await cursor.fetchone()
        return row[0] if row else None


# ───────────────
# Бан
# ───────────────

async def ban_user(user_id: int):
    async with Database.connect() as db:
        await db.execute(
            "UPDATE users SET banned = 1 WHERE user_id = ?",
            (user_id,),
        )
        await db.commit()


async def unban_user(user_id: int):
    async with Database.connect() as db:
        await db.execute(
            "UPDATE users SET banned = 0 WHERE user_id = ?",
            (user_id,),
        )
        await db.commit()


async def is_banned(user_id: int) -> bool:
    async with Database.connect() as db:
        cursor = await db.execute(
            "SELECT banned FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        return bool(row[0]) if row else False


# ───────────────
# Статистика
# ───────────────

async def get_users_count() -> int:
    async with Database.connect() as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        row = await cursor.fetchone()
        return row[0]
