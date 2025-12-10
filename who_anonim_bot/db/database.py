# who_anonim_bot/db/database.py
import aiosqlite
from config.settings import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                gender TEXT,
                link_id TEXT,
                banned INTEGER DEFAULT 0,
                state TEXT DEFAULT 'MAIN_MENU'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS links(
                link_id TEXT PRIMARY KEY,
                owner_id INTEGER,
                created_at INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS anon_sessions(
                session_id TEXT PRIMARY KEY,
                anon_user_id INTEGER,
                owner_id INTEGER,
                anon_tag TEXT,
                created_at INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS active_chats(
                user_id INTEGER PRIMARY KEY,
                partner_id INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS complaints(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_id INTEGER,
                reported_id INTEGER,
                offender_anon_tag TEXT,
                reason TEXT,
                date INTEGER,
                chat_type TEXT
            )
        """)
        await db.commit()

async def get_conn():
    return await aiosqlite.connect(DB_PATH)
