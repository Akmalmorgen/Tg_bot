# who_anonim_bot/handlers/admin.py
from telegram.ext import MessageHandler, filters
from keyboards.keyboards import admin_menu, main_menu_keyboard
from db.users import get_user_state, set_user_state, set_banned
from db.links import get_all_links
from db.complaints import list_complaints, clear_complaints
from config.settings import ADMINS

async def open_admin_panel(update, context):
    uid = update.effective_user.id
    if uid not in ADMINS:
        await update.message.reply_text("⛔ У вас нет доступа.")
        return
    await set_user_state(uid, "ADMIN_PANEL")
    await update.message.reply_text("⚙️ Админ-панель:", reply_markup=admin_menu())

async def handle_admin_actions(update, context):
    text = update.message.text
    uid = update.effective_user.id
    if text == "🗑 Очистить жалобы":
        await clear_complaints()
        await update.message.reply_text("✅ Жалобы очищены.", reply_markup=admin_menu())

def register_admin_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("^⚙️ Админ-панель$|^🗑 Очистить жалобы$"), open_admin_panel))
