from os import listdir
from os.path import dirname, basename

# Automatically import every class inside the commands package. Magic! :D
from .base_command import BaseCommand
from .help import Help
from .version import Version