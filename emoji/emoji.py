import discord
import random
from discord.ext import commands


emojis = ["<:AWOOOKEN:279557451513200641>",
          "<:FeelsBanMan:260505104396845056>"]

class Emoji:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def emoji(self, ctx):
        """Posts a random emoji!"""
        author = ctx.message.author
        await self.bot.say(embed=discord.Embed(description=random.choice(emojis), colour=author.colour))
        
def setup(bot):
    n = Emoji(bot)
    bot.add_cog(n)
