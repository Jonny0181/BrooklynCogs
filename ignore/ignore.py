import os
import discord
import asyncio
from cogs.utils import checks
from discord.ext import commands
from random import choice, randint
from cogs.utils.dataIO import fileIO, dataIO

class Ignore:
    def __init__(self, bot):
        self.bot = bot
        self.load = dataIO.load_json("data/mod/ignore_list.json")
		
    @commands.group(pass_context=True, name="ignore")
    async def _ignore(self, ctx):
        """Ignore a channel, user and or role for your server."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_ignore.command(pass_context=True)
    async def channel(self, ctx, channel : discord.Channel):
        """Ignore a channel."""
        server = ctx.message.server
        if channel.id not in self.load["Channels"]:
            self.load["Channels"].append(channel.id)
            dataIO.save_json("data/mod/ignore_list.json", self.load)
            await self.bot.say("Channel added to ignore list.")
        else:
            await self.bot.say("Channel already in ignore list.")

    @_ignore.command(pass_context=True)
    async def role(self, ctx, role : discord.Role):
        """Ignore a role."""
        server = ctx.message.server
        if role.id not in self.load["Roles"]:
            self.load["Roles"].append(role.id)
            dataIO.save_json("data/mod/ignore_list.json", self.load)
            await self.bot.say("Role added to ignore list.")
        else:
            await self.bot.say("This role is already in the ignore list.")

    @_ignore.command(pass_context=True)
    async def user(self, ctx, user : discord.Member):
        """Ignore a user."""
        server = ctx.message.server
        if user.id not in self.load["Users"]:
            self.load["Users"].append(user.id)
            dataIO.save_json("data/mod/ignore_list.json", self.load)
            await self.bot.say("User added to the ignore list.")
        else:
            await self.bot.say("This user is already in the ignore list.")

    @commands.group(pass_context=True, name="unignore")
    async def _unignore(self, ctx):
        """Ignore a channel, user and or role for your server."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_unignore.command(pass_context=True, name="channel")
    async def _channel(self, ctx, channel : discord.Channel):
        """Ungnore a channel."""
        server = ctx.message.server
        if channel.id in self.load["Channels"]:
            self.load["Channels"].remove(channel.id)
            dataIO.save_json("data/mod/ignore_list.json", self.load)
            await self.bot.say("Channel removed from ignore list.")
        else:
            await self.bot.say("Channel not in ignore list.")

    @_unignore.command(pass_context=True, name="role")
    async def _role(self, ctx, role : discord.Role):
        """Unignore a role."""
        server = ctx.message.server
        if role.id in self.load["Roles"]:
            self.load["Roles"].remove(role.id)
            dataIO.save_json("data/mod/ignore_list.json", self.load)
            await self.bot.say("Role removed from ignore list.")
        else:
            await self.bot.say("This role is not in the ignore list.")

    @_unignore.command(pass_context=True, name="user")
    async def _user(self, ctx, user : discord.Member):
        """Unignore a user."""
        server = ctx.message.server
        if user.id in self.load["Users"]:
            self.load["Users"].remove(user.id)
            dataIO.save_json("data/mod/ignore_list.json", self.load)
            await self.bot.say("User removed from the ignore list.")
        else:
            await self.bot.say("This user is not in the ignore list.")

def check_folder():
    if not os.path.exists('data/mod'):
        print('Creating data/mod folder...')
        os.makedirs('data/mod')


def check_file():
    f = 'data/mod/ignore_list.json'
    if not fileIO(f, 'check'):
        print('Creating default settings.json...')
        fileIO(f, 'save', {})

def setup(bot):
    check_folder()
    check_file()
    n = Ignore(bot)
    bot.add_cog(n)
