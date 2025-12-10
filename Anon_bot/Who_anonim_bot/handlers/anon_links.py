from db.links import get_user_link, create_or_update_link
from keyboards.keyboards import anon_link_menu
from states.states import set_state

async def show_my_link(update, context):
    user_id = update.effective_user.id

    link = await get_user_link(user_id)
    if not link:
        link = await create_or_update_link(user_id)

    tg_link = f"https://t.me/{context.bot.username}?start={link}"

    text = (
        "🔗 <b>Ваша анонимная ссылка</b>\n\n"
        f"<code>{tg_link}</code>\n\n"
        "Вы можете:\n"
        "🔄 Сменить ссылку\n"
        "⬅️ Назад\n"
    )

    await set_state(user_id, "MY_LINK")
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=anon_link_menu())


async def handle_my_link(update, context):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🔄 Сменить ссылку":
        new_code = await create_or_update_link(user_id)
        tg_link = f"https://t.me/{context.bot.username}?start={new_code}"

        return await update.message.reply_text(
            f"✅ Ссылка обновлена!\n\n<code>{tg_link}</code>",
            parse_mode="HTML",
            reply_markup=anon_link_menu()
        )

def register_anon_link_handlers(app):
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(🔗|🔄|⬅️)$"), handle_my_link))
