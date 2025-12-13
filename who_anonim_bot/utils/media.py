from telegram import Message


def is_media(message: Message) -> bool:
    """
    Проверяет, содержит ли сообщение медиа
    """
    return any([
        message.photo,
        message.video,
        message.voice,
        message.audio,
        message.document,
        message.sticker
    ])
