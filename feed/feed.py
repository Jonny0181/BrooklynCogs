import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help
import os

class Newsletter:
    """Allow users to sign up for a newsletter from the owner"""

    def __init__(self, bot):
        self.bot = bot
        self.new = "data/news/registered.json"
        self.news = dataIO.load_json(self.new)
        

    @commands.group(pass_context=True, invoke_without_command=True)
    async def feed(self, ctx):
        """Update Commands"""
        
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    

    @feed.command(pass_context=True)
    async def signup(self, ctx):
        """Signup for our Update feed."""
        
        user = ctx.message.author
        if user.id not in self.news:
            await self.bot.say("Ok, let me set up your account for our update feed!!")
            self.news[user.id] = {'send' : True}
            dataIO.save_json(self.new, self.news)
            await self.bot.say("Congrats, you will now recieve updates! You can turn it off by saying `{}feed toggle`.".format(ctx.prefix))
        else:
            await self.bot.say("You have already registered for a update feed acconut.")
 
    @feed.command(pass_context=True)
    async def toggle(self, ctx):
        """Allows you to turn on and off the updates whenever you feel like it!"""
        
        user = ctx.message.author
        if user.id in self.news:
            news = self.news[user.id]['send']
            if news is False:
                self.news[user.id]['send'] = True 
                dataIO.save_json(self.new, self.news)
                await self.bot.say("Congrats, you will now start recieving updates through pm!")
            else:
                self.news[user.id]['send'] = False 
                dataIO.save_json(self.new, self.news)
                await self.bot.say("Congrats, you will now stop recieving updates through pm!")
        else:
            await self.bot.say("{}, you need a update feed acconut to start receiving the latest info. Use `{}feed signup` now!".format(user.mention, ctx.prefix))

    @checks.is_owner()
    @feed.command(pass_context=True)
    async def announce(self, ctx, *, msg):
        """Owner only, sends announcement for people who !!!!"""

        if len(self.news) <= 0:
            await self.bot.say("You can't send a newsletter if no one is registered.")
            return
        
        for id in self.news:
            if self.news[id]['send']: 
                user = self.bot.get_user_info(id)
                message = "**{} Update!\n\n**".format(self.bot.user.name)
                message += msg
                message += "\n\n*You can always disable updates by saying `{}feed toggle!`*".format(ctx.prefix)
                users = discord.utils.get(self.bot.get_all_members(),
                                  id=id)
                try:
                    await self.bot.send_message(users, message)
                except:
                    await self.bot.say("The message didn't go through, `Fox News has edited this word out due to censorship, we apologize` owner! :angry:")
            else:
                pass
        else:
            await self.bot.say("Newsletter has all been sent out to everyone who wanted it!")

def check_folders():
    if not os.path.exists("data/news"):
        print("Creating the news folder, so be patient...")
        os.makedirs("data/news")
        print("Finish!")

def check_files():
    twentysix = "data/news/registered.json"
    json = {}
    if not dataIO.is_valid_json(twentysix):
        print("Derp Derp Derp...")
        dataIO.save_json(twentysix, json)

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Newsletter(bot))
