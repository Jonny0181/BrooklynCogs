import discord

class Joinmsg:
    """docstring for join message."""
    def __init__(self, bot):
        self.bot = bot

    async def on_server_join(self, server):
        servers = len(self.bot.servers)
        users = len([e.name for e in self.bot.get_all_members()])
        e=discord.Embed(description="Thank for another server!\n\nFor and bugs that you need to report join [here](https://discord.gg/fmuvSX9)!\nFor all of my commands you may type `b!commands`!\nAgain I want to say thank you for another server!\nPlease enjoy Brooklyn and have a good time! <3", colour=discord.Colour.blue())
        e.set_author(name="Brooklyn", icon_url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
        e.set_thumbnail(url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
        await self.bot.send_message(server, embed=e)

def setup(bot):
    n = Joinmsg(bot)
    bot.add_cog(n)
