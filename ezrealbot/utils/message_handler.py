# This, in addition to tweaking __all__ on commands/__init__.py,
# imports all classes inside the commands package.

from ezrealbot import settings
from ezrealbot.commands import BaseCommand


# Register all available commands
def get_command_handlers():
    return {c.__name__.lower(): c()
                    for c in BaseCommand.__subclasses__()}

###############################################################################


async def handle_command(bot, command, args, message):
    # Check whether the command is supported, stop silently if it's not
    # (to prevent unnecesary spam if our bot shares the same command prefix
    # with some other bot)
    if command not in get_command_handlers():
        return

    print(f"{message.author.name}: {settings.COMMAND_PREFIX}{command} "
          + " ".join(args))

    # Retrieve the command
    cmd_obj = get_command_handlers()[command]
    if cmd_obj.params and len(args) < sum(1 for value in cmd_obj.params.values() if value == "MANDATORY"):
        await message.channel.send(message.author.mention + " Insufficient parameters!")
    else:
        await cmd_obj.handle(args, message, bot)