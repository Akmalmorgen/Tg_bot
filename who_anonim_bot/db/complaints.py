from db.database import get_db


async def add_complaint(from_user: int, to_user: int, reason: str):
    db = await get_db()
    await db.execute(
        """
        INSERT INTO complaints (from_user, to_user, reason)
        VALUES (?, ?, ?)
        """,
        (from_user, to_user, reason)
    )
    await db.commit()
    await db.close()


async def get_all_complaints() -> list[tuple]:
    db = await get_db()
    cursor = await db.execute(
        """
        SELECT id, from_user, to_user, reason
        FROM complaints
        ORDER BY id DESC
        """
    )
    rows = await cursor.fetchall()
    await db.close()
    return rows


async def clear_complaints():
    db = await get_db()
    await db.execute("DELETE FROM complaints")
    await db.commit()
    await db.close()
