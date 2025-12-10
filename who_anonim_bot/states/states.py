# who_anonim_bot/states/states.py

# простая константа-реализация, можно и enum
MAIN_MENU = "MAIN_MENU"

# Roulette states
CHOOSING_GENDER = "CHOOSING_GENDER"
SEARCHING_ROULETTE = "SEARCHING_ROULETTE"
IN_ROULETTE = "IN_ROULETTE"

# Link anonymous states
MY_LINK = "MY_LINK"
ANON_CONNECTED_PREFIX = "ANON_CONNECTED:"  # will be followed by session id

# Admin states
ADMIN_PANEL = "ADMIN_PANEL"
BROADCAST = "BROADCAST"
BAN_USER = "BAN_USER"
UNBAN_USER = "UNBAN_USER"

# Reply mode for link owner
WAITING_REPLY_PREFIX = "WAITING_REPLY:"  # WAITING_REPLY:{session_id}
