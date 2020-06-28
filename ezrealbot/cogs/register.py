import discord

from ezrealbot.cogs import BaseCommand


class Register(BaseCommand):
    """
    """

    def __init__(self):
        description = "Add a new user to the database, check the user to confirm his summoner's info"
        params = {"pseudo": "MANDATORY", "region": "MANDATORY"}
        super().__init__(description, params)

    async def handle(self, params, message, client):

        await message.channel.send("Bonjour!")