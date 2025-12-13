import aiosqlite
from pathlib import Path


# Путь к базе данных (SQLite)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.sqlite3"


class Database:
    @staticmethod
    def connect():
        """
        Подключение к SQLite
        """
        return aiosqlite.connect(DB_PATH)


async def init_db():
    """
    Инициализация всех таблиц
    """
    async with Database.connect() as db:
        # Пользователи
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            state TEXT,
            is_banned INTEGER DEFAULT 0
        )
        """)

        # Анонимные ссылки
        await db.execute("""
        CREATE TABLE IF NOT EXISTS anon_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER UNIQUE,
            link_code TEXT UNIQUE
        )
        """)

        # Анонимные сессии (через ссылку)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS anon_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            anon_id TEXT,
            is_active INTEGER DEFAULT 1
        )
        """)

        # Рулетка
        await db.execute("""
        CREATE TABLE IF NOT EXISTS roulette_queue (
            user_id INTEGER PRIMARY KEY,
            gender TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS roulette_chats (
            user_id INTEGER PRIMARY KEY,
            partner_id INTEGER
        )
        """)

        # Жалобы
        await db.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user INTEGER,
            to_user INTEGER,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()
