import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import settings


class Updates:
    """Ask for a role and you shall receive."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def updates(self, ctx):
        """Audio settings."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @updates.command(no_pm=True, pass_context=True)
    async def enable(self, ctx, rolename: str="Updates", user: discord.Member=None):
        """Enables Brooklyn update notifications"""
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  ctx.message.server.roles)
        if user is None:
            user = author

        if role is None:
            await self.bot.say('Something went wrong.  The Updates role cannot be found.')
            return

        if not channel.permissions_for(server.me).manage_roles:
            await self.bot.say('I don\'t have manage_roles permissions.')
            return

        await self.bot.add_roles(user, role)
        await self.bot.say('Added you to the updates feed.'.format(role.name, user.name))

    @updates.command(no_pm=True, pass_context=True)
    async def disable(self, ctx, rolename: str="Updates", user: discord.Member=None):
        """Disabled Brooklyn update notifications."""
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  ctx.message.server.roles)
        if user is None:
            user = author

        if role is None:
            await self.bot.say('Something went wrong.  The Updates role cannot be found.')
            return

        if not channel.permissions_for(server.me).manage_roles:
            await self.bot.say('I don\'t have manage_roles permissions.')
            return

        await self.bot.remove_roles(user, role)
        await self.bot.say('Removed you from the updates feed.')

def setup(bot):
    bot.add_cog(Updates(bot))


