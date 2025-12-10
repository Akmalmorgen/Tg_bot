# who_anonim_bot/main.py
import asyncio
from telegram.ext import Application
from config.settings import TOKEN
from logger.logger import setup_logger
from db.database import init_db
from handlers import register_all_handlers

def build_app():
    return Application.builder().token(TOKEN).build()

async def run():
    # init
    setup_logger()
    await init_db()

    app = build_app()
    register_all_handlers(app)

    # start polling
    print("🚀 Starting bot...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(run())
