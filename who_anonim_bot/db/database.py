import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bot.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            state TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS anon_links (
            user_id INTEGER PRIMARY KEY,
            link_code TEXT UNIQUE
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS anon_sessions (
            anon_id TEXT,
            owner_id INTEGER,
            sender_id INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user INTEGER,
            to_user INTEGER,
            reason TEXT
        )
        """)

        await db.commit()


async def get_db():
    return await aiosqlite.connect(DB_PATH)
