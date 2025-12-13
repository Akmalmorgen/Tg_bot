import uuid
from .database import Database

def _new_session_id() -> str:
    return uuid.uuid4().hex[:12]


async def create_session(owner_id: int, guest_id: int) -> str:
    session_id = _new_session_id()
    async with Database.connect() as db:
        await db.execute(
            """
            INSERT INTO anon_sessions (session_id, owner_id, guest_id)
            VALUES (?, ?, ?)
            """,
            (session_id, owner_id, guest_id),
        )
        await db.commit()
    return session_id


async def get_session_by_user(user_id: int):
    async with Database.connect() as db:
        cursor = await db.execute(
            """
            SELECT session_id, owner_id, guest_id
            FROM anon_sessions
            WHERE owner_id = ? OR guest_id = ?
            """,
            (user_id, user_id),
        )
        return await cursor.fetchone()


async def get_partner(user_id: int):
    session = await get_session_by_user(user_id)
    if not session:
        return None

    _, owner_id, guest_id = session
    return guest_id if user_id == owner_id else owner_id


async def close_session(session_id: str):
    async with Database.connect() as db:
        await db.execute(
            "DELETE FROM anon_sessions WHERE session_id = ?",
            (session_id,),
        )
        await db.commit()
