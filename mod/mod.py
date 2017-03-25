import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help, settings
from collections import deque, defaultdict
from cogs.utils.chat_formatting import escape_mass_mentions, box, pagify
import os
import time
import copy
import re
import datetime
import unicodedata
from random import randint
from random import choice as randchoice
import logging
import random
import asyncio
from .utils.dataIO import fileIO
try:
    from tabulate import tabulate
except:
    raise Exception('Run "pip install tabulate" in your CMD/Linux Terminal')
log = logging.getLogger('red.punish')
db_data = {"Toggle" : False, "No Invite" : False, "Toggle Blacklist" : False, "Blacklisted": {}}

default_settings = {
    "ban_mention_spam" : False,
    "delete_repeats"   : False,
    "mod-log"          : None
                   }
log = logging.getLogger('red.massmove')

class ModError(Exception):
    pass


class UnauthorizedCaseEdit(ModError):
    pass


class CaseMessageNotFound(ModError):
    pass


class NoModLogChannel(ModError):
    pass


class Mod:
    """Moderation tools."""

    def __init__(self, bot):
        self.bot = bot
        self.whitelist_list = dataIO.load_json("data/mod/whitelist.json")
        self.blacklist_list = dataIO.load_json("data/mod/blacklist.json")
        self.ignore_list = dataIO.load_json("data/mod/ignorelist.json")
        self.filter = dataIO.load_json("data/mod/filter.json")
        self.past_names = dataIO.load_json("data/mod/past_names.json")
        self.past_nicknames = dataIO.load_json("data/mod/past_nicknames.json")
        settings = dataIO.load_json("data/mod/settings.json")
        self.settings = defaultdict(lambda: default_settings.copy(), settings)
        self.cache = defaultdict(lambda: deque(maxlen=3))
        self.cases = dataIO.load_json("data/mod/modlog.json")
        self.last_case = defaultdict(dict)
        self._tmp_banned_cache = []
        perms_cache = dataIO.load_json("data/mod/perms_cache.json")
        self._perms_cache = defaultdict(dict, perms_cache)
        self.link_data = "data/antilink/antilink.json"

    def __unload(self):
        self.task.cancel()
        log.debug('Stopped task')
        
    @commands.group(pass_context = True, no_pm = True)
    async def antilink(self, ctx):
        channel = ctx.message.channel
        server = ctx.message.server
        my = server.me
        data = fileIO(self.link_data, "load")
        if server.id not in data:
            data[server.id] = db_data
            fileIO(self.link_data, "save", data)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @antilink.command(pass_context=True)
    async def status(self, ctx):
        """Shows antilink status."""
        channel = ctx.message.channel
        server = ctx.message.server
        directory = fileIO(self.link_data, "load")
        db = directory[server.id]
        if len(db["Blacklisted"]) != 0:
            words = "- {}".format("\n-".join(["{}".format(x) for x in db["Blacklisted"]]))
        else:
            words = "No Links/Words blacklisted for this server"
            colour = ''.join([randchoice('0123456789ABCDEF') for x in range(6)])
            colour = int(colour, 16)
            status = (str(db["Toggle"]).replace("True", "Enabled")).replace("False", "Disabled")
            e = discord.Embed()
            e.colour = colour
            e.description = "Showing AntiLink Settings For {0}\nDo {1.prefix}help {1.command.qualified_name} for more info".format(server.name, ctx)
            e.set_author(name = "AntiLink Settings")
            e.add_field(name = "AntiLink Status", value = status)
            e.add_field(name = "AntiInvite Enabled", value = db["No Invite"])
            e.add_field(name = "AntiLinks Enabled", value = db["Toggle Blacklist"])
            e.add_field(name = "Blacklisted Words", value = words, inline = False)
            e.set_footer(text = "AntiLink Settings", icon_url = server.icon_url)
            e.timestamp = ctx.message.timestamp
            try:
                await self.bot.send_message(channel, embed = e)
            except discord.Forbidden:
                msg = "```css\nAntiLink Settings for {0.name}.\nDo {1.prefix}help {1.command.qualified_name} for more info\n".format(server, ctx)
                msg += "AntiLink Status : {0}\nAntiInvite Enabled : {1}\nAntilinks Enabled : {2}\nBlacklisted Words: {3}\n```".format(status, db["No Invite"], db["Toggle Blacklist"], words)
                await self.bot.send_message(channel, msg)


    @antilink.command(pass_context = True)
    async def toggle(self, ctx):
        """Enables or Disables the Antilink"""
        server = ctx.message.server
        db = fileIO(self.link_data, "load")
        db[server.id]["Toggle"] = not db[server.id]["Toggle"]
        if db[server.id]["Toggle"] is True:
            msg = "Successfully Enabled the Antilinks System\nNote: I need the \"Manage Messages\" Permission to delete messages"
        else:
            msg = "I have successfully disabled the Antilinks System."
        await self.bot.reply(msg)
        fileIO(self.link_data, "save", db)

    @antilink.command(pass_context = True)
    async def antiinvite(self, ctx):
        """Enables or Disables the Antilink"""
        server = ctx.message.server
        db = fileIO(self.link_data, "load")
        db[server.id]["No Invite"] = not db[server.id]["No Invite"]
        if db[server.id]["No Invite"] is True:
            msg = "Successfully Enabled AntiInvite\nI will delete all invite links from now on\nNote: I need the \"Manage Messages\" Permission to delete messages"
        else:
            msg = "I have successfully disabled antiinvite."
        await self.bot.reply(msg)
        fileIO(self.link_data, "save", db)
        
    @antilink.command(pass_context = True)
    async def links(self, ctx):
        """Enables or Disables the Antilink"""
        server = ctx.message.server
        db = fileIO(self.link_data, "load")
        db[server.id]["Toggle Blacklist"] = not db[server.id]["Toggle Blacklist"]
        if db[server.id]["Toggle Blacklist"] is True:
            msg = "Successfully Enabled Antilinks\nI will delete all blacklisted links/words from now on\nNote: I need the \"Manage Messages\" Permission to delete messages"
        else:
            msg = "I have successfully disabled Antilinks and will not delete blacklisted links/words from now on."
        await self.bot.reply(msg)
        fileIO(self.link_data, "save", db)

    @antilink.command(pass_context = True, name = "addword", aliases = ["addlink"])
    async def _addlinks_(self, ctx, *words : str):
        """Adds word to the blacklist
        Note: You can add mutiple words to the blacklist
        Usage:
        b!antilink adword \"This is taken as a word\" linka linkb linkc
        b!antilink addword linka linkb linkc
        b!ntilink addword \"blacklisted word\""""
        server = ctx.message.server
        data = fileIO(self.link_data, "load")
        if not words:
            await self.bot.reply("Please pass the words/links you want me to blacklist")
            return
        for word in words:
            data[server.id]["Blacklisted"][word] = True
        wordlist = " , ".join(["\"{}\"".format(e) for e in words])
        fmt = "Successfully added these words to the list.\n{}".format(wordlist)
        await self.bot.reply(fmt)
        fileIO(self.link_data, "save", data)

    @antilink.command(pass_context = True, name = "removeword", aliases = ["removelink"])
    async def _removelinks_(self, ctx, *words : str):
        """Adds word to the blacklist
        Note: You can add mutiple words to the blacklist
        Usage:
        b!ntilink add \"This is taken as a word\" linka linkb linkc
        b!antilink add linka linkb linkc
        b!antilink add \"blacklisted word\""""
        server = ctx.message.server
        data = fileIO(self.link_data, "load")
        if not words:
            await self.bot.reply("Please pass the words/links you want me to blacklist")
            return
        in_word = []
        for word in words:
            if word in data[server.id]["Blacklisted"]:
                in_word.append(word)
                del data[server.id]["Blacklisted"][word]
        wordlist = " , ".join(["\"{}\"".format(e) for e in in_word])
        fmt = "Successfully removed these words from the list.\n{}".format(wordlist)
        await self.bot.reply(fmt)
        fileIO(self.link_data, "save", data)

    @commands.command(pass_context=True)
    @commands.cooldown(2, 5, commands.BucketType.server)
    @checks.admin_or_permissions(manage_messages=True)
    async def clean(self, ctx, max_messages:int=None):
        """Removes inputed amount of bot and invoker messages."""
	none = False
	if max_messages is None:
	    none = True
	    max_messages = 20
	if max_messages and max_messages > 1500:
	    await self.bot.say("To many messages for me to search through.")
	    return
	if ctx.message.server.me.permissions_in(ctx.message.channel).manage_messages:
	    prefix = await self.bot.funcs.get_prefix(ctx.message)
	    prefix = prefix[0][0]
	    check = lambda m: m.author == self.bot.user or m.content.startswith(prefix)
	    deleted = await self.bot.purge_from(ctx.message.channel, limit=max_messages, check=check, after=datetime.datetime.now() - datetime.timedelta(minutes=5) if none else None)
	    self.bot.pruned_messages.append(deleted)
	    count = len(deleted)
	else:
	    count = 0
	    async for message in self.bot.logs_from(ctx.message.channel, limit=max_messages+1, after=datetime.datetime.now() - datetime.timedelta(minutes=5) if none else None):
                if message.author == self.bot.user:
		    self.bot.pruned_messages.append(message)
		    asyncio.ensure_future(self.bot.delete_message(message))
		    await asyncio.sleep(0.21)
		    count += 1
	x = await self.bot.send_message(ctx.message.channel, "Removed `{0}` messages out of `{1}` searched messages".format(count, max_messages))
	await asyncio.sleep(10)
	try:
	    self.bot.pruned_messages.append(ctx.message)
	    await self.bot.delete_message(ctx.message)
	except:
	    pass
	await self.bot.delete_message(x)

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def hackban(self, ctx, *, user_id: str):
        """Bans users by ID.
        This method does not require the user to be on the server."""

        server = ctx.message.server.id
        try:
            await self.bot.http.ban(user_id, server)
            await self.bot.say("User banned, was <@{}>.".format(user_id))
        except:
            await self.bot.say("Failed to ban. Either `Lacking Permissions` or `User cannot be found`.")
            
    @commands.command(pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def unban(self, ctx, *, user_id: str):
        """Unbans users by ID."""

        server = ctx.message.server.id
        try:
            await self.bot.http.unban(user_id, server)
            await self.bot.say("User unbanned, was <@{}>.".format(user_id))
        except:
            await self.bot.say("Failed to unban. Either `Lacking Permissions` or `User cannot be found`.")

    @commands.group(pass_context=True, hidden=True)
    @checks.is_owner()
    async def blacklist(self, ctx):
        """Bans user from using the bot"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @blacklist.command(name="add")
    async def _blacklist_add(self, user: discord.Member):
        """Adds user to bot's blacklist"""
        if user.id not in self.blacklist_list:
            self.blacklist_list.append(user.id)
            dataIO.save_json("data/mod/blacklist.json", self.blacklist_list)
            await self.bot.say("User has been added to blacklist.")
        else:
            await self.bot.say("User is already blacklisted.")

    @blacklist.command(name="remove")
    async def _blacklist_remove(self, user: discord.Member):
        """Removes user from bot's blacklist"""
        if user.id in self.blacklist_list:
            self.blacklist_list.remove(user.id)
            dataIO.save_json("data/mod/blacklist.json", self.blacklist_list)
            await self.bot.say("User has been removed from blacklist.")
        else:
            await self.bot.say("User is not in blacklist.")

    @blacklist.command(name="clear")
    async def _blacklist_clear(self):
        """Clears the blacklist"""
        self.blacklist_list = []
        dataIO.save_json("data/mod/blacklist.json", self.blacklist_list)
        await self.bot.say("Blacklist is now empty.")

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()  # I don't know how permissive this should be yet
    async def whisper(self, ctx, id, *, text):
        author = ctx.message.author

        target = discord.utils.get(self.bot.get_all_members(), id=id)
        if target is None:
            target = self.bot.get_channel(id)
            if target is None:
                target = self.bot.get_server(id)

        prefix = "```diff\n- Message from {}:".format(
            author.name)
        payload = "{}\n\n+ {}```".format(prefix, text)

        try:
            for page in pagify(payload, delims=[" ", "\n"], shorten_by=10):
                await self.bot.send_message(target, page)
        except discord.errors.Forbidden:
            log.debug("Forbidden to send message to {}".format(id))
        except (discord.errors.NotFound, discord.errors.InvalidArgument):
            log.debug("{} not found!".format(id))
        else:
            await self.bot.say("Done.")

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(move_members=True)
    async def massmove(self, ctx, from_channel: discord.Channel, to_channel: discord.Channel):
        """Massmove users to another voice channel.\nExample: r!!massmove Public Music"""
        await self._massmove(ctx, from_channel, to_channel)

    async def _massmove(self, ctx, from_channel, to_channel):
        """Internal function: Massmove users to another voice channel"""
        # check if channels are voice channels. Or moving will be very... interesting...
        type_from = str(from_channel.type)
        type_to = str(to_channel.type)
        if type_from == 'text':
            await self.bot.say('{} is not a valid voice channel'.format(from_channel.name))
            log.debug('SID: {}, from_channel not a voice channel'.format(from_channel.server.id))
        elif type_to == 'text':
            await self.bot.say('{} is not a valid voice channel'.format(to_channel.name))
            log.debug('SID: {}, to_channel not a voice channel'.format(to_channel.server.id))
        else:
            try:
                log.debug('Starting move on SID: {}'.format(from_channel.server.id))
                log.debug('Getting copy of current list to move')
                voice_list = list(from_channel.voice_members)
                for member in voice_list:
                    await self.bot.move_member(member, to_channel)
                    log.debug('Member {} moved to channel {}'.format(member.id, to_channel.id))
                    await asyncio.sleep(0.05)
            except discord.Forbidden:
                await self.bot.say('I have no permission to move members.')
            except discord.HTTPException:
                await self.bot.say('A error occured. Please try again')

    @commands.group(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def modset(self, ctx):
        """Manages server administration settings."""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)
            roles = settings.get_server(server).copy()
            _settings = {**self.settings[server.id], **roles}
            if "delete_delay" not in _settings:
                _settings["delete_delay"] = -1
            msg = ("Admin role: {ADMIN_ROLE}\n"
                   "Mod role: {MOD_ROLE}\n"
                   "Mod-log: {mod-log}\n"
                   "Delete repeats: {delete_repeats}\n"
                   "Ban mention spam: {ban_mention_spam}\n"
                   "Delete delay: {delete_delay}\n"
                   "".format(**_settings))
            await self.bot.say(box(msg))

    @modset.command(name="adminrole", pass_context=True, no_pm=True)
    async def _modset_adminrole(self, ctx, role_name: str):
        """Sets the admin role for this server, case insensitive."""
        server = ctx.message.server
        if server.id not in settings.servers:
            await self.bot.say("Remember to set modrole too.")
        settings.set_server_admin(server, role_name)
        await self.bot.say("Admin role set to '{}'".format(role_name))

    @modset.command(name="modrole", pass_context=True, no_pm=True)
    async def _modset_modrole(self, ctx, role_name: str):
        """Sets the mod role for this server, case insensitive."""
        server = ctx.message.server
        if server.id not in settings.servers:
            await self.bot.say("Remember to set adminrole too.")
        settings.set_server_mod(server, role_name)
        await self.bot.say("Mod role set to '{}'".format(role_name))

    @modset.command(pass_context=True, no_pm=True)
    async def modlog(self, ctx, channel : discord.Channel=None):
        """Sets a channel as mod log

        Leaving the channel parameter empty will deactivate it"""
        server = ctx.message.server
        if channel:
            self.settings[server.id]["mod-log"] = channel.id
            await self.bot.say("Mod events will be sent to {}"
                               "".format(channel.mention))
        else:
            if self.settings[server.id]["mod-log"] is None:
                await send_cmd_help(ctx)
                return
            self.settings[server.id]["mod-log"] = None
            await self.bot.say("Mod log deactivated.")
        dataIO.save_json("data/mod/settings.json", self.settings)

    @modset.command(pass_context=True, no_pm=True)
    async def banmentionspam(self, ctx, max_mentions : int=False):
        """Enables auto ban for messages mentioning X different people

        Accepted values: 5 or superior"""
        server = ctx.message.server
        if max_mentions:
            if max_mentions < 5:
                max_mentions = 5
            self.settings[server.id]["ban_mention_spam"] = max_mentions
            await self.bot.say("Autoban for mention spam enabled. "
                               "Anyone mentioning {} or more different people "
                               "in a single message will be autobanned."
                               "".format(max_mentions))
        else:
            if self.settings[server.id]["ban_mention_spam"] is False:
                await send_cmd_help(ctx)
                return
            self.settings[server.id]["ban_mention_spam"] = False
            await self.bot.say("Autoban for mention spam disabled.")
        dataIO.save_json("data/mod/settings.json", self.settings)

    @modset.command(pass_context=True, no_pm=True)
    async def deleterepeats(self, ctx):
        """Enables auto deletion of repeated messages"""
        server = ctx.message.server
        if not self.settings[server.id]["delete_repeats"]:
            self.settings[server.id]["delete_repeats"] = True
            await self.bot.say("Messages repeated up to 3 times will "
                               "be deleted.")
        else:
            self.settings[server.id]["delete_repeats"] = False
            await self.bot.say("Repeated messages will be ignored.")
        dataIO.save_json("data/mod/settings.json", self.settings)

    @modset.command(pass_context=True, no_pm=True)
    async def resetcases(self, ctx):
        """Resets modlog's cases"""
        server = ctx.message.server
        self.cases[server.id] = {}
        dataIO.save_json("data/mod/modlog.json", self.cases)
        await self.bot.say("Cases have been reset.")

    @modset.command(pass_context=True, no_pm=True)
    async def deletedelay(self, ctx, time: int=None):
        """Sets the delay until the bot removes the command message.
            Must be between -1 and 60.

        A delay of -1 means the bot will not remove the message."""
        server = ctx.message.server
        if time is not None:
            time = min(max(time, -1), 60)  # Enforces the time limits
            self.settings[server.id]["delete_delay"] = time
            if time == -1:
                await self.bot.say("Command deleting disabled.")
            else:
                await self.bot.say("Delete delay set to {}"
                                   " seconds.".format(time))
            dataIO.save_json("data/mod/settings.json", self.settings)
        else:
            try:
                delay = self.settings[server.id]["delete_delay"]
            except KeyError:
                await self.bot.say("Delete delay not yet set up on this"
                                   " server.")
            else:
                if delay != -1:
                    await self.bot.say("Bot will delete command messages after"
                                       " {} seconds. Set this value to -1 to"
                                       " stop deleting messages".format(delay))
                else:
                    await self.bot.say("I will not delete command messages.")

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str=None):
        """Kicks user."""
        author = ctx.message.author
        server = author.server
        try:
            await self.bot.send_message(user, "**You have been kicked from {}.**\n**Reason:**  {}".format(server.name, reason))
            await self.bot.kick(user)
            logger.info("{}({}) kicked {}({})".format(
                author.name, author.id, user.name, user.id))
            await self.new_case(server,
                                action="Kick \N{WOMANS BOOTS}",
                                mod=author,
                                user=user)
            await self.bot.say("Done, I have kicked {} from the server.".format(user.name))
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the perms to kick users in this chat, please give kick perms.")
        except Exception as e:
            print(e)

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str=None):
        """Bans a user from the server."""
        author = ctx.message.author
        server = author.server
        channel = ctx.message.channel
        can_ban = channel.permissions_for(server.me).ban_members
        if can_ban:
            try:  # We don't want blocked DMs preventing us from banning
                await self.bot.send_message(user, "**You have been banned from {}.**\n**Reason:**  {}".format(server.name, reason))
                pass
                self._tmp_banned_cache.append(user)
                await self.bot.ban(user)
                await self.bot.say("Done, I have banned {} from the server.".format(user.name))
                await self.new_case(server,
                                    action="Ban \N{HAMMER}",
                                    mod=author,
                                    user=user)
            except discord.errors.Forbidden:
                await self.bot.say("I do not have the perms to ban users in this chat, please give ban perms.")
            except Exception as e:
                print(e)
            finally:
                await asyncio.sleep(1)
                self._tmp_banned_cache.remove(user)

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member):
        """Kicks the user, deleting 1 day worth of messages."""
        server = ctx.message.server
        channel = ctx.message.channel
        can_ban = channel.permissions_for(server.me).ban_members
        author = ctx.message.author
        try:
            invite = await self.bot.create_invite(server, max_age=3600*24)
            invite = "\nInvite: " + invite
        except:
            invite = ""
        if can_ban:
            try:
                try:  # We don't want blocked DMs preventing us from banning
                    msg = await self.bot.send_message(user, "You have been banned and "
                              "then unbanned as a quick way to delete your messages.\n"
                              "You can now join the server again.{}".format(invite))
                except:
                    pass
                self._tmp_banned_cache.append(user)
                await self.bot.ban(user, 1)
                logger.info("{}({}) softbanned {}({}), deleting 1 day worth "
                    "of messages".format(author.name, author.id, user.name,
                     user.id))
                await self.new_case(server,
                                    action="Softban \N{DASH SYMBOL} \N{HAMMER}",
                                    mod=author,
                                    user=user)
                await self.bot.unban(server, user)
                await self.bot.say("Done. Enough chaos.")
            except discord.errors.Forbidden:
                await self.bot.say("My role is not high enough to softban that user.")
                await self.bot.delete_message(msg)
            except Exception as e:
                print(e)
            finally:
                await asyncio.sleep(1)
                self._tmp_banned_cache.remove(user)
        else:
            await self.bot.say("I'm not allowed to do that.")

    @commands.command(no_pm=True, pass_context=True, hidden=True)
    @checks.admin_or_permissions(manage_nicknames=True)
    async def rename(self, ctx, user : discord.Member, *, nickname=""):
        """Changes user's nickname

        Leaving the nickname empty will remove it."""
        nickname = nickname.strip()
        if nickname == "":
            nickname = None
        try:
            await self.bot.change_nickname(user, nickname)
            await self.bot.say("Done.")
        except discord.Forbidden:
            await self.bot.say("I cannot do that, I lack the "
                "\"Manage Nicknames\" permission.")

    @commands.group(pass_context=True, no_pm=True, invoke_without_command=True)
    @checks.mod_or_permissions(administrator=True)
    async def mute(self, ctx, user : discord.Member):
        """Mutes user in the channel/server

        Defaults to channel"""
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.channel_mute, user=user)

    @mute.command(name="channel", pass_context=True, no_pm=True)
    async def channel_mute(self, ctx, user : discord.Member):
        """Mutes user in the current channel"""
        channel = ctx.message.channel
        overwrites = channel.overwrites_for(user)
        if overwrites.send_messages is False:
            await self.bot.say("That user can't send messages in this "
                               "channel.")
            return
        self._perms_cache[user.id][channel.id] = overwrites.send_messages
        overwrites.send_messages = False
        try:
            await self.bot.edit_channel_permissions(channel, user, overwrites)
        except discord.Forbidden:
            await self.bot.say("Failed to mute user. I need the manage roles "
                               "permission and the user I'm muting must be "
                               "lower than myself in the role hierarchy.")
        else:
            dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
            await self.bot.say("User has been muted in this channel.")
            await self.new_case(ctx.message.server,
                                    action="Channel Mute :no_mouth:",
                                    mod=ctx.message.author,
                                    user=user)

    @mute.command(name="server", pass_context=True, no_pm=True)
    async def server_mute(self, ctx, user : discord.Member):
        """Mutes user in the server"""
        server = ctx.message.server
        register = {}
        for channel in server.channels:
            if channel.type != discord.ChannelType.text:
                continue
            overwrites = channel.overwrites_for(user)
            if overwrites.send_messages is False:
                continue
            register[channel.id] = overwrites.send_messages
            overwrites.send_messages = False
            try:
                await self.bot.edit_channel_permissions(channel, user,
                                                        overwrites)
            except discord.Forbidden:
                await self.bot.say("Failed to mute user. I need the manage roles "
                                   "permission and the user I'm muting must be "
                                   "lower than myself in the role hierarchy.")
                return
            else:
                await asyncio.sleep(0.1)
        if not register:
            await self.bot.say("That user is already muted in all channels.")
            return
        self._perms_cache[user.id] = register
        dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
        await self.bot.say("User has been muted in this server.")
        await self.new_case(ctx.message.server,
                                    action="Mute :no_mouth:",
                                    mod=ctx.message.author,
                                    user=user)

    @commands.command(name="unmute", pass_context=True, no_pm=True)
    async def server_unmute(self, ctx, user : discord.Member):
        """Unmutes user in the server"""
        server = ctx.message.server
        if user.id not in self._perms_cache:
            await self.bot.say("That user doesn't seem to have been muted with {0}mute commands. "
                               "Unmute them in the channels you want with `{0}unmute <user>`"
                               "".format(ctx.prefix))
            return
        for channel in server.channels:
            if channel.type != discord.ChannelType.text:
                continue
            if channel.id not in self._perms_cache[user.id]:
                continue
            value = self._perms_cache[user.id].get(channel.id)
            overwrites = channel.overwrites_for(user)
            if overwrites.send_messages is False:
                overwrites.send_messages = value
                is_empty = self.are_overwrites_empty(overwrites)
                try:
                    if not is_empty:
                        await self.bot.edit_channel_permissions(channel, user,
                                                                overwrites)
                    else:
                        await self.bot.delete_channel_permissions(channel, user)
                except discord.Forbidden:
                    await self.bot.say("Failed to unmute user. I need the manage roles"
                                       " permission and the user I'm unmuting must be "
                                       "lower than myself in the role hierarchy.")
                    return
                else:
                    del self._perms_cache[user.id][channel.id]
                    await asyncio.sleep(0.1)
        if user.id in self._perms_cache and not self._perms_cache[user.id]:
            del self._perms_cache[user.id] #cleanup
        dataIO.save_json("data/mod/perms_cache.json", self._perms_cache)
        await self.bot.say("User has been unmuted in this server.")
        await self.new_case(ctx.message.server,
                                    action="Server Unmute :smiley:",
                                    mod=ctx.message.author,
                                    user=user)

    @commands.group(pass_context=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def prune(self, ctx):
        """Deletes messages."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @prune.command(pass_context=True)
    async def user(self, ctx, user: discord.Member, number: int):
        """Deletes last X messages from specified user.

        Examples:
        cleanup user @\u200bTwentysix 2
        cleanup user Red 6"""

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        def check(m):
            if m.author == user:
                return True
            elif m == ctx.message:
                return True
            else:
                return False

        to_delete = [ctx.message]

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        tries_left = 5
        tmp = ctx.message

        while tries_left and len(to_delete) - 1 < number:
            async for message in self.bot.logs_from(channel, limit=100,
                                                    before=tmp):
                if len(to_delete) - 1 < number and check(message):
                    to_delete.append(message)
                tmp = message
            tries_left -= 1

        logger.info("{}({}) deleted {} messages "
                    " made by {}({}) in channel {}"
                    "".format(author.name, author.id, len(to_delete),
                              user.name, user.id, channel.name))

        if is_bot:
            await self.mass_purge(to_delete)
        else:
            await self.slow_deletion(to_delete)

    @prune.command(pass_context=True)
    async def messages(self, ctx, number: int):
        """Deletes last X messages.

        Example:
        cleanup messages 26"""

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        async for message in self.bot.logs_from(channel, limit=number+1):
            to_delete.append(message)

        logger.info("{}({}) deleted {} messages in channel {}"
                    "".format(author.name, author.id,
                              number, channel.name))

        if is_bot:
            await self.mass_purge(to_delete)
        else:
            await self.slow_deletion(to_delete)

    @commands.command(pass_context=True, hidden=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def reason(self, ctx, case, *, reason : str=""):
        """Lets you specify a reason for mod-log's cases

        Defaults to last case assigned to yourself, if available."""
        author = ctx.message.author
        server = author.server
        try:
            case = int(case)
            if not reason:
                await send_cmd_help(ctx)
                return
        except:
            if reason:
                reason = "{} {}".format(case, reason)
            else:
                reason = case
            case = self.last_case[server.id].get(author.id, None)
            if case is None:
                await send_cmd_help(ctx)
                return
        try:
            await self.update_case(server, case=case, mod=author,
                                   reason=reason)
        except UnauthorizedCaseEdit:
            await self.bot.say("That case is not yours.")
        except KeyError:
            await self.bot.say("That case doesn't exist.")
        except NoModLogChannel:
            await self.bot.say("There's no mod-log channel set.")
        except CaseMessageNotFound:
            await self.bot.say("Couldn't find the case's message.")
        else:
            await self.bot.say("Case #{} updated.".format(case))

    @commands.command()
    async def names(self, user : discord.Member):
        """Show previous names/nicknames of a user"""
        server = user.server
        names = self.past_names[user.id] if user.id in self.past_names else None
        try:
            nicks = self.past_nicknames[server.id][user.id]
            nicks = [escape_mass_mentions(nick) for nick in nicks]
        except:
            nicks = None
        msg = ""
        if names:
            names = [escape_mass_mentions(name) for name in names]
            msg += "**Past 20 names**:\n"
            msg += ", ".join(names)
        if nicks:
            if msg:
                msg += "\n\n"
            msg += "**Past 20 nicknames**:\n"
            msg += ", ".join(nicks)
        if msg:
            await self.bot.say(msg)
        else:
            await self.bot.say("That user doesn't have any recorded name or "
                               "nickname change.")

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def addrole(self, ctx, rolename, user: discord.Member=None):
        """Adds a role to a user, defaults to author
        Role name must be in quotes if there are spaces."""
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server

        if user is None:
            user = author

        role = self._role_from_string(server, rolename)

        if role is None:
            await self.bot.say('That role cannot be found.')
            return

        if not channel.permissions_for(server.me).manage_roles:
            await self.bot.say('I don\'t have manage_roles.')
            return

        await self.bot.add_roles(user, role)
        await self.bot.say('Added role {} to {}'.format(role.name, user.name))

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def removerole(self, ctx, rolename, user: discord.Member=None):
        """Removes a role from user, defaults to author
        Role name must be in quotes if there are spaces."""
        server = ctx.message.server
        author = ctx.message.author

        role = self._role_from_string(server, rolename)
        if role is None:
            await self.bot.say("Role not found.")
            return

        if user is None:
            user = author

        if role in user.roles:
            try:
                await self.bot.remove_roles(user, role)
                await self.bot.say("Role successfully removed.")
            except discord.Forbidden:
                await self.bot.say("I don't have permissions to manage roles!")
        else:
            await self.bot.say("User does not have that role.")

    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  roles)
        try:
            log.debug("Role {} found from rolename {}".format(
                role.name, rolename))
        except:
            log.debug("Role not found for rolename {}".format(rolename))
        return role
    
    @commands.command(pass_context = True)
    @checks.mod_or_permissions(manage_messages=True)
    async def botclean(self, ctx, limit : int = None):
        """Removes all bot messages."""
        if limit is None:
            limit = 100
        elif limit > 100:
            limit = 100
        await self.bot.purge_from(ctx.message.channel, limit=limit, before=ctx.message, check= lambda e: e.author.bot)
        
    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_roles=True)
    async def crole(self, ctx, *, rolename: str = None):
        """Creates a role.
        When the roles is created it will appear at the bottom of the list."""
        if rolename is None:
            await self.bot.say("Please specify a name for the role.")
            return
        server = ctx.message.server
        name = ''.join(rolename)
        await self.bot.create_role(server, name= '{}'.format(name))
        message = "**Done, I have created the role {}.** :thumbsup:".format(name)
        await self.bot.say(message)
        
    @commands.command(pass_context=True)
    async def drole(self, ctx, rolename):
        """Deletes an existing role."""
        channel = ctx.message.channel
        server = ctx.message.server

        role = self._role_from_string(server, rolename)

        if role is None:
            await self.bot.say('**Role was not found.**')
            return

        await self.bot.delete_role(server,role)
        message = "**Done, I have deleted the role {}.** :thumbsup:".format(rolename)
        await self.bot.say(message)

    @commands.group(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def erole(self, ctx):
        """Edits roles settings"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @commands.command(pass_context=True)
    async def deleteme(self, message):
        msg = await self.bot.say('I will delete myself now...')
        await self.bot.delete_message(msg)

    @erole.command(aliases=["color"], pass_context=True)
    async def colour(self, ctx, role: discord.Role, value: discord.Colour):
        """Edits a role's colour
        Use double quotes if the role contains spaces.
        Colour must be in hexadecimal format.
        \"http://www.w3schools.com/colors/colors_picker.asp\"
        Examples:
        r!!editrole colour \"The Transistor\" #ff0000
        r!!editrole colour Test #ff9900"""
        author = ctx.message.author
        try:
            await self.bot.edit_role(ctx.message.server, role, color=value)
            logger.info("{}({}) changed the colour of role '{}'".format(
                author.name, author.id, role.name))
            await self.bot.say("Done, there you go fam.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to manage roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")

    @erole.command(name="name", pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def edit_role_name(self, ctx, role: discord.Role, name: str):
        """Edits a role's name
        Use double quotes if the role or the name contain spaces.
        Examples:
        r!!editrole name \"The Transistor\" Test"""
        if name == "":
            await self.bot.say("Name cannot be empty.")
            return
        try:
            author = ctx.message.author
            old_name = role.name  # probably not necessary?
            await self.bot.edit_role(ctx.message.server, role, name=name)
            logger.info("{}({}) changed the name of role '{}' to '{}'".format(
                author.name, author.id, old_name, name))
            await self.bot.say("Done, there you go fam.")
        except discord.Forbidden:
            await self.bot.say("I need permissions to manage roles first.")
        except Exception as e:
            print(e)
            await self.bot.say("Something went wrong.")
        
    async def mass_purge(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1.5)

    async def slow_deletion(self, messages):
        for message in messages:
            try:
                await self.bot.delete_message(message)
            except:
                pass

    def is_mod_or_superior(self, message):
        user = message.author
        server = message.server
        admin_role = settings.get_server_admin(server)
        mod_role = settings.get_server_mod(server)

        if user.id == settings.owner:
            return True
        elif discord.utils.get(user.roles, name=admin_role):
            return True
        elif discord.utils.get(user.roles, name=mod_role):
            return True
        else:
            return False

    async def new_case(self, server, *, action, mod=None, user, reason=None):
        channel = server.get_channel(self.settings[server.id]["mod-log"])
        if channel is None:
            return

        if server.id in self.cases:
            case_n = len(self.cases[server.id]) + 1
        else:
            case_n = 1

        case = {"case"         : case_n,
                "action"       : action,
                "user"         : user.name,
                "user_id"      : user.id,
                "reason"       : reason,
                "moderator"    : mod.name if mod is not None else None,
                "moderator_id" : mod.id if mod is not None else None}

        if server.id not in self.cases:
            self.cases[server.id] = {}

        tmp = case.copy()
        if case["reason"] is None:
            tmp["reason"] = "Type [p]reason {} <reason> to add it".format(case_n)
        if case["moderator"] is None:
            tmp["moderator"] = "Unknown"
            tmp["moderator_id"] = "Nobody has claimed responsibility yet"

        case_msg = ("**Case #{case}** | {action}\n"
                    "**User:** {user} ({user_id})\n"
                    "**Moderator:** {moderator} ({moderator_id})\n"
                    "**Reason:** {reason}"
                    "".format(**tmp))

        try:
            msg = await self.bot.send_message(channel, case_msg)
        except:
            msg = None

        case["message"] = msg.id if msg is not None else None

        self.cases[server.id][str(case_n)] = case

        if mod:
            self.last_case[server.id][mod.id] = case_n

        dataIO.save_json("data/mod/modlog.json", self.cases)

    async def update_case(self, server, *, case, mod, reason):
        channel = server.get_channel(self.settings[server.id]["mod-log"])
        if channel is None:
            raise NoModLogChannel()

        case = str(case)
        case = self.cases[server.id][case]

        if case["moderator_id"] is not None:
            if case["moderator_id"] != mod.id:
                raise UnauthorizedCaseEdit()

        case["reason"] = reason
        case["moderator"] = mod.name
        case["moderator_id"] = mod.id

        case_msg = ("**Case #{case}** | {action}\n"
                    "**User:** {user} ({user_id})\n"
                    "**Moderator:** {moderator} ({moderator_id})\n"
                    "**Reason:** {reason}"
                    "".format(**case))

        dataIO.save_json("data/mod/modlog.json", self.cases)

        msg = await self.bot.get_message(channel, case["message"])
        if msg:
            await self.bot.edit_message(msg, case_msg)
        else:
            raise CaseMessageNotFound()

    async def check_filter(self, message):
        server = message.server
        if server.id in self.filter.keys():
            for w in self.filter[server.id]:
                if w in message.content.lower():
                    try:
                        await self.bot.delete_message(message)
                        logger.info("Message deleted in server {}."
                                    "Filtered: {}"
                                    "".format(server.id, w))
                        return True
                    except:
                        pass
        return False

    async def check_duplicates(self, message):
        server = message.server
        author = message.author
        if server.id not in self.settings:
            return False
        if self.settings[server.id]["delete_repeats"]:
            self.cache[author].append(message)
            msgs = self.cache[author]
            if len(msgs) == 3 and \
                    msgs[0].content == msgs[1].content == msgs[2].content:
                if any([m.attachments for m in msgs]):
                    return False
                try:
                    await self.bot.delete_message(message)
                    return True
                except:
                    pass
        return False

    async def check_mention_spam(self, message):
        server = message.server
        author = message.author
        if server.id not in self.settings:
            return False
        if self.settings[server.id]["ban_mention_spam"]:
            max_mentions = self.settings[server.id]["ban_mention_spam"]
            mentions = set(message.mentions)
            if len(mentions) >= max_mentions:
                try:
                    self._tmp_banned_cache.append(author)
                    await self.bot.ban(author, 1)
                except:
                    logger.info("Failed to ban member for mention spam in "
                                "server {}".format(server.id))
                else:
                    await self.new_case(server,
                                        action="Ban \N{HAMMER}",
                                        mod=server.me,
                                        user=author,
                                        reason="Mention spam (Autoban)")
                    return True
                finally:
                    await asyncio.sleep(1)
                    self._tmp_banned_cache.remove(author)
        return False

    async def on_command(self, command, ctx):
        """Currently used for:
            * delete delay"""
        server = ctx.message.server
        message = ctx.message
        try:
            delay = self.settings[server.id]["delete_delay"]
        except KeyError:
            # We have no delay set
            return
        except AttributeError:
            # DM
            return

        if delay == -1:
            return

        async def _delete_helper(bot, message):
            try:
                await bot.delete_message(message)
                logger.debug("Deleted command msg {}".format(message.id))
            except discord.errors.Forbidden:
                # Do not have delete permissions
                logger.debug("Wanted to delete mid {} but no"
                             " permissions".format(message.id))

        await asyncio.sleep(delay)
        await _delete_helper(self.bot, message)

    async def on_message(self, message):
        if message.channel.is_private or self.bot.user == message.author \
         or not isinstance(message.author, discord.Member):
            return
        elif self.is_mod_or_superior(message):
            return
        deleted = await self.check_filter(message)
        if not deleted:
            deleted = await self.check_duplicates(message)
        if not deleted:
            deleted = await self.check_mention_spam(message)

    def fetch_joined_at(self, user, server):
        """Just a special case for someone special :^)"""
        if user.id == "96130341705637888" and server.id == "133049272517001216":
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at

    async def on_member_ban(self, member):
        if member not in self._tmp_banned_cache:
            server = member.server
            await self.new_case(server,
                                user=member,
                                action="Ban \N{HAMMER}")

    async def check_names(self, before, after):
        if before.name != after.name:
            if before.id not in self.past_names:
                self.past_names[before.id] = [after.name]
            else:
                if after.name not in self.past_names[before.id]:
                    names = deque(self.past_names[before.id], maxlen=20)
                    names.append(after.name)
                    self.past_names[before.id] = list(names)
            dataIO.save_json("data/mod/past_names.json", self.past_names)

        if before.nick != after.nick and after.nick is not None:
            server = before.server
            if server.id not in self.past_nicknames:
                self.past_nicknames[server.id] = {}
            if before.id in self.past_nicknames[server.id]:
                nicks = deque(self.past_nicknames[server.id][before.id],
                              maxlen=20)
            else:
                nicks = []
            if after.nick not in nicks:
                nicks.append(after.nick)
                self.past_nicknames[server.id][before.id] = list(nicks)
                dataIO.save_json("data/mod/past_nicknames.json",
                                 self.past_nicknames)

    def are_overwrites_empty(self, overwrites):
        """There is currently no cleaner way to check if a
        PermissionOverwrite object is empty"""
        original = [p for p in iter(overwrites)]
        empty = [p for p in iter(discord.PermissionOverwrite())]
        return original == empty
        
    async def on_message(self, message):
        data = fileIO(self.link_data, "load")
        if message.channel.is_private:
            return
        else:
            pass
        if not message.server.id in data:
            data[message.server.id] = db_data
            fileIO(self.link_data,"save", data)
        else:
            pass
        directory = fileIO(self.link_data, "load")
        db = directory[message.server.id]
        channel = message.channel
        idk = message.content
        if db["Toggle"] is True and db["No Invite"] is True:
            check = None
            if ("discord.gg/" in message.content) or ("discord" in idk and "." in idk and "gg" in idk and "/" in idk) or ("discordapp.com/invite/" in message.content) or ("discord.me/" in message.content) or ("discordapp" in idk and "." in idk and "com" in idk and "/" in idk and "invite" in idk and "/" in idk):
                check = True
            else:
                pass
            embeds = message.embeds
            if len(embeds) > 0 and message.author != self.bot.user:
                edb = embeds[0]
                if "type" in edb and edb["type"] == "rich":
                    des = edb["description"] if "description" in edb else "None"
                    tex = edb["title"] if "title" in edb else "None"
                    nam = edb["author"]["name"] if "author" in edb and "name" in edb["author"] else "None"
                else:
                    des = "None"
                    tex = "None"
                    nam = "None"
                if ("discord.gg/" in des) or ("discord" in des and "." in des and "gg" in des and "/" in des) or ("discordapp.com/invite/" in des) or ("discord.me/" in des) or ("discordapp" in des and "." in des and "com" in des and "/" in des and "invite" in des and "/" in des):
                    check = True
                else:
                    pass
                if ("discord.gg/" in tex) or ("discord" in tex and "." in tex and "gg" in tex and "/" in tex) or ("discordapp.com/invite/" in tex) or ("discord.me/" in tex) or ("discordapp" in tex and "." in tex and "com" in tex and "/" in tex and "invite" in tex and "/" in tex):
                    check = True
                else:
                    pass
                if ("discord.gg/" in nam) or ("discord" in nam and "." in nam and "gg" in nam and "/" in nam) or ("discordapp.com/invite/" in nam) or ("discord.me/" in nam) or ("discordapp" in nam and "." in nam and "com" in nam and "/" in nam and "invite" in nam and "/" in nam):
                    check = True
                else:
                    pass
            else:
                pass
            if check is True:
                try:
                    await self.bot.delete_message(message)
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    fmt = "{0.author.mention}, **Please do not send invite links in this server**".format(message)
                    try:
                        await self.bot.send_message(channel, fmt)
                    except discord.Forbidden:
                        try:
                            await self.bot.send_message(author, fmt)
                        except discord.Forbidden:
                            pass
                else:
                    fmt = "{0.author.mention}, **Please do not send invite links in this server**".format(message)
                    try:
                        await self.bot.send_message(channel, fmt)
                    except discord.Forbidden:
                        try:
                            await self.bot.send_message(author, fmt)
                        except discord.Forbidden:
                            pass
        else:
            pass
        if db["Toggle"] is True and db["Toggle Blacklist"] is True:
            check = None
            embeds = message.embeds
            edb = None
            if len(embeds) > 0:
                edb = embeds[0]
            des = "None"
            tex = "None"
            nam = "None"
            if edb is not None:
                if edb["type"] == "rich":
                    des = edb["description"] if "description" in edb else "None"
                    tex = edb["title"] if "title" in edb else "None"
                    nam = edb["author"]["name"] if "author" in edb and "name" in edb["author"] else "None"
                else:
                    pass
            else:
                des = "None"
                tex = "None"
                nam = "None"
            some_list = " ".join(e for e in [des, tex, nam, message.content])
            for word in db["Blacklisted"]:
                if word in some_list:
                    check = True
            if check is True:
                try:
                    await self.bot.delete_message(message)
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    pass
                else:
                    pass
    async def on_message_edit(self, before, after):
        data = fileIO(self.link_data, "load")
        if before.channel.is_private:
            return
        else:
            pass
        if before.server.id not in data:
            data[before.server.id] = db_data
            fileIO(self.link_data,"save",data)
        directory = fileIO(self.link_data, "load")
        db = directory[before.server.id]
        channel = before.channel
        if not before.content != after.content:
            pass
        else:
            message = after
            idk = message.content
            if db["Toggle"] is True and db["No Invite"] is True:
                check = None
                if ("discord.gg/" in message.content) or ("discord" in idk and "." in idk and "gg" in idk and "/" in idk) or ("discordapp.com/invite/" in message.content) or ("discord.me/" in message.content) or ("discordapp" in idk and "." in idk and "com" in idk and "/" in idk and "invite" in idk and "/" in idk):
                    check = True
                else:
                    pass
                embeds = message.embeds
                if len(embeds) > 0:
                    edb = embeds[0]
                    if "type" in edb and edb["type"] == "rich":
                        des = edb["description"] if "description" in edb else "None"
                        tex = edb["title"] if "title" in edb else "None"
                        nam = edb["author"]["name"] if "author" in edb and "name" in edb["author"] else "None"
                    else:
                        des = "None"
                        tex = "None"
                        nam = "None"
                    if ("discord.gg/" in des) or ("discord" in des and "." in des and "gg" in des and "/" in des) or ("discordapp.com/invite/" in des) or ("discord.me/" in des) or ("discordapp" in des and "." in des and "com" in des and "/" in des and "invite" in des and "/" in des):
                        check = True
                    else:
                        pass
                    if ("discord.gg/" in tex) or ("discord" in tex and "." in tex and "gg" in tex and "/" in tex) or ("discordapp.com/invite/" in tex) or ("discord.me/" in tex) or ("discordapp" in tex and "." in tex and "com" in tex and "/" in tex and "invite" in tex and "/" in tex):
                        check = True
                    else:
                        pass
                    if ("discord.gg/" in nam) or ("discord" in nam and "." in nam and "gg" in nam and "/" in nam) or ("discordapp.com/invite/" in nam) or ("discord.me/" in nam) or ("discordapp" in nam and "." in nam and "com" in nam and "/" in nam and "invite" in nam and "/" in nam):
                        check = True
                    else:
                        pass
                if check is True:
                    try:
                        await self.bot.delete_message(message)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        fmt = "{0.author.mention}, **Please do not send invite links in this server**".format(message)
                        try:
                            await self.bot.send_message(channel, fmt)
                        except discord.Forbidden:
                            try:
                                await self.bot.send_message(author, fmt)
                            except discord.Forbidden:
                                pass
                    else:
                        fmt = "{0.author.mention}, **Please do not send invite links in this server**".format(message)
                        try:
                            await self.bot.send_message(channel, fmt)
                        except discord.Forbidden:
                            try:
                               await self.bot.send_message(author, fmt)
                            except discord.Forbidden:
                                pass
            else:
                pass
            if db["Toggle"] is True and db["Toggle Blacklist"] is True:
                check = None
                embeds = message.embeds
                edb = None
                if len(embeds) > 0:
                    edb = embeds[0]
                des = "None"
                tex = "None"
                nam = "None"
                if edb is not None:
                    if edb["type"] == "rich":
                        des = edb["description"] if "description" in edb else "None"
                        tex = edb["title"] if "title" in edb else "None"
                        nam = edb["author"]["name"] if "author" in edb and "name" in edb["author"] else "None"
                    else:
                        pass
                else:
                    des = "None"
                    tex = "None"
                    nam = "None"
                some_list = " ".join(e for e in [des, tex, nam, message.content])
                for word in db["Blacklisted"]:
                    if word in some_list:
                        check = True
                if check is True:
                    try:
                        await self.bot.delete_message(message)
                    except discord.Forbidden:
                        pass
                    except discord.NotFound:
                        pass
                    else:
                        pass
                    
    async def on_server_join(self, server):
        data = fileIO(self.link_data, "load")
        data[server.id] = db_data
        fileIO(self.link_data, "save", data)
                
def check_folders():
    if os.path.exists("data/antilink"):
        pass
    else:
        try:
            print("Creating data/antilink folder...")
            os.makedirs("data/antilink")
        except FileExistsError:
            pass
        else:
            print("created data/antilinks folder")

def check_files():
    f = "data/antilink/antilink.json"
    if not fileIO(f, "check"):
        print("Creating antilink antilink.json...")
        fileIO(f, "save", {})


def check_folders():
    folders = ("data", "data/mod/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    ignore_list = {"SERVERS": [], "CHANNELS": []}

    files = {
        "blacklist.json"      : [],
        "whitelist.json"      : [],
        "ignorelist.json"     : ignore_list,
        "filter.json"         : {},
        "past_names.json"     : {},
        "past_nicknames.json" : {},
        "settings.json"       : {},
        "modlog.json"         : {},
        "perms_cache.json"    : {}
    }

    for filename, value in files.items():
        if not os.path.isfile("data/mod/{}".format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json("data/mod/{}".format(filename), value)

def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("mod")
    # Prevents the logger from being loaded again in case of module reload
    if logger.level == 0:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='data/mod/mod.log', encoding='utf-8', mode='a')
        handler.setFormatter(
            logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    n = Mod(bot)
    bot.add_listener(n.check_names, "on_member_update")
    bot.add_cog(n)
