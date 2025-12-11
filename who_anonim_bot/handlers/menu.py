from telegram import Update
from telegram.ext import ContextTypes

from db.users import get_user_state, set_state
from states.states import MAIN_MENU

from keyboards.keyboards import main_menu_kb, help_kb
from handlers.anon_link import show_my_link
from handlers.roulette import start_roulette_handler
from handlers.admin import admin_panel
from config.settings import ADMINS


# ======================================================
# 🔹 Главное меню — универсальная точка входа
# ======================================================
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    # Всегда ставим состояние меню
    await set_state(user_id, MAIN_MENU)

    # --- Кнопки меню ---
    if text == "🔗 Моя анон-ссылка":
        await show_my_link(update, context)
        return

    if text == "🎲 Рулетка":
        await start_roulette_handler(update, context)
        return

    if text == "💬 Помощь":
        await show_help(update, context)
        return

    if text == "⚙️ Админ-панель":
        if user_id in ADMINS:
            await admin_panel(update, context)
        else:
            await update.message.reply_text("❌ У вас нет доступа.")
        return

    # Если текст неизвестный
    await update.message.reply_text(
        "Выберите действие снизу 👇",
        reply_markup=main_menu_kb()
    )


# ======================================================
# 🔹 Помощь
# ======================================================
async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📘 <b>Помощь</b>\n\n"
        "🔗 Создай свою анонимную ссылку и делись ею.\n"
        "🎲 Общайся в рулетке.\n"
        "💬 Отвечай анонимным пользователям.\n\n"
        "👨‍💻 Для сотрудничества: @who_mercy"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu_kb()
    )
