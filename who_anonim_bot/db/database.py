import aiosqlite
import os


DB_PATH = "database.db"


async def init_db():
    """
    Создаёт базу данных и все таблицы,
    если они ещё не существуют.
    """
    async with aiosqlite.connect(DB_PATH) as db:

        # ---------- Пользователи ----------
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                state TEXT DEFAULT NULL,
                banned INTEGER DEFAULT 0
            )
        """)

        # ---------- Анонимные ссылки ----------
        await db.execute("""
            CREATE TABLE IF NOT EXISTS links (
                user_id INTEGER PRIMARY KEY,
                link_code TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ---------- Анонимные чаты по ссылке ----------
        await db.execute("""
            CREATE TABLE IF NOT EXISTS anon_sessions (
                session_id TEXT PRIMARY KEY,
                owner_id INTEGER,
                anon_id INTEGER,
                last_message TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ---------- Рулетка ----------
        await db.execute("""
            CREATE TABLE IF NOT EXISTS roulette_queue (
                user_id INTEGER PRIMARY KEY,
                gender TEXT,
                searching INTEGER DEFAULT 1
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS roulette_pairs (
                user_id INTEGER PRIMARY KEY,
                partner_id INTEGER
            )
        """)

        # ---------- Жалобы ----------
        await db.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_id INTEGER,
                target_id INTEGER,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()


async def get_db():
    """
    Открывает соединение с базой данных.
    Каждый вызов -> новое подключение (рекомендуется для aiosqlite).
    """
    return await aiosqlite.connect(DB_PATH)
