import discord
from discord.ext import commands

timef = datetime.datetime.now().strftime("%A, %B %-d %Y at %-I:%M%p").replace("PM", "pm").replace("AM", "am")

class EmbedSay:
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command(pass_context=True)
    async def embedsay(self, ctx, *, text: str)):
        """Have Brooklyn say a message but in embed!"""
        author = ctx.message.author
        e = discord.Embed(description=str(text))
        e.set_author(name=author.name, icon_url=author.avatar_url)
        e.set_thumbnail(url=author.avatar_url)
        e.set_footer(text=timef)
        await self.bot.say(embed=e)
        
def setup(bot):
    n = EmbedSay(bot)
    bot.add_cog(n)
