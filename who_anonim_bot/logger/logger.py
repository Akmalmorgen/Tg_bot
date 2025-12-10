# who_anonim_bot/logger/logger.py
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
