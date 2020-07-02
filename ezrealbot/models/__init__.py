from os import listdir
from os.path import dirname, basename
# Automatically import every class inside the cogs package. Magic! :D
from .guild import Guild
from .member import Member

from ezrealbot.utils.sqlite_utils import initialize_sql

initialize_sql()