import discord
import random
from discord.ext import commands

class Emoji:
    def __init__(self, ctx):
        self.bot = bot
        
emojis = ["<:AWOOOKEN:279557451513200641>",
          "<:FeelsBanMan:260505104396845056>"]

    @commands.command()
    async def emoji(self):
        """Posts a random emoji!"""
        await self.bot.say(random.choice(emojis))
        
def setup(bot):
    n = Emoji(bot)
    bot.add_cog(n)
