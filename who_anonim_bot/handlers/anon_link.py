from telegram import Update
from telegram.ext import ContextTypes

from db.links import (
    get_user_link,
    create_new_link,
    regenerate_link,
    count_active_anons,
)

from db.users import set_state
from states.states import (
    MY_LINK_MENU,
)

from keyboards.keyboards import (
    anon_link_menu_kb,
    main_menu_kb,
)

from logger.logger import get_logger

logger = get_logger()


# ======================================================
# 🔹 Показ моей анонимной ссылки
# ======================================================
async def show_my_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # получаем или создаём ссылку
    link_code = await get_user_link(user_id)
    if not link_code:
        link_code = await create_new_link(user_id)

    # считаем активных анонимов
    active_count = await count_active_anons(user_id)

    deep_link = f"https://t.me/{context.bot.username}?start={link_code}"

    text = (
        "🔗 <b>Ваша анонимная ссылка</b>\n\n"
        f"Ваша ссылка:\n<code>{deep_link}</code>\n\n"
        f"🧑‍🦰 Активных анонимов: <b>{active_count}</b>\n\n"
        "Управление 👇"
    )

    await set_state(user_id, MY_LINK_MENU)

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=anon_link_menu_kb()
    )


# ======================================================
# 🔹 Смена анонимной ссылки
# ======================================================
async def change_my_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # генерируем новую ссылку
    new_code = await regenerate_link(user_id)

    new_link = f"https://t.me/{context.bot.username}?start={new_code}"

    text = (
        "🔄 <b>Ссылка обновлена!</b>\n\n"
        f"Новая ссылка:\n<code>{new_link}</code>\n\n"
        "Старая ссылка теперь недействительна."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=anon_link_menu_kb()
    )
