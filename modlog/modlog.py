from discord.ext import commands
from cogs.utils import checks
import datetime
from cogs.utils.dataIO import fileIO
import discord
import asyncio
import os
from random import choice, randint

inv_settings = {"Channel": None, "toggleedit": False, "toggledelete": False, "toggleuser": False, "toggleroles": False,
                "togglevoice": False,
                "toggleban": False, "togglejoin": False, "toggleleave": False}


class invitemirror:
    def __init__(self, bot):
        self.bot = bot
        self.direct = "data/modlogset/settings.json"

    @checks.admin_or_permissions(administrator=True)
    @commands.group(name='modlogtoggle', pass_context=True, no_pm=True)
    async def modlogtoggles(self, ctx):
        """toggle which server activity to log"""
        if ctx.invoked_subcommand is None:
            db = fileIO(self.direct, "load")
            server = ctx.message.server
            await self.bot.send_cmd_help(ctx)
            try:
                e = discord.Embed(title="Setting for {}".format(server.name), colour=discord.Colour.blue())
                e.add_field(name="Delete", value=str(db[ctx.message.server.id]['toggledelete']))
                e.add_field(name="Edit", value=str(db[ctx.message.server.id]['toggleedit']))
                e.add_field(name="Roles", value=str(db[ctx.message.server.id]['toggleroles']))
                e.add_field(name="Voice", value=str(db[ctx.message.server.id]['togglevoice']))
                e.add_field(name="Ban", value=str(db[ctx.message.server.id]['toggleban']))
                e.add_field(name="Join", value=str(db[ctx.message.server.id]['togglejoin']))
                e.add_field(name="Leave", value=str(db[ctx.message.server.id]['toggleleave']))
                e.set_thumbnail(url=server.icon_url)
        await self.bot.say(embed=e)
            except KeyError:
                return

    @checks.admin_or_permissions(administrator=True)
    @commands.group(pass_context=True, name='modlogset', no_pm=True)
    async def modlogset(self, ctx):
        """Change modlog settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @modlogset.command(pass_context=True, name='channel', no_pm=True)
    async def channel(self, ctx):
        """Set the channel to send notifications too"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if ctx.message.server.me.permissions_in(ctx.message.channel).send_messages:
            if server.id in db:
                db[server.id]['Channel'] = ctx.message.channel.id
                fileIO(self.direct, "save", db)
                await self.bot.say("Channel changed.")
                return
            if not server.id in db:
                db[server.id] = inv_settings
                db[server.id]["Channel"] = ctx.message.channel.id
                fileIO(self.direct, "save", db)
                await self.bot.say("I will now send toggled modlog notifications here")
        else:
            return

    @modlogset.command(name='disable', pass_context=True, no_pm=True)
    async def disable(self, ctx):
        """disables the modlog"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            await self.bot.say("Server not found, use modlogset to set a channnel")
            return
        del db[server.id]
        fileIO(self.direct, "save", db)
        await self.bot.say("I will no longer send modlog notifications here")

    @modlogtoggles.command(name='edit', pass_context=True, no_pm=True)
    async def edit(self, ctx):
        """toggle notifications when a member edits theyre message"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleedit"] == False:
            db[server.id]["toggleedit"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Edit messages enabled")
        elif db[server.id]["toggleedit"] == True:
            db[server.id]["toggleedit"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Edit messages disabled")
            
    @modlogtoggles.command(name='join', pass_context=True, no_pm=True)
    async def join(self, ctx):
        """toggles notofications when a member joins the server."""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["togglejoin"] == False:
            db[server.id]["togglejoin"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Enabled join logs.")
        elif db[server.id]['togglejoin'] == True:
            db[server.id]['togglejoin'] = False
            fileIO(self.direct, 'save', db)
            await self.bot.say("Disabled join logs.")
            
    @modlogtoggles.command(name='leave', pass_context=True, no_pm=True)
    async def leave(self, ctx):
        """toggles notofications when a member joins the server."""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleleave"] == False:
            db[server.id]["toggleleave"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Enabled leave logs.")
        elif db[server.id]['toggleleave'] == True:
            db[server.id]['toggleleave'] = False
            fileIO(self.direct, 'save', db)
            await self.bot.say("Disabled leave logs.")

    @modlogtoggles.command(name='delete', pass_context=True, no_pm=True)
    async def delete(self, ctx):
        """toggle notifications when a member delete theyre message"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggledelete"] == False:
            db[server.id]["toggledelete"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Delete messages enabled")
        elif db[server.id]["toggledelete"] == True:
            db[server.id]["toggledelete"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Delete messages disabled")

    @modlogtoggles.command(name='user', pass_context=True, no_pm=True)
    async def user(self, ctx):
        """toggle notifications when a user changes his profile"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleuser"] == False:
            db[server.id]["toggleuser"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("User messages enabled")
        elif db[server.id]["toggleuser"] == True:
            db[server.id]["toggleuser"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("User messages disabled")

    @modlogtoggles.command(name='roles', pass_context=True, no_pm=True)
    async def roles(self, ctx):
        """toggle notifications when roles change"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleroles"] == False:
            db[server.id]["toggleroles"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Role messages enabled")
        elif db[server.id]["toggleroles"] == True:
            db[server.id]["toggleroles"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Role messages disabled")

    @modlogtoggles.command(name='voice', pass_context=True, no_pm=True)
    async def voice(self, ctx):
        """toggle notifications when voice status change"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["togglevoice"] == False:
            db[server.id]["togglevoice"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Voice messages enabled")
        elif db[server.id]["togglevoice"] == True:
            db[server.id]["togglevoice"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Voice messages disabled")

    @modlogtoggles.command(name='ban', pass_context=True, no_pm=True)
    async def ban(self, ctx):
        """toggle notifications when a user is banned"""
        server = ctx.message.server
        db = fileIO(self.direct, "load")
        if db[server.id]["toggleban"] == False:
            db[server.id]["toggleban"] = True
            fileIO(self.direct, "save", db)
            await self.bot.say("Ban messages enabled")
        elif db[server.id]["toggleban"] == True:
            db[server.id]["toggleban"] = False
            fileIO(self.direct, "save", db)
            await self.bot.say("Ban messages disabled")

    async def on_message_delete(self, message):
        server = message.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggledelete'] == False:
            return
        if message.author is message.author.bot:
            pass
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        msg = ":pencil: `{}` **Channel**: {} **{}'s** message has been deleted. Content: {}".format(time.strftime(fmt), message.channel.mention, message.author, message.content)
        await self.bot.send_message(server.get_channel(channel),
                                    msg)
        
    async def on_member_join(self, member):
        server = member.server
        db = fileIO(self.direct, 'load')
        if not server.id in db:
            return
        if db[server.id]['togglejoin'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        users = len([e.name for e in server.members])
        msg = ":white_check_mark: `{}` **{}** join the server. Total users: {}.".format(time.strftime(fmt), member.name, users)
        await self.bot.send_message(server.get_channel(channel), msg)
        
    async def on_member_remove(self, member):
        server = member.server
        db = fileIO(self.direct, 'load')
        if not server.id in db:
            return
        if db[server.id]['toggleleave'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = "%H:%M:%S"
        users = len([e.name for e in server.members])
        msg = ":x: `{}` **{}** has left the server or was kicked. Total members {}.".format(time.strftime(fmt), member.name, users)

    async def on_message_edit(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleedit'] == False:
            return
        if before.content == after.content:
            return
        if before.author.bot:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        msg = ":pencil: `{}` **Channel**: {} **{}'s** message has been edited.\nBefore: {}\nAfter: {}".format(time.strftime(fmt), before.channel.mention, before.author, before.content, after.content)
        await self.bot.send_message(server.get_channel(channel),
                                    msg)

    async def on_voice_state_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['togglevoice'] == False:
            return
        if before.bot:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        msg = ":person_with_pouting_face::skin-tone-3: `{}` **{}'s** voice status has updated. **Channel**: {}\n**Local Mute:** {} **Local Deaf:** {} **Server Mute:** {} **Server Deaf:** {}".format(time.strftime(fmt), after.name, after.voice_channel, after.self_mute, after.self_deaf, after.mute, after.deaf)
        await self.bot.send_message(server.get_channel(channel),
                                    msg)

    async def on_member_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleuser'] and db[server.id]['toggleroles'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        if not before.nick == after.nick:
            msg = ":person_with_pouting_face::skin-tone-3: `{}` **{}** changed their nickname from **{}** to **{}**".format(time.strftime(fmt), before.name, before.kick, after.nick)
            await self.bot.send_message(server.get_channel(channel),
                                        msg)

    async def on_member_update(self, before, after):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleuser'] and db[server.id]['toggleroles'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        if not before.roles == after.roles:
            msg = ":person_with_pouting_face::skin-tone-3: `{}` **{}'s** roles have changed. Old: `{}` New: `{}`".format(time.strftime(fmt), before.name, ", ".join([r.name for r in before.roles]), ", ".join([r.name for r in after.roles]))
            await self.bot.send_message(server.get_channel(channel),
                                        msg)

    async def on_member_ban(self, member):
        server = before.server
        db = fileIO(self.direct, "load")
        if not server.id in db:
            return
        if db[server.id]['toggleban'] == False:
            return
        channel = db[server.id]["Channel"]
        time = datetime.datetime.now()
        fmt = '%H:%M:%S'
        msg = ":hammer: `{}` {}({}) has been banned!".format(member.name, member.id)
        await self.bot.send_message(server.get_channel(channel),
                                    msg)


def check_folder():
    if not os.path.exists('data/modlogset'):
        print('Creating data/modlogset folder...')
        os.makedirs('data/modlogset')


def check_file():
    f = 'data/modlogset/settings.json'
    if not fileIO(f, 'check'):
        print('Creating default settings.json...')
        fileIO(f, 'save', {})


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(invitemirror(bot))
