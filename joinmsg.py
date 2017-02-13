import discord

class Joinmsg:
    """docstring for join message."""
    def __init__(self, bot):
        self.bot = bot

    async def on_server_join(self, server):
        await self.bot.send_message(server, """**Hi! My name is Brooklyn! :wave: 
I was made to fill your discord with music and joy!
My command affix is `b!`, for all my  commands do `b!help`!
Well, that's it! I hope you enjoy me in your server!***""")

def setup(bot):
    n = Joinmsg(bot)
    bot.add_cog(n)
