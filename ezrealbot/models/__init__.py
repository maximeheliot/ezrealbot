from os import listdir
from os.path import dirname, basename
from models.sqlite.sqlite_utils import initialize_sql

# Automatically import every class inside the cogs package. Magic! :D
from .Guild import Guild

initialize_sql()