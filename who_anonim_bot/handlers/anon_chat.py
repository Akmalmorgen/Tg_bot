from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes

from db.anon_chat import (
    create_session,
    get_session_partner,
    save_message,
    close_session,
)
from db.users import set_state
from db.complaints import add_complaint

from states.states import ANON_CHAT
from keyboards.keyboards import main_menu_kb

from logger.logger import get_logger

logger = get_logger()


# =====================================================
# 🔹 Вход в анонимный чат по ссылке
# =====================================================
async def start_anon_session(update: Update, context: ContextTypes.DEFAULT_TYPE, owner_id: int):
    """Создание анонимной сессии для человека, который зашел по ссылке"""

    user_id = update.effective_user.id

    # ❗ создаём или находим существующую сессию
    anon_id = await create_session(user_id, owner_id)

    await set_state(user_id, ANON_CHAT)

    await update.message.reply_text(
        f"🟢 <b>Вы подключены</b>\n\n"
        f"Теперь можете писать анонимно.",
        parse_mode="HTML",
    )

    # уведомление владельцу
    await context.bot.send_message(
        owner_id,
        f"📨 <b>Новое сообщение от Аноним #{anon_id}</b>\n"
        f"Пользователь подключился.",
        parse_mode="HTML"
    )


# =====================================================
# 🔹 Inline кнопки: Ответить / Пожаловаться
# =====================================================
def owner_buttons(anon_user_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{anon_user_id}"),
            InlineKeyboardButton("⚠️ Пожаловаться", callback_data=f"report:{anon_user_id}")
        ]
    ])


def complaint_buttons(anon_user_id: int):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟥 Мат", callback_data=f"reason:mat:{anon_user_id}")],
        [InlineKeyboardButton("🟧 Спам", callback_data=f"reason:spam:{anon_user_id}")],
        [InlineKeyboardButton("🟨 18+ контент", callback_data=f"reason:adult:{anon_user_id}")],
        [InlineKeyboardButton("🟦 Угроза", callback_data=f"reason:threat:{anon_user_id}")]
    ])


# =====================================================
# 🔹 Сообщения внутри анонимного чата
# =====================================================
async def anon_chat_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сообщения того, кто пишет владельцу ссылки"""

    user_id = update.effective_user.id
    text = update.message.text

    # находим собеседника
    partner_id, anon_id = await get_session_partner(user_id)

    if not partner_id:
        await update.message.reply_text(
            "❌ Чат завершён.",
            reply_markup=main_menu_kb()
        )
        return

    # сохраняем для истории
    await save_message(user_id, partner_id, text)

    # отправка владельцу
    await context.bot.send_message(
        partner_id,
        f"🕶 Сообщение от Аноним #{anon_id}:\n\n{text}",
        reply_markup=owner_buttons(user_id)
    )


# =====================================================
# 🔹 Ответ владельца
# =====================================================
async def callback_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split(":")
    anon_user_id = int(data[1])

    context.user_data["reply_to"] = anon_user_id

    await query.message.reply_text(
        "✍️ Напишите ответ:",
    )


async def owner_reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    owner_id = update.effective_user.id
    text = update.message.text

    if "reply_to" not in context.user_data:
        return

    target = context.user_data["reply_to"]
    del context.user_data["reply_to"]

    partner_id, anon_id = await get_session_partner(target)

    # отправляем обратно анониму
    await update.message.bot.send_message(
        target,
        f"💬 Ответ собеседника:\n\n{text}"
    )

    # сохраняем в истории
    await save_message(owner_id, target, text)

    await update.message.reply_text("✅ Отправлено.")


# =====================================================
# 🔹 Пожаловаться
# =====================================================
async def callback_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    anon_user_id = int(query.data.split(":")[1])

    await query.message.reply_text(
        "⚠️ Выберите причину жалобы:",
        reply_markup=complaint_buttons(anon_user_id)
    )


# =====================================================
# 🔹 Выбор причины жалобы
# =====================================================
async def callback_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, reason, anon_user_id = query.data.split(":")
    anon_user_id = int(anon_user_id)

    # записываем жалобу в БД
    await add_complaint(reporter=query.from_user.id, reported=anon_user_id, reason=reason)

    await query.message.reply_text("✅ Жалоба отправлена администратору.")


# =====================================================
# 🔹 Завершение анонимного чата
# =====================================================
async def stop_anon_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner_id, anon_id = await get_session_partner(user_id)
    await close_session(user_id)

    if partner_id:
        await context.bot.send_message(
            partner_id,
            f"🔴 Аноним #{anon_id} завершил чат.",
            reply_markup=main_menu_kb()
        )

    await update.message.reply_text(
        "Чат завершён.",
        reply_markup=main_menu_kb()
    )

    await set_state(user_id, "MAIN_MENU")
