from functools import wraps
from config.settings import ADMINS, BANNED_USERS
from telegram import Update
from telegram.ext import ContextTypes


def admin_only(func):
    """Декоратор — доступ только админам"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMINS:
            await update.message.reply_text("❌ Эта команда доступна только администраторам.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def check_ban(func):
    """Декоратор — проверка бана"""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id in BANNED_USERS:
            await update.message.reply_text("🚫 Вы заблокированы.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
