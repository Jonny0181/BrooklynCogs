import os
import discord
import asyncio
from cogs.utils import checks
from discord.ext import commands
from random import choice, randint
from cogs.utils.dataIO import fileIO, dataIO

settings = {"Channels" : [], "Users" : [], "Roles" : []}

class Ignore:
    def __init__(self, bot):
        self.bot = bot
        self.load = "data/ignore/ignore_list.json"
		
    @commands.group(pass_context=True, name="ignore")
    async def _ignore(self, ctx):
        """Ignore a channel, user and or role for your server."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_ignore.command(pass_context=True)
    async def configure(self, ctx):
        """Configure ignoring for your server."""
        server = ctx.message.server
        db = fileIO(self.load, "load")
        if server.id in db:
            db[server.id] = settings
            fileIO(self.load, "save", db)
            await self.bot.say(":x: Your server is already configured! Please add some channels, users, or roles you would like to ignore!")
            return
        if server.id not in db:
            db[server.id] = settings
            fileIO(self.load, "save", db)
            await self.bot.say("Configured server! You may not ignore channels, users and roles!")
            return

    @_ignore.command(pass_context=True)
    async def channel(self, ctx, *, channel : discord.Channel):
        """Ignore a channel."""
        server = ctx.message.server
        if channel.id not in self.ignore_lists[server.id]["Channels"]:
            self.load[server.id]["Channels"].append(channel.id)
            dataIO.save_json("data/ignore/ignore_list.json", self.load)
            await self.bot.say("Channel added to ignore list.")
        else:
            await self.bot.say("Channel already in ignore list.")

    @_ignore.command(pass_context=True)
    async def role(self, ctx, *, role : discord.Role):
        """Ignore a role."""
        server = ctx.message.server
        if role.id not in self.load[server.id]["Roles"]:
            self.load[server.id]["Roles"].append(role.id)
            dataIO.save_json("data/ignore/ignore_list.json", self.load)
            await self.bot.say("Role added to ignore list.")
        else:
            await self.bot.say("This role is already in the ignore list.")

    @_ignore.command(pass_context=True)
    async def user(self, ctx, *, user : discord.Member):
        """Ignore a user."""
        server = ctx.message.server
        if user.id not in self.load[server.id]["Users"]:
            self.load[server.id]["Users"].append(user.id)
            dataIO.save_json("data/ignore/ignore_list.json", self.load)
            await self.bot.say("User added to the ignore list.")
        else:
            await self.bot.say("This user is already in the ignore list.")

def check_folder():
    if not os.path.exists('data/ignore'):
        print('Creating data/ignore folder...')
        os.makedirs('data/ignore')


def check_file():
    f = 'data/ignore/ignore_list.json'
    if not fileIO(f, 'check'):
        print('Creating default settings.json...')
        fileIO(f, 'save', {})

def setup(bot):
    check_folder()
    check_file()
    n = Ignore(bot)
    bot.add_cog(n)
