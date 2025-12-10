from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from users import is_banned
from complaints import add_complaint

# user_id → owner_id (куда пишет аноним)
active_anon_chats = {}

# owner_id → last_anon_id
last_messages = {}


async def connect_anon(update: Update, context: ContextTypes.DEFAULT_TYPE, link_id: str):
    """Пользователь переходит по анонимной ссылке и начинает чат"""

    user_id = update.effective_user.id

    if await is_banned(user_id):
        await update.message.reply_text("🚫 Вы заблокированы.")
        return

    from links import get_link_owner
    owner_id = await get_link_owner(link_id)

    if owner_id is None:
        await update.message.reply_text("❌ Эта ссылка недействительна.")
        return

    if user_id == owner_id:
        await update.message.reply_text("❌ Вы не можете писать сами себе.")
        return

    # регистрируем чат
    active_anon_chats[user_id] = owner_id
    last_messages[owner_id] = user_id

    await update.message.reply_text(
        "💬 Вы подключились к анонимному чату!\nМожете писать сообщение.",
    )

    # сообщение владельцу
    await context.bot.send_message(
        owner_id,
        "📨  <b>НОВОЕ АНОНИМНОЕ СООБЩЕНИЕ</b>\n\n"
        "Пользователь написал вам анонимно.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{user_id}"),
                InlineKeyboardButton("⚠ Пожаловаться", callback_data=f"report:{user_id}")
            ]
        ])
    )


async def handle_anon_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Аноним отправляет сообщение владельцу"""
    user_id = update.effective_user.id

    if user_id not in active_anon_chats:
        return  # не в анон-чате

    owner_id = active_anon_chats[user_id]
    text = update.message.text

    last_messages[owner_id] = user_id

    await context.bot.send_message(
        owner_id,
        f"🕶 <b>Аноним:</b>\n{text}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{user_id}"),
                InlineKeyboardButton("⚠ Пожаловаться", callback_data=f"report:{user_id}")
            ]
        ])
    )

    await update.message.reply_text("✅ Сообщение отправлено.")


async def anon_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка inline-кнопок: ответ / жалоба"""

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data.startswith("reply:"):
        anon_id = int(data.split(":")[1])
        context.user_data["reply_to"] = anon_id

        await query.message.reply_text(
            "✏ Напишите ответ анониму:"
        )
        return

    if data.startswith("report:"):
        anon_id = int(data.split(":")[1])
        add_complaint(user_id, anon_id, "inline_report")

        await query.message.reply_text("⚠ Жалоба отправлена администратору.")
        return


async def send_owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Владелец отвечает анониму"""
    user_id = update.effective_user.id

    if "reply_to" not in context.user_data:
        return

    anon_id = context.user_data["reply_to"]
    text = update.message.text

    await context.bot.send_message(
        anon_id,
        f"💬 <b>Ответ:</b>\n{text}",
        parse_mode="HTML"
    )

    await update.message.reply_text("✅ Ответ отправлен.")
    del context.user_data["reply_to"]
