from telegram import Update
from telegram.ext import ContextTypes
from config.settings import BOT_USERNAME
from db.users import add_user, set_state
from db.links import find_owner_by_code
from db.anon_chat import start_anon_session
from states.states import MAIN_MENU
from keyboards.keyboards import main_menu_kb


# ==========================================
# 🔹 Приветственное сообщение
# ==========================================
WELCOME_TEXT = (
    "👻 <b>Who?Anonim™</b>\n\n"
    "Добро пожаловать в анонимный чат!\n\n"
    "🔗 Создавай анонимную ссылку\n"
    "🎲 Общайся в рулетке\n"
    "💬 Отвечай анонимам\n"
    "⚠️ И оставайся невидимкой\n\n"
    "Выберите действие снизу 👇"
)


# ==========================================
# 🔹 Обработчик /start
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    await add_user(user_id)                   # регистрация
    await set_state(user_id, MAIN_MENU)       # состояние — главное меню

    # Если /start пришёл с параметром
    # Например: /start Ab91f3
    args = context.args

    if args:
        code = args[0]

        # Проверяем, существует ли ссылка
        owner_id = await find_owner_by_code(code)

        # Если ссылка валидная → запускаем анонимный чат
        if owner_id and owner_id != user_id:
            await start_anon_session(update, context, owner_id)
            return

    # Обычное начало — без ссылки
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu_kb(),
        parse_mode="HTML"
)
