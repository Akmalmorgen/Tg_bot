# who_anonim_bot/handlers/broadcast.py
from telegram.ext import MessageHandler, filters
from config.settings import ADMINS
from db.users import get_conn  # not used directly; you'll iterate users
import aiosqlite

async def ask_broadcast(update, context):
    uid = update.effective_user.id
    if uid not in ADMINS:
        await update.message.reply_text("⛔")
        return
    context.user_data["broadcast_mode"] = True
    await update.message.reply_text("📢 Пришлите сообщение для рассылки (текст/медиа).")

async def do_broadcast(update, context):
    if not context.user_data.get("broadcast_mode"):
        return
    # iterate users from DB
    from db.database import get_conn
    sent = 0
    failed = 0
    async with await get_conn() as db:
        cur = await db.execute("SELECT user_id FROM users WHERE banned=0")
        rows = await cur.fetchall()
        for r in rows:
            target = r[0]
            try:
                if update.message.text:
                    await context.bot.send_message(target, update.message.text)
                else:
                    await update.message.copy_to(target)
                sent += 1
            except Exception:
                failed += 1
    context.user_data["broadcast_mode"] = False
    await update.message.reply_text(f"✅ Рассылка завершена. Отправлено: {sent}, Ошибок: {failed}")

def register_broadcast_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("^📢 Рассылка$"), ask_broadcast))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, do_broadcast))
