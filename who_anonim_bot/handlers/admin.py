from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from config.settings import ADMIN_ID
from states.states import UserState
from db.users import (
    get_all_users,
    get_banned_users,
    ban_user,
    unban_user,
    set_state
)
from db.complaints import get_complaints, clear_complaints


def admin_keyboard():
    keyboard = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("👥 Пользователи")],
        [KeyboardButton("⚠️ Жалобы"), KeyboardButton("🗑 Очистить жалобы")],
        [KeyboardButton("📢 Рассылка")],
        [KeyboardButton("🚫 Забанить"), KeyboardButton("✅ Разбанить")],
        [KeyboardButton("🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет доступа.")
        return

    set_state(user_id, UserState.ADMIN_PANEL)

    users = get_all_users()
    banned = get_banned_users()
    complaints = get_complaints()

    text = (
        "👑 <b>АДМИН ПАНЕЛЬ</b>\n\n"
        f"👥 Пользователей: <b>{len(users)}</b>\n"
        f"🚫 Забанено: <b>{len(banned)}</b>\n"
        f"⚠️ Жалоб: <b>{len(complaints)}</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


async def admin_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id != ADMIN_ID:
        return

    if text == "📊 Статистика":
        await admin_panel(update, context)

    elif text == "👥 Пользователи":
        users = get_all_users()
        msg = "👥 <b>Пользователи:</b>\n\n"
        for uid in users[:20]:
            msg += f"• <code>{uid}</code>\n"
        await update.message.reply_text(msg, parse_mode="HTML")

    elif text == "⚠️ Жалобы":
        complaints = get_complaints()
        if not complaints:
            await update.message.reply_text("✅ Жалоб нет.")
        else:
            msg = "⚠️ <b>Жалобы:</b>\n\n"
            for c in complaints[-10:]:
                msg += f"• {c}\n"
            await update.message.reply_text(msg, parse_mode="HTML")

    elif text == "🗑 Очистить жалобы":
        clear_complaints()
        await update.message.reply_text("✅ Жалобы очищены.")

    elif text == "🚫 Забанить":
        set_state(user_id, UserState.BAN_USER)
        await update.message.reply_text("Введите ID пользователя для бана:")

    elif text == "✅ Разбанить":
        set_state(user_id, UserState.UNBAN_USER)
        await update.message.reply_text("Введите ID пользователя для разбана:")
