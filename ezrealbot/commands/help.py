import discord

from ezrealbot.commands.base_command import BaseCommand


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Help(BaseCommand):
    """
        **Search for the command and returns his documentation.**

        You will want to use this function in any place you would usually know for precise information about a command.

```py
@param command: The command you\'re looking for information
@return message: The command information
```
        **Example**

        > **!help** *help*

        > **!help** *users*

        **Note**
        You may want to use this function without parameter to see the list of commands available.

        > **!help**
    """

    def __init__(self):
        description = "Display a help message regarding the command you're looking for"
        params = {"command": "OPTIONAL"}
        super().__init__(description, params)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        embed = discord.Embed(title="**Ezreal Help**", color=0x00ff00)
        discord.Embed()

        if len(params) != 0:
            cmd = COMMAND_HANDLERS[params[0]]
            embed.add_field(name=cmd.description.split(":")[0], value=cmd.__doc__)
        else:
            # Displays all descriptions, sorted alphabetically by command name
            for cmd in sorted(COMMAND_HANDLERS.items()):
                description = cmd[1].description.split(":")
                embed.add_field(name=description[0], value=description[1], inline=False)

        await message.channel.send(embed=embed)
