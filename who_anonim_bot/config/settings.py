# who_anonim_bot/config/settings.py

# Если деплоишь на хостинге — используйте переменные окружения.
import os

TOKEN = os.getenv("8134649307:AAH3k13igSnG9t6lGYYTvu7e2D4RiKaCXMI")  # или вставьте токен сюда (не рекомендуется)
ADMINS = [7967404620]  # список админов (int)
DB_PATH = os.getenv("WHO_ANONIM_DB", "database.db")
BOT_USERNAME = os.getenv("WHO_ANONIM_USERNAME", "Who_Anonim_Bot")  # optional
