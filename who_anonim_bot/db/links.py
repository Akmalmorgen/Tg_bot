import secrets
from .database import get_db


# ========================================
# 🔹 Генерация уникального кода ссылки
# ========================================
def generate_link_code() -> str:
    """Генерирует уникальный код ссылки типа 'A3f9K2'."""
    return secrets.token_hex(3)  # 6 символов


# ========================================
# 🔹 Получить ссылку пользователя
# ========================================
async def get_link(user_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT link_code FROM links WHERE user_id = ?",
        (user_id,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ========================================
# 🔹 Создать или обновить ссылку
# ========================================
async def set_link(user_id: int, new_code: str):
    db = await get_db()
    await db.execute(
        "INSERT INTO links (user_id, link_code) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET link_code = excluded.link_code",
        (user_id, new_code)
    )
    await db.commit()
    await db.close()


# ========================================
# 🔹 Найти пользователя по коду ссылки
# ========================================
async def find_owner_by_code(code: str):
    db = await get_db()
    cursor = await db.execute(
        "SELECT user_id FROM links WHERE link_code = ?",
        (code,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else None


# ========================================
# 🔹 Проверить, существует ли такой код
# ========================================
async def is_code_exists(code: str) -> bool:
    db = await get_db()
    cursor = await db.execute(
        "SELECT 1 FROM links WHERE link_code = ?",
        (code,)
    )
    row = await cursor.fetchone()
    await db.close()

    return row is not None
