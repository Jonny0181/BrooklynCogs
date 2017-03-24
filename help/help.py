import discord
from discord.ext import commands

a=discord.Embed(title="About Brooklyn", description="""Brooklyn - A fun multipurpose bot for Discord with an interactive Cleverbot, Music, Moderation and many other Utility features.\nFor Help: [Brooklyn Help](https://discord.gg/fmuvSX9)\nOAuth Link: [Brooklyn OAuth](https://discordapp.com/oauth2/authorize?client_id=226132382846156800&permissions=-1&scope=bot)""", colour=discord.Colour.blue())
a.set_thumbnail(url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")

au=discord.Embed(title="Audio Commands:", description="""
  **np  :**           Info about the current song.
  **pause  :**        Pauses the current song, `[p]resume` to continue.
  **play  :**         Plays a link / searches and play.
  **queue  :**        Shows the current queue.
  **resume  :**       Resumes a paused song or playlist.
  **skip  :**         Skips a song, using the set threshold if the requester isn't.
  **stop  :**         Stops a currently playing song or playlist. 
  **volume  :**       Sets the volume (0 - 100).
  **disconnect  :**   Disconnects Brooklyn from the voice channel.""", colour=discord.Colour.red())
au.set_thumbnail(url="https://images-ext-2.discordapp.net/eyJ1cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vZFVzZm5EUUpadDJ2OWQxbjJ0V3NQWmlZTExtT1FranYzUjRyYnNUdzgzbFlHbzJjUWU4dTJ6LTBZUVB4bW1jZ2tMOGQ9dzMwMCJ9.vpoypHNhN9RNUM_NgLm89xQvjB0?width=80&height=80")

fun=discord.Embed(title="Fun Commands:", description="""
  **heist  :**        General heist related commands.
  **setheist  :**     Set different options in the heist config.
  **bank  :**         Bank operations
  **economyset  :**   Changes economy module settings
  **leaderboard  :**  Server / global leaderboard
  **payday  :**       Get some free credits
  **payouts  :**      Shows slot machine payouts
  **slot  :**         Play the slot machine.
  **cahcredits  :**   Code credits.
  **cahgames  :**     Displays up to 10 CAH games in progress.
  **chat  :**         Broadcasts a message to the other players.
  **flushhand  :**    Flushes the cards in your hand.
  **game  :**         Displays the game's current status.
  **hand  :**         Shows your hand.
  **idlekick  :**     Sets whether or not to kick members if idle.
  **joincah  :**      Join a Cards Against Humanity game.
  **laid  :**         Shows who laid their cards and who hasn't.
  **lay  :**          Lays a card or cards from your hand.
  **leavecah  :**     Leaves the current game you're in.
  **newcah  :**       Starts a new Cards Against Humanity game.
  **pick  :**         As the judge - pick the winning card(s).
  **removeplayer  :** Removes a player from the game.
  **score  :**        Display the score of the current game.
  **cookie  :**       Give a user a cookie.""", colour=discord.Colour.red())
fun.set_thumbnail(url="http://www.niagarafallsfunzone.com/images/layout/tickets.png")

mod=discord.Embed(title="Moderation Commands:", description="""
  **addrole  :**      Adds a role to a user, defaults to author
  **ban  :**          Bans a user from the server.
  **botclean  :**     Removes all bot messages.
  **crole  :**        Creates a role.
  **drole  :**        Deletes an existing role.
  **erole  :**        Edits roles settings.
  **hackban  :**      Bans user by id, user doesn't have to be in server.
  **unban  :**        Unbans a user from the server. Uses user id.
  **kick  :**         Kicks user.
  **massmove  :**     Massmove users to another voice channel.
  **mute  :**         Mutes user in the channel/server.
  **prune  :**        Deletes messages.
  **removerole  :**   Removes a role from user.
  **softban  :**      Kicks user, deleting 1 day of messages.
  **unmute  :**       Unmutes user in the channel/server.
  **autorole  :**     Change settings for autorole.
  **antilink  :**     Antilink settings for your server.
  **pin  :**          Pin a recent message, useful on mobile.
  **modlogset  :**    Change modlog settings.
  **modlogtoggle  :** toggle which server activity to log.
  **welcomer  :**     Welcome and leave message, with invite link.
  **serverprefix  :** Set your own prefix for your server.""", colour=discord.Colour.green())
mod.set_thumbnail(url="https://images-ext-2.discordapp.net/.eJwNwcEOwiAMANB_4V5oJ5ixm4l3P4E0sUOSSRpkclj27_reYfa2mcW8etfFuTGG1X37SoPeuNRSs32Ku6mmO3dOD5XqypuzfJz3M2LgCShcEPwcCSIxwSohMCNSvK5pCpgI_6zWbM4fD7EiMg.E9FwPjfhw-pCKaEMXTvoZ2-ZY-M?width=80&height=80")

info=discord.Embed(title="Infomation Commands: ", description="""
  **names  :**        Show previous names/nicknames of a user
  **admins  :**       Shows mods in the server.
  **avatar  :**       Retrieves a users avatar.
  **discr  :**        Gives you farmed discrms.
  **inrole  :**       Check members in the role specified.
  **mods  :**         Shows mods in the server.
  **ping  :**         Pong.
  **roleid  :**       Gives the id of a role, must use quotes.
  **roleinfo  :**     Gives you information about a role.
  **semotes  :**      ServerEmote List.
  **sinfo  :**        Shows servers informations.
  **stats  :**        Shows stats.
  **uinfo  :**        Shows users informations
  **utime  :**        Shows how long the bot has been online.
  **feed  :**         Enables or disables announcement subscription.
  **banlist  :**      Shows bans for the server.
  **serverstats  :**  Shows stats on users status and servercount.
  **sleaderboard  :** Shows Brooklyn top 10 servers.""", colour=discord.Colour.blue())
info.set_thumbnail(url="https://images-ext-1.discordapp.net/eyJ1cmwiOiJodHRwczovL3VwbG9hZC53aWtpbWVkaWEub3JnL3dpa2lwZWRpYS9lbi81LzU0L0luZm9ybWF0aW9uLnBuZyJ9.xi-2ZzV_czvJDaudMrqeqOgNZ8E?width=80&height=80")

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def audio(self, ctx):
        """Sends Audio help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=au)
                
    @commands.command(pass_context=True)
    async def mod(self, ctx):
        """Sends Mod help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=mod)

    @commands.command(pass_context=True)
    async def fun(self, ctx):
        """Sends Fun help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=fun)
                
    @commands.command(pass_context=True)
    async def information(self, ctx):
        """Sends Info help message."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = channel
        await self.bot.send_message(destination, embed=info)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        """Channel help message."""
        try:
            e=discord.Embed(title="Brooklyn Help", description="Here is a little bit of help with Brooklyn!\n\n**1)** To get all of Brooklyn's commands you may type `b!commands`.\n**2)** For Brooklyn's support server you may join [here.](https://discord.gg/fmuvSX9)\n**3)** For updates on Brooklyn you may join [here.](https://discord.gg/weDWNJm)\n**4)** For changelog and more type `b!info`.\n**5)** You may type the module as a command and all the commands in that module will be pasted out in a message. Example: `b!mod`\n**6)** And for any comments or concerns please use the `b!contact` commands.\n\nThank you for reading this and have a great day!", colour=discord.Colour.blue())
            e.set_thumbnail(url="https://images-ext-1.discordapp.net/.eJwFwQsKwyAMANC7eAA_iU3TwthZYhRW2FZRu8FK7773TnO0p1nNY4zaV-c0v23euu4tS61W95eTjwxp3QFQQEAGjhQmYu8dKsSFOSoxQ8ZJEMscUoLZL5FI7bekeu_br9yCh2iuP44VINs.ZtSGfr53jRG7PUbMI4gaUeWw0l0?width=250&height=250")
            await self.bot.say(embed=e)
        except:
            msg = "__**Brooklyn Help**__\n\n"
            msg += "**1)** To get all of Brooklyn's commands you may type `b!commands`.\n"
            msg += "**2)** For changelog and more type `b!info`.\n"
            msg += "**3)** You may type the module as a command. Example: `b!mod`\n"
            msg += "**4)** And for any comments or concerns please use the b!contact commands.\n\n"
            msg += "__**Thank you for reading this and have a great day!**__\n\n"
            msg += "`Disclaimer:` This is the old embed, you're only seeing this because I do not have embed perms. If you want to see the new help message please give me embed perms."
            await self.bot.say(msg)
            
    @commands.command(pass_context=True, no_pm=True)
    async def help2(self, ctx):
        await self.bot.say(":warning: | Some menu items may not work for certain users due to permission requirements.")
        author = ctx.message.author
        menu = self.bot.get_cog("Menu")
        cmds = ["Roles", "Send modules", "List modules", "Permissions", "Invite", "Disclaimer", "Cancel"]

        result = await menu.number_menu(ctx, "Utilities menu", cmds, autodelete=True)
        cmd = cmds[result-1]

        if cmd == "Roles":
            await ctx.invoke(self.roles)
                
        if cmd == "Send modules":
            await ctx.invoke(self.sendmod)
        
        if cmd == "List modules":
            await ctx.invoke(self.listmods)
            
        if cmd == "Permissions":
            await ctx.invoke(self.permissions)
            
        if cmd == "Invite":
            await ctx.invoke(self.invite)
                
        if cmd == "Disclaimer":
            await ctx.invoke(self.disclaimer)    
                
        if cmd == "Cancel":
            return await self.bot.say("Menu cancelled.")

        if cmd is None:
            return await self.bot.say("Menu has expired.")

    @commands.command(pass_context=True)
    async def commands(self, ctx):
        """Shows all commands."""
        channel = ctx.message.channel
        author = ctx.message.author
        destination = author
        await self.bot.send_message(destination, embed=a)
        await self.bot.send_message(destination, embed=au)
        await self.bot.send_message(destination, embed=mod)
        await self.bot.send_message(destination, embed=info)
        await self.bot.send_message(destination, embed=fun)

    async def on_message(self, message):
        if message.content == "b!commands":
            if not message.channel.is_private:
                await self.bot.send_message(message.channel, message.author.mention+", I have pm'd you my commands! :mailbox_with_mail:")        

def setup(bot):
    n = Help(bot)
    bot.remove_command('help')
    bot.add_cog(n)
