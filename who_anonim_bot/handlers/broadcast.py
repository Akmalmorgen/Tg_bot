from telegram import Update
from telegram.ext import ContextTypes

from states.states import UserState
from db.users import get_all_users, is_banned, set_state


async def broadcast_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_state(update.effective_user.id, UserState.BROADCAST)
    await update.message.reply_text(
        "📢 <b>РАССЫЛКА</b>\n\n"
        "Отправьте текст для рассылки:",
        parse_mode="HTML"
    )


async def broadcast_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    users = get_all_users()

    success = 0
    for uid in users:
        if not is_banned(uid):
            try:
                await context.bot.send_message(
                    uid,
                    f"📢 <b>Сообщение:</b>\n\n{text}",
                    parse_mode="HTML"
                )
                success += 1
            except:
                pass

    set_state(update.effective_user.id, UserState.ADMIN_PANEL)
    await update.message.reply_text(f"✅ Рассылка отправлена: {success} пользователям")
