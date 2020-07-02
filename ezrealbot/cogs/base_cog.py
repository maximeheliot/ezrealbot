import asyncio
from datetime import datetime
from typing import Tuple

import discord
import requests
from discord.ext import commands

from ezrealbot import settings
from ezrealbot import EzrealBot

import ezreal.utils
import ezreal.core.query as query

from models import Guild, Member


def get_command_name(cmd):
    name = f"**{settings.COMMAND_PREFIX}{cmd.name}**"
    if cmd.params.keys():
        name += " " + " ".join(f"*<{p}>*" for p in cmd.params.keys() if p != 'self' and p != 'ctx')
    return name


class BaseCog(commands.Cog, name='Base'):
    def __init__(self, bot: EzrealBot):
        """
        :param bot: the bot to attach the cog to
        """
        self.bot = bot
        self._last_member = None

    @commands.command(description="Display a help message regarding the command you're looking for.")
    async def help(self, ctx, command: str = ""):
        """
            **Search for the command and returns his documentation.**

            You will want to use this function in any place you would usually know for precise information about a command.

    ```py
    @param ctx: Application intern parameter for discord action service
    @param command: The command you\'re looking for information
    @return message: The command information
    ```
            **Example**

            > **ez!help** *help*

            > **ez!help** *users*

            **Note**
            You may want to use this function without parameter to see the list of cogs available.

            > **ez!help**
        """
        embed = discord.Embed(title="**Ezreal Help**", color=0x00ff00)

        if len(command) != 0:
            for cmd in self.bot.commands:
                if cmd.name == command:
                    embed.add_field(name=get_command_name(cmd), value=cmd.help)
        else:
            # Displays all descriptions, sorted alphabetically by command name
            for cmd in sorted(self.bot.commands, key=lambda x: x.name):
                embed.add_field(name=get_command_name(cmd), value=cmd.description, inline=False)

        await ctx.send(embed=embed)

    @commands.command(description="Display the lastest application version number and a *what's new* list of information.")
    async def version(self, ctx):
        """
            **Return the lastest application version number and a list of the latest features it includes.**

            You will want to use this function to know about what's new in the latest version of the application.

    ```py
    @param ctx: Application intern parameter for discord action service
    @return message: The version information
    ```
            **Example**

            > **ez!help**
        """
        r = None

        try:
            r = requests.get('https://api.github.com/repos/maximeheliot/ezrealbot/releases/latest').json()
        except ConnectionError as err:
            await ctx.send("ConnectionError: ", err)
            return
        except requests.HTTPError as err:
            await ctx.send("HTTPError: ", err)
            return
        except requests.Timeout as err:
            await ctx.send("Timeout: ", err)
            return

        embed = discord.Embed(title="**Ezreal Version " + r['tag_name'] + " **", color=0xff0000, description=r['body'])

        await ctx.send(embed=embed)

