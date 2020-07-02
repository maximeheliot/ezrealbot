import asyncio
from datetime import datetime
from typing import Tuple

import discord
from discord.ext import commands
from ezreal.core import query

from ezrealbot import EzrealBot
from models import Member
from discord.utils import get


class MemberCog(commands.Cog, name='Base'):
    def __init__(self, bot: EzrealBot):
        """
        :param bot: the bot to attach the cog to
        """
        self.bot = bot
        self._last_member = None

    @commands.command(description="Add a new user to the database, check the user to confirm his summoner's info.")
    async def register(self, ctx, region: str = '', *, pseudo: str = ''):
        """
            **Search for your summoner profile and add it in the bot member's list.**

            You will want to use this function to allow the bot to collect your game statistics and get access to member-exclusive features.

    ```py
    @param ctx: Application intern parameter for discord action service
    @param pseudo: Your League of Legends summoner name
    @param region: Your League of Legends region ['EUW', 'NA', ...]
    @return message: The summoner checking information
    ```
            **Example**

            > **ez!register EUW Kassout**
        """
        member = ctx.bot.ezreal_session.query(Member)\
            .filter(Member.guild_id == ctx.guild.id, Member.discord_id == ctx.author.id).one_or_none()
        if member is not None:
            await ctx.send("You're already a member! please use ***ez!show*** to see your summoner info or "
                           "***ez!modify*** to change it.")
            return
        summoner = query.read_summoner_info(name=pseudo, region=region)

        embed = discord.Embed(title="**" + summoner.name + "#" + summoner.region + "**", color=0x00ff00)
        embed.add_field(name="level", value=summoner.level)
        self.add_embed_rank_emoji(summoner, embed)
        embed.set_image(url=summoner.profile_icon_url)
        embed.set_footer(text="Can you confirm it's you?")

        response = await ctx.send(embed=embed)

        return_value, accepting_players = await self.checkmark_validation(response, ctx.author.id, timeout=5 * 60)

        if return_value:
            member = Member(discord_id=ctx.author.id, region=summoner.region, summoner_id=summoner.id,
                            guild_id=ctx.guild.id, registration_date=datetime.now())
            ctx.bot.ezreal_session.add(member)
            ctx.bot.ezreal_session.commit()

            await ctx.send("Welcome on board!")

    @commands.command(description="Display the member information and his summoner profile.")
    async def show(self, ctx):
        """
            **Return the lastest member information and his related summoner profile.**

            You will want to use this function to remember your member information and to witch summoner account it is linked.

    ```py
    @param ctx: Application intern parameter for discord action service
    @return message: The member information
    ```
            **Example**

            > **ez!show**
        """
        member = ctx.bot.ezreal_session.query(Member)\
            .filter(Member.guild_id == ctx.guild.id, Member.discord_id == ctx.author.id).one_or_none()
        if member is None:
            await ctx.send("You're not already a member! Please use ***ez!register*** to become one!")
            return

        summoner = query.read_summoner_info(region=member.region, id=member.summoner_id)

        embed = discord.Embed(title="**" + ctx.author.name + "#" + ctx.author.discriminator + "**", color=0x00ff00)
        embed.add_field(name="member since", value=member.registration_date.date(), inline=False)
        embed.add_field(name="summoner name", value=summoner.name, inline=False)
        embed.add_field(name="region", value=summoner.region)
        embed.add_field(name="level", value=summoner.level)
        self.add_embed_rank_emoji(summoner, embed)
        embed.set_thumbnail(url=summoner.profile_icon_url)

        await ctx.send(embed=embed)

    async def checkmark_validation(self, message: discord.Message, validating_member: int, timeout=120.0) \
            -> Tuple[bool, int]:
        """
        Implements a checkmark validation on the chosen message.
        Returns True if validation_threshold members in validating_members pressed '✅' before the timeout.
        """
        await message.add_reaction("✅")
        await message.add_reaction("❎")

        def check(received_reaction: discord.Reaction, sending_user: discord.User):
            # This check is simply used to see if a player in the game responded to the message.
            # Queue logic is handled below
            return (received_reaction.message.id == message.id
                    and sending_user.id == validating_member
                    and str(received_reaction.emoji) in ["✅", "❎"])

        try:
            while True:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout, check=check)

                if str(reaction.emoji) == "✅":
                    return True, validating_member

                elif str(reaction.emoji) == "❎":
                    break

        # We get there if no player accepted in the last two minutes
        except asyncio.TimeoutError:
            pass

        # This handles both timeout and queue refusal
        return False, validating_member

    def add_embed_rank_emoji(self, summoner, embed: discord.Embed):
        for emoji in self.bot.emojis:
            if summoner.rank.split(" ")[0].lower() in emoji.name:
                embed.add_field(name="rank", value=f"{emoji} " + summoner.rank)
                break
            elif summoner.rank == "Unranked":
                embed.add_field(name="rank", value=summoner.rank)
                break

    @commands.command(description="Replace the actual linked summoner profile to the new one passed in parameter.")
    async def update(self, ctx, region: str = '', *, pseudo: str = ''):
        """
            **Search for summoner profile with input parameters and check member for his approbation to replaced it by his old one.**

            You will want to use this function to remember your member information and to witch summoner account it is linked.

    ```py
    @param ctx: Application intern parameter for discord action service
    @param pseudo: Your League of Legends summoner name
    @param region: Your League of Legends region ['EUW', 'NA', ...]
    @return message: The summoner checking information
    ```
            **Example**

            > **ez!update EUW Kassout**
        """
        member = ctx.bot.ezreal_session.query(Member)\
            .filter(Member.guild_id == ctx.guild.id, Member.discord_id == ctx.author.id)
        if member.one_or_none() is None:
            await ctx.send("You're not already a member! Please use ***ez!register*** to become one!")
            return
        summoner = query.read_summoner_info(name=pseudo, region=region)

        if summoner.id == member.one_or_none().summoner_id and summoner.region == member.one_or_none().region:
            await ctx.send("This summoner profile is already the one defined as yours. "
                           "Please use ***ez!show*** to consult your actual profile.")
            return

        embed = discord.Embed(title="**" + summoner.name + "#" + summoner.region + "**", color=0x00ff00)
        embed.add_field(name="level", value=summoner.level)
        self.add_embed_rank_emoji(summoner, embed)
        embed.set_image(url=summoner.profile_icon_url)
        embed.set_footer(text="Can you confirm you want to use this summoner profile from now on?\n"
                              "Be careful, this modification will also erase all previous stats captures "
                              "and computations and wont be retrievable in any ways.")

        response = await ctx.send(embed=embed)

        return_value, accepting_players = await self.checkmark_validation(response, ctx.author.id, timeout=5 * 60)

        if return_value:
            member.update({Member.summoner_id: summoner.id, Member.region: summoner.region})

            await ctx.send("Update done!")

    @commands.command(description="Erase all current information of the user in the Database.")
    async def delete(self, ctx):
        """
            **Erase all the different information the bot host about the user to unregister him.**

            You will want to use this function to unregister yourself from the bot application.

    ```py
    @param ctx: Application intern parameter for discord action service
    @return message: Asking user confirmation
    ```
            **Example**

            > **ez!delete**
        """
        member = ctx.bot.ezreal_session.query(Member)\
            .filter(Member.guild_id == ctx.guild.id, Member.discord_id == ctx.author.id).one_or_none()
        if member is None:
            await ctx.send("You're not a member! Sorry but science still don't know how to erase the void.")
            return

        response = await ctx.send("Are you sure? :(")

        return_value, accepting_players = await self.checkmark_validation(response, ctx.author.id, timeout=5 * 60)

        if return_value:
            ctx.bot.ezreal_session.delete(member)
            ctx.bot.ezreal_session.commit()
            await ctx.send("See you soon!")

    @commands.command(description="Display all current registered users of the server.")
    async def members(self, ctx):
        """
            **Display the list of current registered users of the server.**

            You will want to use this function to resume who are the registered members of your server.

    ```py
    @param ctx: Application intern parameter for discord action service
    @return message: List of members and information resume.
    ```
            **Example**

            > **ez!members**
        """
        members = ctx.bot.ezreal_session.query(Member)\
            .filter(Member.guild_id == ctx.guild.id).all()
        if not members:
            await ctx.send("Their is no members in your server. :'(")
            return

        embed = discord.Embed(title=f'**EzrealBot {ctx.guild.name} community**', color=0x00ff00)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        for member in members:
            user = get(ctx.guild.members, id=member.discord_id)
            summoner = query.read_summoner_info(id=member.summoner_id, region=member.region)
            embed.add_field(name=user.name, value=f'{summoner.name}#{summoner.region}\t{summoner.rank}')

        await ctx.send(embed=embed)
