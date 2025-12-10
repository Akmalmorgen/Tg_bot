# who_anonim_bot/handlers/anon_link.py
from telegram.ext import MessageHandler, filters
from keyboards.keyboards import anon_link_menu, anon_owner_menu, owner_inline_buttons, report_reason_keyboard
from db.links import get_link_for_user, change_link_for_user, get_owner_by_link
from db.anon_chat import create_anon_session, get_latest_session_for_anon
from states.states import MY_LINK, ANON_CONNECTED_PREFIX
from utils.media import copy_message

async def show_my_link(update, context):
    uid = update.effective_user.id
    link = await get_link_for_user(uid)
    tg_link = f"https://t.me/{context.bot.username}?start={link}"
    await set_state = None  # placeholder for optional state write
    await update.message.reply_text(f"🔗 Ваша ссылка:\n{tg_link}", reply_markup=anon_link_menu())

async def handle_link_menu_actions(update, context):
    text = update.message.text
    uid = update.effective_user.id
    if text == "🔄 Сменить ссылку":
        new_code = await change_link_for_user(uid)
        await update.message.reply_text(f"✅ Ссылка изменена: https://t.me/{context.bot.username}?start={new_code}", reply_markup=anon_link_menu())
    elif text == "⬅️ Назад":
        await update.message.reply_text("Главное меню:", reply_markup=main_menu_keyboard(uid in context.bot.bot_data.get("admins", [])))

def register_anon_link_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("^🔄 Сменить ссылку$|^⬅️ Назад$"), handle_link_menu_actions))
