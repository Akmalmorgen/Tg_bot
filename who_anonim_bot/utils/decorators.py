# who_anonim_bot/utils/decorators.py
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import ADMINS
from db.users import is_banned

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in ADMINS:
            await update.message.reply_text("⛔ У вас нет доступа.")
            return
        return await func(update, context)
    return wrapper

def check_ban(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if await is_banned(uid):
            await update.message.reply_text("🚫 Вы заблокированы.")
            return
        return await func(update, context)
    return wrapper
