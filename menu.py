from telegram import Update
from telegram.ext import ContextTypes

from keyboards import main_menu, gender_choice_keyboard
from anon_link import show_my_link
from roulette_handler import start_gender_choice
from start import start_command
from config import ADMINS
from admin import open_admin_panel


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок в главном меню"""

    text = update.message.text
    user_id = update.effective_user.id

    # 🔗 Моя анон-ссылка
    if text == "🔗 Моя анон-ссылка":
        await show_my_link(update, context)
        return

    # 🎲 Рулетка
    if text == "🎲 Рулетка":
        await start_gender_choice(update, context)
        return

    # 💬 Помощь
    if text == "💬 Помощь":
        await update.message.reply_text(
            "💡 Помощь и доработки: @who_mercy",
            reply_markup=main_menu()
        )
        return

    # ⚙️ Админ-панель
    if text == "⚙️ Админ-панель" and user_id in ADMINS:
        await open_admin_panel(update, context)
        return

    # Если непонятная команда — показываем меню
    await update.message.reply_text("Выберите действие:", reply_markup=main_menu())
