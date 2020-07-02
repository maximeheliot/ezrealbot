import sys

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

from ezrealbot import settings
from ezrealbot.events import BaseEvent
from ezrealbot.utils import get_session

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
from models import Guild

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

        self.remove_command('help')
        self.ezreal_session = get_session()

        from ezrealbot.cogs.base_cog import BaseCog
        from ezrealbot.cogs.member_cog import MemberCog

        self.add_cog(BaseCog(self))
        self.add_cog(MemberCog(self))

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

        print("Check for guilds registration...")
        registration = 0
        for guild in self.guilds:
            check_guild = self.ezreal_session.query(Guild).filter(Guild.discord_id == guild.id).one_or_none()
            if not check_guild:
                new_guild = Guild(discord_id=guild.id)
                self.ezreal_session.add(new_guild)
                self.ezreal_session.commit()
                registration += 1

        print(f'Servers registered: {len(self.guilds)}')
        print(f'New server(s): {registration}')
