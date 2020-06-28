import os

from ezrealbot.utils import get_discord_token

# The prefix that will be used to parse cogs.
# It doesn't have to be a single character!
COMMAND_PREFIX = "ez!"

# The bot token. Keep this secret!
BOT_TOKEN = get_discord_token()

# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "help"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))