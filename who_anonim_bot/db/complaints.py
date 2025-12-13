from .database import Database


async def add_complaint(from_user: int, to_user: int, reason: str | None = None):
    async with Database.connect() as db:
        await db.execute(
            """
            INSERT INTO complaints (from_user, to_user, reason)
            VALUES (?, ?, ?)
            """,
            (from_user, to_user, reason),
        )
        await db.commit()


async def get_all_complaints(limit: int = 50):
    async with Database.connect() as db:
        cursor = await db.execute(
            """
            SELECT id, from_user, to_user, reason, created_at
            FROM complaints
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return await cursor.fetchall()


async def clear_complaints():
    async with Database.connect() as db:
        await db.execute("DELETE FROM complaints")
        await db.commit()
