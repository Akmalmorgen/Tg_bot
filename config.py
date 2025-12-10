# config.py (place near main.py)
import os

TOKEN = os.getenv("WHO_ANONIM_TOKEN", "8134649307:AAH3k13igSnG9t6lGYYTvu7e2D4RiKaCXMI")
ADMINS = [7967404620]  # list of ints, add more admins as needed
BOT_NAME = os.getenv("@Who_Anonim_Bot", "Who_Anonim_Bot")
DB_PATH = os.getenv("WHO_ANONIM_DB", "anon_bot.db")
