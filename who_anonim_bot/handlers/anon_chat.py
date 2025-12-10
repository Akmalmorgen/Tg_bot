# who_anonim_bot/handlers/anon_chat.py
from telegram.ext import CallbackQueryHandler, MessageHandler, filters
from db.links import get_owner_by_link
from db.anon_chat import create_anon_session, get_latest_session_for_anon, get_session
from db.users import ensure_user
from keyboards.keyboards import owner_inline_buttons, report_reason_keyboard
from states.states import WAITING_REPLY_PREFIX
from utils.media import copy_message
import re

async def handle_start_deeplink(update, context):
    # /start <code> handling
    args = context.args
    user = update.effective_user
    if not args:
        return
    code = args[0]
    owner = await get_owner_by_link(code)
    if not owner:
        await update.message.reply_text("❌ Ссылка недействительна.")
        return
    if owner == user.id:
        await update.message.reply_text("❌ Это ваша ссылка!")
        return
    session_id, anon_tag = await create_anon_session(user.id, owner)
    await update.message.reply_text("✅ Вы подключены — напишите сообщение.")
    # notify owner
    try:
        await context.bot.send_message(owner, f"📨 Аноним #{anon_tag} подключился. Когда он напишет — под сообщением появятся кнопки.", reply_markup=None)
    except Exception:
        pass

async def anon_message_from_guest(update, context):
    # anon writes message — forward to owner with inline buttons
    user = update.effective_user
    # get latest session
    sess = await get_latest_session_for_anon(user.id)
    if not sess:
        await update.message.reply_text("❌ Сессия не найдена.")
        return
    session_id, owner_id, anon_tag = sess[0], sess[1], sess[2]
    # forward content using copy_message
    try:
        await copy_message(context.bot, from_chat_id=user.id, message=update.message, to_chat_id=owner_id)
    except Exception:
        pass
    # send inline control under the forwarded message
    await context.bot.send_message(owner_id, f"👤 Аноним #{anon_tag}:", reply_markup=owner_inline_buttons(session_id))
    await update.message.reply_text("✅ Сообщение отправлено анонимно.")

async def callback_query_handler(update, context):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data.startswith("reply:"):
        session = data.split(":",1)[1]
        owner = q.from_user.id
        # set owner's state to waiting reply for this session
        await context.bot.send_message(owner, "✏️ Введите ответ — ваше следующее сообщение будет отправлено анониму.")
        context.user_data["waiting_reply_session"] = session
    elif data.startswith("report:"):
        session = data.split(":",1)[1]
        await q.message.reply_text("📋 Выберите причину:", reply_markup=report_reason_keyboard(session))
    elif data.startswith("report_reason:"):
        _, session, reason = data.split(":",2)
        sess = await get_session(session)
        if not sess:
            await q.message.reply_text("❌ Сессия не найдена.")
            return
        reporter = q.from_user.id
        anon_user_id = sess[1]
        # store complaint
        from db.complaints import add_complaint
        await add_complaint(reporter, anon_user_id, sess[3], reason, chat_type="anon_link")
        await q.message.reply_text("✅ Жалоба отправлена администраторам.")

def register_anon_chat_handlers(app):
    from handlers.start import cmd_start
    # CallbackQuery for reply/report
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    # message handlers will be registered elsewhere:
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, anon_message_from_guest))
