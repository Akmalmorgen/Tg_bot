from telegram import Update
from telegram.ext import ContextTypes

from db.users import get_all_users, is_banned
from utils.media import forward_media_to_user


async def broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Рассылка текста всем пользователям"""
    text = update.message.text
    success = 0

    users = await get_all_users()

    for user_id in users:
        if await is_banned(user_id):
            continue
        try:
            await context.bot.send_message(user_id, text)
            success += 1
        except:
            pass

    await update.message.reply_text(f"📩 Текст отправлен {success} пользователям.")


async def broadcast_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Рассылка медиа: фото, видео, документ, голосовые"""
    users = await get_all_users()
    sent = 0

    for user_id in users:
        if await is_banned(user_id):
            continue

        ok = await forward_media_to_user(update, context, user_id)
        if ok:
            sent += 1

    await update.message.reply_text(f"📤 Медиа отправлено {sent} пользователям.")
