from db.links import get_user_link
from db.anon_chat import create_session, get_session
from keyboards.keyboards import owner_inline
from utils.media import forward_media
from states.states import set_state

import random
import string

def rand_id():
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))

async def process_deeplink(update, context, code):
    user = update.effective_user
    owner_id = None

    async_link = await get_user_link(user.id)

    # нельзя писать самому себе
    if async_link == code:
        return await update.message.reply_text("❌ Это ваша же ссылка.")

    async with context.bot_data["db"].cursor() as cur:
        await cur.execute("SELECT user_id FROM anon_links WHERE link_code=?", (code,))
        row = await cur.fetchone()
        if not row:
            return await update.message.reply_text("❌ Ссылка недействительна.")
        owner_id = row[0]

    session_id = rand_id()
    await create_session(session_id, owner_id, user.id)

    await update.message.reply_text(
        "💬 Вы подключились! Пишите анонимно.",
        reply_markup=None
    )

    await context.bot.send_message(
        owner_id,
        f"📨 Новое сообщение от Анонима #{session_id[:4]}",
    )

    await set_state(user.id, f"ANON_{session_id}")
    return

async def handle_anon_message(update, context):
    user_id = update.effective_user.id
    state = context.user_data.get("state")

    if not state or not state.startswith("ANON_"):
        return

    session_id = state.replace("ANON_", "")
    session = await get_session(session_id)

    if not session:
        return await update.message.reply_text("❌ Чат закрыт.")

    owner_id = session[1]

    sent = await forward_media(update, owner_id)

    await context.bot.send_message(
        owner_id,
        f"Ответить анониму #{session_id[:4]}",
        reply_markup=owner_inline(session_id)
    )


def register_anon_chat_handlers(app):
    from telegram.ext import MessageHandler, filters

    # сообщения анонима
    app.add_handler(MessageHandler(filters.ALL, handle_anon_message))
