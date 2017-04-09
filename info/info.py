import asyncio
import discord
import random
import os
import psutil
import datetime
import time
import copy
from .utils import checks
from .utils.formats import human_timedelta
from discord.ext import commands
from __main__ import send_cmd_help
from .utils.chat_formatting import box
wrap = "```py\n{}\n```"
starttime = time.time()
class Info:
    def __init__(self, bot):
	    self.bot = bot
	    self.cache_path = "data/audio/cache"

    def fetch_joined_at(self, user, server):
        """Just a special case for someone special :^)"""
        if user.id == "96130341705637888" and server.id == "133049272517001216":
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at
            
    def _cache_size(self):
        songs = os.listdir(self.cache_path)
        size = sum(map(lambda s: os.path.getsize(
            os.path.join(self.cache_path, s)) / 10**6, songs))
        return size

    @commands.command(pass_context=True, no_pm=True, aliases=['newmembers'])
    async def newusers(self, ctx, *, count=5):
        """Tells you the newest members of the server.
        This is useful to check if any suspicious members have
        joined.
        The count parameter can only be up to 25.
        """
        guild = ctx.message.server
        count = max(min(count, 25), 5)

        members = sorted(guild.members, key=lambda m: m.joined_at, reverse=True)[:count]

        e = discord.Embed(title='New Members', colour=discord.Colour.green())

        for member in members:
            body = '`Joined Server:` {0}\n`Account created:` {1}'.format(human_timedelta(member.joined_at),
                                                    human_timedelta(member.created_at))
            e.add_field(name='{0} (ID: {0.id})'.format(member), value=body, inline=False)

        await self.bot.say(embed=e)

    @commands.command(pass_context=True)
    async def sleaderboard(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        e = discord.Embed(colour=author.colour)
        e.set_thumbnail(url=server.me.avatar_url)
        e.title = "Currently on {} server with {} users!".format(len(self.bot.servers), len([e.name for e in self.bot.get_all_members()]))
        e.description = "".join(["**Name:** {0.name} | **Members:** {0.member_count} Members\n\n".format(e) for e in sorted(self.bot.servers, key =lambda e : e.member_count, reverse=True)][:10])
        await self.bot.say(embed=e)

    @commands.command(pass_context=True)
    async def serverstats(self, ctx):
        away = "<:vpAway:212789859071426561>"
        dnd = "<:vpDnD:236744731088912384>"
        offline = "<:vpOffline:212790005943369728>"
        online = "<:vpOnline:212789758110334977>"
        on = len([e.name for e in self.bot.get_all_members() if e.status == discord.Status.online])
        idlle = len([e.name for e in self.bot.get_all_members() if e.status == discord.Status.idle])
        dnd2 = len([e.name for e in self.bot.get_all_members() if e.status == discord.Status.dnd])
        off = len([e.name for e in self.bot.get_all_members() if e.status == discord.Status.offline])
        msg = "I am currently in **{}** servers.\n".format(len(self.bot.servers))
        msg += "{} Users: {}\n".format(online, on)
        msg += "{} Users: {}\n".format(away, idlle)
        msg += "{} Users: {}\n".format(dnd, dnd2)
        msg += "{} Users: {}\n".format(offline, off)
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def discr(self, ctx, discrim: int):
        """gives you farmed discrms"""
        try:
            dis = []
            for server in self.bot.servers:
                for member in server.members:
                    if int(member.discriminator) == discrim:
                        if not member.name in dis:
                            dis.append(member.name)
            em = discord.Embed(title="Scraped Discriminators\n", description="\n".join(dis),color=0xff5555, inline=True)
            await self.bot.say(embed=em)
        except Exception as e:
            await self.bot.say(wrap.format(type(e).__name__ + ': ' + str(e)))
	
    @commands.command(pass_context=True)
    async def banlist(self, ctx):
        """Displays the server's banlist"""
        try:
            banlist = await self.bot.get_bans(ctx.message.server)
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Ban Members` permission")
            return
        bancount = len(banlist)
        if bancount == 0:
            banlist = "No users are banned from this server"
        else:
            banlist = ", ".join(map(str, banlist))
        await self.bot.say("Total bans: `{}`\n```{}```".format(bancount, banlist))
    
    @commands.command(pass_context=True)
    async def info(self, ctx):
        """Shows information on Brooklyn."""
        prefix = ctx.prefix
        owner = "<@146040787891781632>"
        servers = len(self.bot.servers)
        members = len([e.name for e in self.bot.get_all_members()])
        e = discord.Embed(description="Brooklyn - A multi function Discord bot with music, moderation, and utility features.", colour=discord.Colour.blue())
        e.add_field(name="Live Information:", value="Owner: {}\nPrefix: {}\nServers: {}\nTotal Users: {}\nTotal Commands: {}\nTotal Modules: {}\nApi Version: {}".format(owner, prefix, servers, members, len(self.bot.commands), len(self.bot.cogs), discord.__version__))
        e.add_field(name="Links:", value="[Support Server.](https://discord.gg/ETqpvsa)\n[Invite url.](https://discordapp.com/oauth2/authorize?client_id=226132382846156800&permissions=-1&scope=bot)\n[Website](http://brooklyn.cf/)\n[Patreon](https://www.patreon.com/_brooklyn)")
        e.set_author(name="Brooklyn#6591", icon_url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
        e.add_field(name="Changelog:", value="""**Added:**
`1)` b!sleaderboard | Shows Brooklyn top 10 servers.
`2)` b!antiraid | Manage antiraid settings.""")
        e.set_thumbnail(url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
        try:
            await self.bot.say(embed=e)
        except discord.HTTPException:
            prefix = ctx.prefix
            owner = "<@146040787891781632>"
            servers = len(self.bot.servers)
            users = len([e.name for e in self.bot.get_all_members()])
            channels = len([e.name for e in self.bot.get_all_channels()])
            data = "**Brooklyn - A multi function Discord bot with music, moderation, and utility features.**\n\n"
            data += "**Live Information:**\n"
            data += "Owner: {}\n".format(owner)
            data += "Prefix: {}\n".format(prefix)
            data += "Servers: {}\n".format(servers)
            data += "Total Users: {}\n".format(users)
            data += "Total Channels: {}\n".format(channels)
            data += "Total Commands: {}\n".format(len(self.bot.commands))
            data += "Total Modules: {}\n\n".format(len(self.bot.cogs))
            data += "**Links:**\n"
            data += "Official Server: https://discord.gg/ETqpvsa\n"
            data += "Invite Url: https://discordapp.com/oauth2/authorize?client_id=226132382846156800&permissions=-1&scope=bot\n"
            data += "Website: http://brooklyn.cf/\n"
            data += "Patreon: https://www.patreon.com/_brooklyn\n\n"
            data += "**Changelog:**\n\n"
            data += "**Added:**\n"
            data += "`1)` b!sleaderboard | Shows Brooklyn top 10 servers.\n`2)` b!antiraid | Manage antiraid settings."
            await self.bot.say(data)

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong."""
        msg = await self.bot.say(embed=discord.Embed(description="Pinging to server.........", colour=discord.Colour.blue()))
        time = (msg.timestamp - ctx.message.timestamp).total_seconds() * 1000
        await self.bot.edit_message(msg, embed=discord.Embed(description='Pong: {}ms :ping_pong:'.format(round(time)), colour=discord.Colour.blue()))

    @commands.command(pass_context=True)
    async def pingt(self, ctx):
        await self.bot.say("Pinging to server...")
        await asyncio.sleep(0.9)
        await self.bot.say("Diving this by this.....")
        await asyncio.sleep(0.9)
        await self.bot.say("Alight now we need to times this by this....")
        await asyncio.sleep(0.9)
        await self.bot.say("Now we need to add this and then subtract by 2...")
        await asyncio.sleep(0.9)
        await self.bot.say("Checking calculations...")
        await asyncio.sleep(0.9)
        await self.bot.say("Editing a message....")
        msg = await self.bot.say("........")
        time = (msg.timestamp - ctx.message.timestamp).total_seconds() * 10
        await self.bot.edit_message(msg, 'Acording to my calculations it took {}ms to ping to the server.'.format(round(time)))

    @commands.command()
    async def join(self):
        await self.bot.whisper("Here is my link buddy.\nhttps://discordapp.com/oauth2/authorize?client_id=226132382846156800&permissions=-1&scope=bot")

    @commands.command(pass_context=True)
    async def stats(self, ctx):
        """Shows stats."""
        text_channels = 0
        voice_channels = 0
        list2 = []
        list = []
        for i in self.bot.servers:
            if i.me.voice_channel is not None:
                list.append(i.me.voice_channel)
        for c in list:
            list2.extend(c.voice_members)
        mem_v = psutil.virtual_memory()
        cpu_p = psutil.cpu_percent(interval=None, percpu=True)
        cpu_usage = sum(cpu_p)/len(cpu_p)
        online = len([e.name for e in self.bot.get_all_members() if not e.bot and e.status == discord.Status.online])
        idle = len([e.name for e in self.bot.get_all_members() if not e.bot and e.status == discord.Status.idle])
        dnd = len([e.name for e in self.bot.get_all_members() if not e.bot and e.status == discord.Status.dnd])
        offline = len([e.name for e in self.bot.get_all_members() if not e.bot and e.status == discord.Status.offline])
        seconds = time.time() - starttime
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        w, d = divmod(d, 7)
        t1 = time.perf_counter()
        await self.bot.type()
        t2 = time.perf_counter()
        data = discord.Embed(description="Showing stats for {}.".format(self.bot.user.name), colour=discord.Colour.red())
        data.add_field(name="Owner", value="<@146040787891781632>")
        data.add_field(name="Ping", value="{}ms".format(round((t2-t1)*1000)))
        data.add_field(name="Servers", value=len(self.bot.servers))
        data.add_field(name="Api version", value=discord.__version__)
        data.add_field(name="Users", value="{} Online<:vpOnline:212789758110334977>\n{} Idle<:vpAway:212789859071426561>\n{} Dnd<:vpDnD:236744731088912384>\n{} Offline<:vpOffline:212790005943369728>".format(online, idle, dnd, offline))
        data.add_field(name="Channels", value="{} Voice Channels\n{} Text Channels".format(len([e for e in self.bot.get_all_channels() if e.type == discord.ChannelType.voice]), len([e for e in self.bot.get_all_channels() if e.type == discord.ChannelType.text])))
        data.add_field(name='CPU usage', value='{0:.1f}%'.format(cpu_usage))
        data.add_field(name='Memory usage', value='{0:.1f}%'.format(mem_v.percent))
        data.add_field(name="Commands", value="{0} active modules, with {1} commands...".format(len(self.bot.cogs), len(self.bot.commands)))
        data.add_field(name='Uptime', value="%d Weeks," % (w) + " %d Days," % (d) + " %d Hours,"
                                   % (
                h) + " %d Minutes," % (m) + " and %d Seconds!" % (s))
        data.add_field(name="Voice Stats:", value="Connected to {} voice channels, with a total of {} users, and {:.3f} MB of cache.".format(len(list), len(list2), self._cache_size()), inline=False)
        data.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        data.set_thumbnail(url=ctx.message.author.avatar_url)
        await self.bot.say(embed=data)

    @commands.command(pass_context=True, allow_pm=False, hidden=True)
    async def sinfo2(self, ctx):
        "Show server , owner and channel info"
        server = ctx.message.server
        channel = ctx.message.channel
        members = set(server.members)

        owner = server.owner

        offline = filter(lambda m: m.status is discord.Status.offline, members)
        offline = set(offline)

        bots = filter(lambda m: m.bot, members)
        bots = set(bots)

        users = members - bots

        msg = '\n'.join((
            'Server Name     : ' + server.name,
            'Server ID       : ' + str(server.id),
            'Server Created  : ' + str(server.created_at),
            'Server Region   : ' + str(server.region),
            'Verification    : ' + str(server.verification_level),
            # minus one for @everyone
            'Server # Roles  : %i' % (len(server.roles) - 1),
            '',
            'Server Owner    : ' + (
                ('{0.nick} ({0})'.format(owner)) if owner.nick
                else str(owner)),
            'Owner ID        : ' + str(owner.id),
            'Owner Status    : ' + str(owner.status),
            '',
            'Total Bots      : %i' % len(bots),
            'Bots Online     : %i' % len(bots - offline),
            'Bots Offline    : %i' % len(bots & offline),
            '',
            'Total Users     : %i' % len(users),
            'Users Online    : %i' % len(users - offline),
            'Users Offline   : %i' % len(users & offline),
            '',
            'Current Channel : #' + channel.name,
            'Channel ID      : ' + str(channel.id),
            'Channel Created : ' + str(channel.created_at)
        ))
        embed=discord.Embed(description=msg, colour=discord.Colour.blue())
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def sinfo(self, ctx):
        """Shows servers informations"""
        server = ctx.message.server
        mfa_level = server.mfa_level
        vl = server.verification_level
        total = len([e.name for e in server.members if not e.bot])
        bots = len([e.name for e in server.members if e.bot])
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("**Created {}. {} days ago.**"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        x = -1
        emojis =  []
        while x < len([r for r in ctx.message.server.emojis]) -1:
            x = x + 1
            emojis.append("<:{}:{}>".format([r.name for r in ctx.message.server.emojis][x], [r.id for r in ctx.message.server.emojis][x]))

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Info", value=str("**Region:** {0.region}\n**Id:** {0.id}".format(server)))
        data.add_field(name="Users", value="**Humans:** {}\n**Bots:** {}".format(total, bots))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Verification Level", value=vl)
        data.add_field(name="Require 2FA", value=bool(mfa_level))
        data.add_field(name="Default Channel", value=server.default_channel.mention)
        data.add_field(name="Roles", value=len(server.roles))
        data.set_footer(text="Owner: {}".format(str(server.owner)))

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        if server.icon_url and server.features:
            data.set_author(name=server.name, url=server.icon_url, icon_url=server.icon_url)
            data.set_thumbnail(url="https://static-cdn.jtvnw.net/jtv_user_pictures/panel-92094149-image-0b6104b16249b783-320.png")
        else:
            data.set_author(name=server.name)
        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            online = str(len([m.status for m in server.members if str(m.status) == "online" or str(m.status) == "idle"]))
            server = ctx.message.server
            total_users = str(len(server.members))
            text_channels = len([x for x in server.channels if str(x.type) == "text"])
            voice_channels = len(server.channels) - text_channels
            list = [e for e in server.emojis if not e.managed]
            emoji = ''
            for emote in list:
                emoji += "<:{0.name}:{0.id}> ".format(emote)
            data = "```prolog\n"
            data += "Name: {}\n".format(server.name)
            data += "ID: {}\n".format(server.id)
            data += "Region: {}\n".format(server.region)
            data += "Users: {}/{}\n".format(online, total_users)
            data += "Text channels: {}\n".format(text_channels)
            data += "Voice channels: {}\n".format(voice_channels)
            data += "Roles: {}\n".format(len(server.roles))
            passed = (ctx.message.timestamp - server.created_at).days
            data += "Created: {} ({} days ago)\n".format(server.created_at, passed)
            data += "Owner: {}\n".format(server.owner)
            if server.icon_url != "":
                data += "Icon: {}".format(server.icon_url)
                data += "```"
            else:
                data += "```"
            if server.emojis:
                emojis =  []
                while x < len([r for r in ctx.message.server.emojis]) -1:
                    x = x + 1
                    emojis.append("<:{}:{}>".format([r.name for r in ctx.message.server.emojis][x], [r.id for r in ctx.message.server.emojis][x]))
                data += "Emotes\n{}".format(emoji)
            await self.bot.say(data)

    @commands.command(pass_context=True, no_pm=True)
    async def cookie(self, ctx, *, user: discord.Member):
        await self.bot.say("**You have given {} a cookie! | :cookie:**".format(user.mention))

    @commands.command(pass_context=True, no_pm=True)
    async def uinfo(self, ctx, *, user: discord.Member=None):
        """Shows userss informations"""
        author = ctx.message.author
        server = ctx.message.server

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = self.fetch_joined_at(user, server)
        since_created = (ctx.message.timestamp - user.created_at).days
        since_joined = (ctx.message.timestamp - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "**Playing:** {}".format(user.game)
        else:
            game = "**Streaming:** [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = discord.Embed(description=game, colour=user.colour)
        data.add_field(name="Name", value=user.name)
        data.add_field(name="ID", value=user.id)
        data.add_field(name="Color", value=user.colour)
        data.add_field(name="Discriminator", value=user.discriminator)
        data.add_field(name="VoiceChannel", value=bool(user.voice_channel))
        data.add_field(name="Nickname", value=user.nick)
        data.add_field(name="Deafened", value="Local: {}\nServer: {}".format(user.self_deaf, user.deaf))
        data.add_field(name="Muted", value="Local: {}\nServer: {}".format(user.self_mute, user.mute))
        data.add_field(name="Status", value=user.status)
        data.add_field(name="Top Role", value=user.top_role)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="All Roles", value=roles, inline=False)
        data.set_footer(text="Member Number: {}"
                             "".format(member_number))
        if user.avatar_url:
            name = str(user)
            name = " ~ ".join((name, user.nick)) if user.nick else name
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=user.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            author = ctx.message.author
            server = ctx.message.server
            if not user:
                user = author
            roles = [x.name for x in user.roles if x.name != "@everyone"]
            if not roles: roles = ["None"]
            data = "```prolog\n"
            data += "Name: {}\n".format(str(user))
            data += "Nickname: {}\n".format(str(user.nick))
            data += "ID: {}\n".format(user.id)
            if user.game is None:
                pass
            elif user.game.url is None:
                data += "Playing: {}\n".format(str(user.game))
            else:
                data += "Streaming: {} ({})\n".format(str(user.game),(user.game.url))
            passed = (ctx.message.timestamp - user.created_at).days
            data += "Created: {} ({} days ago)\n".format(user.created_at, passed)
            joined_at = self.fetch_joined_at(user, server)
            passed = (ctx.message.timestamp - joined_at).days
            data += "Joined: {} ({} days ago)\n".format(joined_at, passed)
            data += "Roles: {}\n".format(", ".join(roles))
            if user.avatar_url != "":
                data += "Avatar:"
                data += "```"
                data += user.avatar_url
            else:
                data += "```"
            await self.bot.say(data)

    @commands.command(pass_context=True)
    async def semotes(self, ctx):
        """ServerEmote List"""
        server = ctx.message.server

        list = [e for e in server.emojis if not e.managed]
        emoji = ''
        for emote in list:
            emoji += "<:{0.name}:{0.id}> ".format(emote)
        try:
            await self.bot.say(emoji)
        except:
            await self.bot.say("Server has no emotes.")

    @commands.command(pass_context=True)
    async def inrole(self, ctx, *, rolename):
        """Check members in the role specified."""
        colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        server = ctx.message.server
        message = ctx.message
        channel = ctx.message.channel
        await self.bot.send_typing(ctx.message.channel)
        therole = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), ctx.message.server.roles)
        if therole is not None and len([m for m in server.members if therole in m.roles]) < 50:
            await asyncio.sleep(1) #taking time to retrieve the names
            server = ctx.message.server
            member = discord.Embed(description="**{1} users found in the {0} role.**\n".format(rolename, len([m for m in server.members if therole in m.roles])), colour=discord.Colour(value=colour))
            member.add_field(name="Users", value="\n".join(m.display_name for m in server.members if therole in m.roles))
            await self.bot.say(embed=member)
        elif len([m for m in server.members if therole in m.roles]) > 50:
            awaiter = await self.bot.say("Getting Member Names")
            await asyncio.sleep(1)
            await self.bot.edit_message(awaiter, " :raised_hand: Woah way too many people in **{0}** Role, **{1}** Members found\n".format(rolename,  len([m.mention for m in server.members if therole in m.roles])))
        else:
            embed=discord.Embed(description="**Role was not found**", colour=discord.Colour(value=colour))
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def avatar(self, ctx, *, user: discord.Member=None):
        """Retrieves a users avatar."""
        author = ctx.message.author
        if not user:
            user = author
        data = discord.Embed(colour=user.colour)
        data.set_image(url=user.avatar_url)
        data.set_author(name="Avatar for "+user.name, icon_url=user.avatar_url)
        data.set_footer(text=datetime.datetime.now().strftime("%A, %B %-d %Y at %-I:%M%p").replace("PM", "pm").replace("AM", "am"))
        await self.bot.say(embed=data)

    @commands.command(pass_context=True)
    async def mods(self, ctx):
        """Shows mods in the server."""
        colour = "".join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        server = ctx.message.server
        one = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).manage_messages and not e.bot and e.status == discord.Status.online]
        two = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).manage_messages and not e.bot and e.status == discord.Status.idle]
        three = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).manage_messages and not e.bot and e.status == discord.Status.dnd]
        four = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).manage_messages and not e.bot and e.status == discord.Status.offline]
        embed = discord.Embed(description="Listing mods for this server.", colour=discord.Colour(value=colour))
        if one:
            embed.add_field(name="Online", value="{0}".format(("\n".join(one)).replace("`", "")), inline=False)
        else:
            embed.remove_field(0)
        if two:
            embed.add_field(name="Idle", value="{0}".format(("\n".join(two)).replace("`", "")), inline=False)
        else:
            embed.remove_field(1)
        if three:
            embed.add_field(name="Dnd", value="{0}".format(("\n".join(three)).replace("`", "")), inline=False)
        else:
            embed.remove_field(2)
        if four:
            embed.add_field(name="Offline", value="{0}".format(("\n".join(four)).replace("`", "")), inline=False)
        else:
            embed.remove_field(3)
        if server.icon_url:
            embed.set_author(name=server.name, url=server.icon_url)
            embed.set_thumbnail(url=server.icon_url)
        else:
            embed.set_author(name=server.name)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def admins(self, ctx):
        """Shows mods in the server."""
        colour = "".join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        server = ctx.message.server
        one = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).administrator and not e.bot and e.status == discord.Status.online]
        two = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).administrator and not e.bot and e.status == discord.Status.idle]
        three = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).administrator and not e.bot and e.status == discord.Status.dnd]
        four = [e.display_name for e in server.members if e.permissions_in(ctx.message.channel).administrator and not e.bot and e.status == discord.Status.offline]
        embed = discord.Embed(description="Listing admins for this server.", colour=discord.Colour(value=colour))
        if one:
            embed.add_field(name="Online", value="{0}".format(("\n".join(one)).replace("`", "")), inline=False)
        else:
            embed.remove_field(0)
        if two:
            embed.add_field(name="Idle", value="{0}".format(("\n".join(two)).replace("`", "")), inline=False)
        else:
            embed.remove_field(1)
        if three:
            embed.add_field(name="Dnd", value="{0}".format(("\n".join(three)).replace("`", "")), inline=False)
        else:
            embed.remove_field(2)
        if four:
            embed.add_field(name="Offline", value="{0}".format(("\n".join(four)).replace("`", "")), inline=False)
        else:
            embed.remove_field(3)
        if server.icon_url:
            embed.set_author(name=server.name, url=server.icon_url)
            embed.set_thumbnail(url=server.icon_url)
        else:
            embed.set_author(name=server.name)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def utime(self, ctx):
        """Shows how long the bot has been online."""
        seconds = time.time() - starttime
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        w, d = divmod(d, 7)
        await self.bot.say("Brooklyn has been up for %d Weeks," % (w) + " %d Days," % (d) + " %d Hours,"
                                   % (
                h) + " %d Minutes," % (m) + " and %d Seconds!" % (s))

    @commands.command(pass_context=True)
    async def roleid(self, ctx, rolename):
        """Gives the id of a role, must use quotes."""
        channel = ctx.message.channel
        server = ctx.message.server
        channel = ctx.message.channel
        await self.bot.send_typing(ctx.message.channel)

        role = self._role_from_string(server, rolename)

        if role is None:
            await self.bot.say(embed=discord.Embed(description='Cannot find role!', colour=discord.Colour.red()))
            return

        await self.bot.say(embed=discord.Embed(description=':white_check_mark: **Role id of {} is `{}`**'.format(rolename, role.id), colour=discord.Colour.green()))

    @commands.command(pass_context=True, aliases=["ri"])
    async def roleinfo(self, ctx, rolename):
        """Get your role info !!!
        If dis dun work first trry use "" quotes on te role"""
        channel = ctx.message.channel
        server = ctx.message.server
        colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
        colour = int(colour, 16)
        await self.bot.send_typing(ctx.message.channel)
        therole = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), ctx.message.server.roles)
        since_created = (ctx.message.timestamp - therole.created_at).days
        created_on = "{} days ago".format(since_created)
        if therole is None:
            await bot.say(':no_good: That role cannot be found. :no_good:')
            return
        if therole is not None:
            perms = iter(therole.permissions)
            perms_we_have = ""
            perms_we_dont = ""
            for x in perms:
                if "True" in str(x):
                    perms_we_have += "<:vpGreenTick:257437292820561920> {0}\n".format(str(x).split('\'')[1])
                else:
                    perms_we_dont += ("<:vpRedTick:257437215615877129> {0}\n".format(str(x).split('\'')[1]))
            msg = discord.Embed(description=":raised_hand:***`Collecting Role Stats`*** :raised_hand:",
            colour=therole.color)
            if therole.color is None:
                therole.color = discord.Colour(value=colour)
            lolol = await self.bot.say(embed=msg)
            em = discord.Embed(colour=therole.colour)
            em.add_field(name="Role Name", value=therole.name)
            em.add_field(name="Created", value=created_on)
            em.add_field(name="UsersinRole", value=len([m for m in server.members if therole in m.roles]))
            em.add_field(name="Id", value=therole.id)
            em.add_field(name="Color", value=therole.color)
            em.add_field(name="Position", value=therole.position)
            em.add_field(name="Valid Perms", value="{}".format(perms_we_have))
            em.add_field(name="Invalid Perms", value="{}".format(perms_we_dont))
            em.set_thumbnail(url=server.icon_url)
        try:
            await self.bot.edit_message(lolol, embed=em)
        except discord.HTTPException:
            permss = "```diff\n"
            therole = discord.utils.find(lambda r: r.name.lower() == rolename.lower(), ctx.message.server.roles)
            if therole is None:
                await bot.say(':no_good: That role cannot be found. :no_good:')
                return
            if therole is not None:
                perms = iter(therole.permissions)
                perms_we_have2 = ""
                perms_we_dont2 = ""
                for x in perms:
                    if "True" in str(x):
                        perms_we_have2 += "+{0}\n".format(str(x).split('\'')[1])
                    else:
                        perms_we_dont2 += ("-{0}\n".format(str(x).split('\'')[1]))
            await self.bot.say("{}Name: {}\nCreated: {}\nUsersinRole : {}\nId : {}\nColor : {}\nPosition : {}\nValid Perms : \n{}\nInvalid Perms : \n{}```".format(permss, therole.name, created_on, len([m for m in server.members if therole in m.roles]), therole.id, therole.color, therole.position, perms_we_have2, perms_we_dont2))
            await self.bot.delete_message(lolol)

    @commands.command(pass_context=True, no_pm=True, hidden=True)
    async def perms(self, ctx):
        user = await self._prompt(ctx, "Mention a user...")
        try:
            if user.mentions is not None:
                user = user.mentions[0]
        except:
            try:
                user = discord.utils.get(ctx.message.server.members, name=str(user.content))
            except:
                return await self.bot.say("User not found!:x:")
        perms = iter(ctx.message.channel.permissions_for(user))
        perms_we_have = "```diff\n"
        perms_we_dont = ""
        for x in perms:
            if "True" in str(x):
                perms_we_have += "+\t{0}\n".format(str(x).split('\'')[1])
            else:
                perms_we_dont += ("-\t{0}\n".format(str(x).split('\'')[1]))
        await self.bot.say("{0}{1}```".format(perms_we_have, perms_we_dont))

    async def _prompt(self, ctx, msg: str):
        await self.bot.say(msg)
        msg = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
        return msg

    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  roles)
        return role

def setup(bot):
	bot.add_cog(Info(bot))
