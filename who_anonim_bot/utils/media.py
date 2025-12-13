from telegram import Update
from telegram.ext import ContextTypes


async def send_any_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int
):
    """
    Копирует ЛЮБОЕ сообщение:
    - текст
    - фото
    - видео
    - аудио
    - документ
    - голос
    """

    try:
        await context.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id
        )
        return True

    except Exception as e:
        print(f"[MEDIA ERROR] {e}")
        return False
