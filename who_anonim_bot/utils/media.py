# who_anonim_bot/utils/media.py
async def copy_message(bot, from_chat_id: int, message, to_chat_id: int):
    """
    Generic media/text forward using copy_message where possible.
    message: telegram.Message
    """
    try:
        return await bot.copy_message(chat_id=to_chat_id, from_chat_id=from_chat_id, message_id=message.message_id)
    except Exception as e:
        # fallback: for unknown types, try forward
        try:
            return await bot.forward_message(chat_id=to_chat_id, from_chat_id=from_chat_id, message_id=message.message_id)
        except Exception:
            return None
