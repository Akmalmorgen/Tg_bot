from .database import Database


async def add_to_queue(user_id: int, gender: str):
    async with Database.connect() as db:
        await db.execute(
            "INSERT OR REPLACE INTO roulette_waiting (user_id, gender) VALUES (?, ?)",
            (user_id, gender),
        )
        await db.commit()


async def remove_from_queue(user_id: int):
    async with Database.connect() as db:
        await db.execute(
            "DELETE FROM roulette_waiting WHERE user_id = ?",
            (user_id,),
        )
        await db.commit()


async def find_partner(user_id: int, gender: str):
    async with Database.connect() as db:
        cursor = await db.execute(
            """
            SELECT user_id FROM roulette_waiting
            WHERE gender = ? AND user_id != ?
            LIMIT 1
            """,
            (gender, user_id),
        )
        row = await cursor.fetchone()

        if not row:
            return None

        partner_id = row[0]

        # Удаляем обоих из очереди
        await db.execute(
            "DELETE FROM roulette_waiting WHERE user_id IN (?, ?)",
            (user_id, partner_id),
        )
        await db.commit()

        return partner_id
