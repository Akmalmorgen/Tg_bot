from telegram import Update
from telegram.ext import ContextTypes

from keyboards import admin_menu, main_menu
from users import get_all_users, ban_user, unban_user, is_banned
from links import get_all_links
from complaints import (
    get_recent_complaints,
    clear_complaints,
    count_complaints
)
from config import ADMINS
from utils import broadcast_media, broadcast_text


async def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открыть админ-панель"""
    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.message.reply_text("❌ У вас нет доступа.")
        return

    users = await get_all_users()
    links = await get_all_links()
    complaints_count = count_complaints()

    text = (
        "👑 <b>АДМИН ПАНЕЛЬ</b>\n\n"
        f"👥 Пользователи: <b>{len(users)}</b>\n"
        f"🔗 Активных ссылок: <b>{len(links)}</b>\n"
        f"⚠ Жалоб: <b>{complaints_count}</b>\n\n"
        "Выберите действие:"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=admin_menu()
    )


async def handle_admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок админ-панели"""

    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in ADMINS:
        return

    # 📊 Статистика
    if text == "📊 Статистика":
        await open_admin_panel(update, context)
        return

    # 👥 Пользователи
    if text == "👥 Пользователи":
        users = await get_all_users()

        result = "👥 <b>СПИСОК ПОЛЬЗОВАТЕЛЕЙ</b>\n\n"
        for uid in users[:40]:
            mark = "🚫" if await is_banned(uid) else "✅"
            result += f"{mark} <code>{uid}</code>\n"

        await update.message.reply_text(result, parse_mode="HTML")
        return

    # 🔗 Все ссылки
    if text == "🔗 Все ссылки":
        links = await get_all_links()

        msg = "🔗 <b>АКТИВНЫЕ ССЫЛКИ</b>\n\n"
        for owner_id, link_id in list(links.items())[:30]:
            msg += f"<code>{owner_id}</code> → <b>{link_id}</b>\n"

        await update.message.reply_text(msg, parse_mode="HTML")
        return

    # ⚠ Жалобы
    if text == "⚠ Жалобы":
        complaints = get_recent_complaints()

        if not complaints:
            await update.message.reply_text("⚠ Жалоб нет.")
            return

        msg = "⚠ <b>ПОСЛЕДНИЕ ЖАЛОБЫ</b>\n\n"
        for c in complaints:
            msg += (
                f"От: <code>{c['reporter']}</code>\n"
                f"На: <code>{c['reported']}</code>\n"
                f"Причина: {c['reason']}\n"
                "──────────────\n"
            )

        await update.message.reply_text(msg, parse_mode="HTML")
        return

    # 🗑 Очистить жалобы
    if text == "🗑 Очистить жалобы":
        clear_complaints()
        await update.message.reply_text("🗑 Жалобы очищены.")
        return

    # 🚫 Забанить
    if text == "🚫 Забанить":
        await update.message.reply_text("Введите ID пользователя для блокировки:")
        context.user_data["admin_action"] = "ban"
        return

    # ✅ Разбанить
    if text == "✅ Разбанить":
        await update.message.reply_text("Введите ID пользователя для разбана:")
        context.user_data["admin_action"] = "unban"
        return

    # 📢 Рассылка
    if text == "📢 Рассылка":
        await update.message.reply_text(
            "Отправьте текст или медиа для рассылки:"
        )
        context.user_data["admin_action"] = "broadcast"
        return

    # Обработка ввода ID / текста
    if "admin_action" in context.user_data:

        action = context.user_data["admin_action"]

        # BAN
        if action == "ban":
            try:
                target = int(text)
                await ban_user(target)
                await update.message.reply_text(
                    f"🚫 Пользователь <code>{target}</code> забанен.",
                    parse_mode="HTML"
                )
            except:
                await update.message.reply_text("❌ Некорректный ID.")
            del context.user_data["admin_action"]
            return

        # UNBAN
        if action == "unban":
            try:
                target = int(text)
                await unban_user(target)
                await update.message.reply_text(
                    f"✅ Пользователь <code>{target}</code> разбанен.",
                    parse_mode="HTML"
                )
            except:
                await update.message.reply_text("❌ Некорректный ID.")
            del context.user_data["admin_action"]
            return

        # BROADCAST
        if action == "broadcast":
            # текст
            if update.message.text:
                await broadcast_text(update, context)
                del context.user_data["admin_action"]
                return

            # медиа
            await broadcast_media(update, context)
            del context.user_data["admin_action"]
            return
