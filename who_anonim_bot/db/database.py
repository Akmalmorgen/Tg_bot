import aiosqlite

DB_PATH = "who_anonim_bot/database.db"

class Database:
    @staticmethod
    async def connect():
        return await aiosqlite.connect(DB_PATH)

    @staticmethod
    async def init_db():
        async with aiosqlite.connect(DB_PATH) as db:
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    state TEXT DEFAULT 'menu',
                    gender TEXT,
                    in_chat_with INTEGER
                );

                CREATE TABLE IF NOT EXISTS anon_links (
                    user_id INTEGER PRIMARY KEY,
                    link_code TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS anon_sessions (
                    session_id TEXT PRIMARY KEY,
                    owner_id INTEGER,
                    guest_id INTEGER
                );

                CREATE TABLE IF NOT EXISTS roulette_waiting (
                    user_id INTEGER PRIMARY KEY,
                    gender TEXT
                );

                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_user INTEGER,
                    against_user INTEGER,
                    reason TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            await db.commit()
