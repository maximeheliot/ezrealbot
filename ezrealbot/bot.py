import sys

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

from ezrealbot import settings
from ezrealbot.events import BaseEvent
from ezrealbot.utils import get_session, message_handler

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


class EzrealBot(commands.Bot):

    def __init__(self):
        # Initialize the client
        print("Starting up...")

        super().__init__(settings.COMMAND_PREFIX)
        self.discord_token = settings.BOT_TOKEN

        self.ezreal_session = get_session()

    def run(self, *args, **kwargs):
        super().run(self.discord_token, *args, **kwargs)

    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag
    async def on_ready(self):
        if this.running:
            return

        this.running = True

        # Set the playing status
        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await self.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print(f'{self.user.name} logged in!', flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(event.run, 'interval', (self,),
                          minutes=event.interval_minutes)
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)

    # The message handler for both new message and edits
    async def common_handle_message(self, message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(self, cmd_split[0].lower(), cmd_split[1:], message)
            except Exception as e:
                print("Error while handling message", flush=True)
                raise

    async def on_message(self, message):
        await self.common_handle_message(message)

    async def on_message_edit(self, before, after):
        await self.common_handle_message(after)

    async def on_command_error(self, ctx, error):
        # User-facing error
        await ctx.send('`Error: {}`'
                       '\nUse `!help` for commands help. Contact <@124633440078266368> for bugs.'.format(error),
                       delete_after=self.warning_duration)
        raise error
