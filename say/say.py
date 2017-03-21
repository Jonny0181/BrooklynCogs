import discord
from discord.ext import commands


class Say:
    """Makes the bot say things"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def say(self, ctx, *, text: str):
        """Says Something as the bot."""
        await self.bot.say(str(text))


def setup(bot):
    bot.add_cog(Say(bot))
