from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import ADMINS
from db.users import is_user_banned


# ─────────────────────
# 🔐 Проверка на админа
# ─────────────────────
def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if user_id not in ADMINS:
            await update.message.reply_text("⛔ У вас нет доступа.")
            return

        return await func(update, context)

    return wrapper


# ─────────────────────
# 🚫 Проверка на бан
# ─────────────────────
def not_banned(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if await is_user_banned(user_id):
            await update.message.reply_text("🚫 Вы заблокированы.")
            return

        return await func(update, context)

    return wrapper
