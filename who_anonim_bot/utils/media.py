from telegram import Message


async def send_media_copy(bot, chat_id: int, message: Message):
    """
    Универсальная отправка любых медиа через copy_message.
    Работает для фото, видео, голосовых, документов, GIF и т.д.
    """
    try:
        return await bot.copy_message(chat_id, message.chat_id, message.message_id)
    except Exception as e:
        print("Ошибка при отправке медиа:", e)
        return None
