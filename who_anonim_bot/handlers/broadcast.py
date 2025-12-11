from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from config.settings import ADMINS
from db.users import get_all_users
from utils.media import forward_message_safe

# Состояния
WAIT_BROADCAST = 1001


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Старт режима рассылки"""
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return

    await update.message.reply_text(
        "Введите текст или отправьте фото/видео/файл для рассылки.\n\n"
        "❗ Чтобы отменить, отправьте: Отмена"
    )
    return WAIT_BROADCAST


async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка рассылки всем пользователям"""
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return ConversationHandler.END

    # Отмена
    if update.message.text and update.message.text.lower() == "отмена":
        await update.message.reply_text("❌ Рассылка отменена.")
        return ConversationHandler.END

    users = await get_all_users()

    sent = 0
    fail = 0

    for uid in users:
        try:
            await forward_message_safe(update, uid)
            sent += 1
        except:
            fail += 1

    await update.message.reply_text(
        f"📢 Рассылка завершена!\n\n"
        f"Отправлено: {sent}\n"
        f"Ошибок: {fail}"
    )

    return ConversationHandler.END


def register_broadcast_handler(app):
    """Регистрация хендлеров"""

    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^📢 Рассылка$"), start_broadcast)
        ],
        states={
            WAIT_BROADCAST: [
                MessageHandler(filters.ALL, send_broadcast)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex("^Отмена$"), send_broadcast)
        ]
    )

    app.add_handler(conv)
