# main.py  (GSM-friendly: all modules are imported flat)
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# simple logger setup
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# конфиг — файл config.py должен лежать рядом
from config import TOKEN, ADMINS

# импорты хендлеров (все файлы в одной папке)
from start import start_command
from menu import handle_main_menu
from anon_link import show_my_link, change_link
from anon_chat_handler import connect_anon, handle_anon_message, anon_callback, send_owner_reply
from roulette_handler import (
    start_gender_choice, pick_gender, cancel_search,
    handle_roulette_message, next_partner, stop_chat_button, report_partner
)
from admin import open_admin_panel, handle_admin_actions
from broadcast import broadcast_text, broadcast_media

# callback handler function name collisions: make sure handler functions exist in files
# register handlers function
def register_handlers(app):
    # basic /start
    app.add_handler(CommandHandler("start", start_command))

    # callback queries (inline buttons: reply/report in anon chats)
    app.add_handler(CallbackQueryHandler(anon_callback))

    # main menu and generic message routing (menu.py)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))

    # anon link messages & anon chat messages:
    # we assume connect_anon is called from start when deep-link /start <code> is used
    # all other non-command messages should be routed to proper handlers inside menu/anon_link/anon_chat handler logic

    # roulette related regex handlers — they are MessageHandlers inside roulette_handler.py
    # but to be safe, register a fallback to handle messages in roulette
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_roulette_message))

    # admin handlers (admin panel buttons and actions)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_actions))

    # broadcast handlers (admin sends content)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_text))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, broadcast_media))

async def main():
    if not TOKEN:
        print("ERROR: TOKEN is empty. Put your bot token in config.py or set WHO_ANONIM_TOKEN env var.")
        return

    # create application
    app = Application.builder().token(TOKEN).build()

    # make admins list available in bot_data if you need
    app.bot_data["admins"] = ADMINS

    # register all handlers
    register_handlers(app)

    print("🚀 Bot starting (GSM-compatible main.py)...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
