from .database import get_db


# ================================
# 🔹 Добавить жалобу
# ================================
async def add_complaint(reporter_id: int, target_id: int):
    db = await get_db()

    await db.execute(
        """
        INSERT INTO complaints (reporter_id, target_id)
        VALUES (?, ?)
        """,
        (reporter_id, target_id)
    )

    await db.commit()
    await db.close()


# ================================
# 🔹 Получить последние жалобы
# limit — количество (например 20)
# ================================
async def get_complaints(limit: int = 20):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT reporter_id, target_id, created_at
        FROM complaints
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = await cursor.fetchall()
    await db.close()

    return rows


# ================================
# 🔹 Очистить все жалобы
# ================================
async def clear_complaints():
    db = await get_db()

    await db.execute("DELETE FROM complaints")

    await db.commit()
    await db.close()


# ================================
# 🔹 Сколько жалоб на пользователя?
# ================================
async def count_complaints(target_id: int):
    db = await get_db()

    cursor = await db.execute(
        """
        SELECT COUNT(*) 
        FROM complaints 
        WHERE target_id = ?
        """,
        (target_id,)
    )

    row = await cursor.fetchone()
    await db.close()

    return row[0] if row else 0
