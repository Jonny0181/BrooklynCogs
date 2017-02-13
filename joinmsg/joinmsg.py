import discord

class Joinmsg:
    """docstring for join message."""
    def __init__(self, bot):
        self.bot = bot

    async def on_server_join(self, server):
        servers = len(self.bot.servers)
        users = len([e.name for e in self.bot.get_all_members()])
        e = discord.Embed(description="Hai, my name is Brooklyn! :wave::skin-tone-3:\nI was summed here by an admin.\nIf you need to report any bugs or anything join [here](https://discord.gg/fmuvSX9).\nOr you may use the `b!contact` command.\n\n**My Features:**\n`1)` Music.\n`2)` Moderation.\n`3)` More will come. :eyes:\n\nFor all of my commands please use `b!commands`.\nIf you need any links or anything please use the `b!help` command.\n\nThat's it! Thank you for adding Brooklyn and have a nice day!", colour=discord.Colour.blue())
        e.set_author(name="Brooklyn", icon_url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
        e.set_footer(text="Now in {} servers seeing {} users!".format(server, user))
        e.set_thumbnail(url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
        await self.bot.send_message(server, embed=e)

def setup(bot):
    n = Joinmsg(bot)
    bot.add_cog(n)
