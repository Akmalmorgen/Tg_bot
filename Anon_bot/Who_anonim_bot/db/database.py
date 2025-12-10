import aiosqlite

DB_PATH = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                gender TEXT,
                banned INTEGER DEFAULT 0
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS anon_links(
                user_id INTEGER PRIMARY KEY,
                link_code TEXT,
                last_active INTEGER
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS anon_sessions(
                session_id TEXT PRIMARY KEY,
                owner_id INTEGER,
                guest_id INTEGER,
                active INTEGER DEFAULT 1
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS roulette_queue(
                user_id INTEGER PRIMARY KEY,
                gender TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS roulette_sessions(
                user_id INTEGER PRIMARY KEY,
                partner_id INTEGER
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS complaints(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user INTEGER,
                to_user INTEGER,
                reason TEXT,
                timestamp INTEGER
            )
        """)

        await db.commit()


async def get_db():
    return await aiosqlite.connect(DB_PATH)
