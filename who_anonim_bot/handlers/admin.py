from telegram import Update
from telegram.ext import ContextTypes

from config.settings import ADMINS
from keyboards.keyboards import admin_menu_kb, main_menu_kb

from db.users import get_all_users, set_state
from db.links import count_links
from db.anon_chat import count_active_sessions
from db.complaints import get_complaints, clear_complaints
from db.users import ban_user, unban_user, get_banned_users

from states.states import (
    ADMIN_MENU,
    ADMIN_BAN,
    ADMIN_UNBAN,
    ADMIN_BROADCAST,
    MAIN_MENU
)

from utils.media import resend_media
from logger.logger import get_logger
logger = get_logger()


# ======================================================
# 🔹 Вход в админ-панель
# ======================================================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.message.reply_text("❌ У вас нет доступа.")
        return

    links_count = await count_links()
    users = await get_all_users()
    sessions = await count_active_sessions()
    complaints = await get_complaints()
    banned = await get_banned_users()

    text = (
        "👑 <b>АДМИН-ПАНЕЛЬ</b>\n\n"
        f"🔗 Активных ссылок: <b>{links_count}</b>\n"
        f"👥 Пользователей: <b>{len(users)}</b>\n"
        f"💬 Активных анон. чатов: <b>{sessions}</b>\n"
        f"⚠️ Жалоб: <b>{len(complaints)}</b>\n"
        f"🚫 Забанено: <b>{len(banned)}</b>\n"
    )

    await set_state(user_id, ADMIN_MENU)

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )


# ======================================================
# 🔹 Показать жалобы
# ======================================================
async def admin_show_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):

    complaints = await get_complaints()

    if not complaints:
        await update.message.reply_text(
            "✔️ Жалоб нет.",
            reply_markup=admin_menu_kb()
        )
        return

    text = "⚠️ <b>ЖАЛОБЫ:</b>\n\n"
    for c in complaints:
        text += (
            f"От: <code>{c['reporter']}</code>\n"
            f"На: <code>{c['reported']}</code>\n"
            f"Причина: <b>{c['reason']}</b>\n"
            "──────────────\n"
        )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )


# ======================================================
# 🔹 Очистить жалобы
# ======================================================
async def admin_clear_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await clear_complaints()

    await update.message.reply_text(
        "✔️ Жалобы очищены!",
        reply_markup=admin_menu_kb()
    )


# ======================================================
# 🔹 Бан пользователя
# ======================================================
async def admin_ban_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    await set_state(user_id, ADMIN_BAN)

    await update.message.reply_text(
        "🚫 Введите ID пользователя для бана:",
        reply_markup=admin_menu_kb()
    )


async def admin_ban_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        target_id = int(update.message.text)
    except:
        await update.message.reply_text("❌ Нужно ввести число.", reply_markup=admin_menu_kb())
        return

    await ban_user(target_id)

    await update.message.reply_text(
        f"🚫 Пользователь <code>{target_id}</code> забанен!",
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )


# ======================================================
# 🔹 Разбан
# ======================================================
async def admin_unban_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    await set_state(user_id, ADMIN_UNBAN)

    banned_list = await get_banned_users()

    if not banned_list:
        await update.message.reply_text(
            "Нет забаненных пользователей.",
            reply_markup=admin_menu_kb()
        )
        return

    text = "🚫 <b>ЗАБАНЕННЫЕ:</b>\n\n"
    for uid in banned_list:
        text += f"• <code>{uid}</code>\n"

    await update.message.reply_text(
        text + "\nВведите ID для разбана:",
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )


async def admin_unban_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        target_id = int(update.message.text)
    except:
        await update.message.reply_text("❌ Введите число.", reply_markup=admin_menu_kb())
        return

    await unban_user(target_id)

    await update.message.reply_text(
        f"✅ Пользователь <code>{target_id}</code> разбанен!",
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )


# ======================================================
# 🔹 Рассылка
# ======================================================
async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    await set_state(user_id, ADMIN_BROADCAST)

    await update.message.reply_text(
        "📢 Отправьте сообщение для рассылки.\n"
        "Можно: текст / фото / видео / файлы",
        reply_markup=admin_menu_kb()
    )


async def admin_broadcast_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = await get_all_users()
    success = 0

    for uid in users:
        try:
            await resend_media(update, uid)
            success += 1
        except Exception as e:
            logger.error(f"Broadcast error to {uid}: {e}")

    await update.message.reply_text(
        f"📢 Успешно отправлено: <b>{success}</b>",
        parse_mode="HTML",
        reply_markup=admin_menu_kb()
    )

    # выход в меню
    await set_state(update.effective_user.id, ADMIN_MENU)
