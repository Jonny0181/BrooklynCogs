import discord
import random
import sys
from discord.ext import commands
have_pil = True

class Random:
    def __init__(self, bot):
        self.bot = bot
        self.web_render = None

    @commands.command()
    async def charlie(self, *, question: str):
        """Ask a question... Charlie Charlie are you there?
        Usage: charlie [question to ask, without punctuation]"""
        aq = '' if question.endswith('?') else '?'
        await self.bot.say('*Charlie Charlie* ' + question + aq + "\n**" +
                           random.choice(['Yes', 'No']) + '**')
                           
    @commands.command(pass_context=True)
    async def screenshot(self, ctx):
        """Take a screenshot.
        Usage: screenshot"""
        if have_pil and (sys.platform not in ['linux', 'linux2']):
            grabber = ImageGrab
        else:
            grabber = pyscreenshot
        image = grabber.grab()
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        await self.bot.upload(img_bytes, filename='screenshot.png', content='This is *probably* what my screen looks like right now.')
        
    @commands.command(pass_context=True)
    async def render(self, ctx, *, webpage: str):
        """Render a webpage to image.
        Usage: render [url]"""
        await self.bot.say(':warning: Not yet working.'
                           'Type `yes` within 6 seconds to proceed and maybe crash your bot.')
        if not (await self.bot.wait_for_message(timeout=6.0, author=ctx.message.author,
                                                channel=ctx.message.channel,
                                                check=lambda m: m.content.lower().startswith('yes'))):
            return
        try:
            self.web_render = scr.Screenshot()
            image = self.web_render.capture(webpage)
            await self.bot.upload(io.BytesIO(image), filename='webpage.png')
        except Exception as e:
            await self.bot.say(e)
                           
    @commands.command()
    async def randcolor(self):
        """Generate a random color.
        Usage: rcolor"""
        col_rgb = [random.randint(1, 255) for i in range(0, 3)]
        col_str = '0x%02X%02X%02X' % (col_rgb[0], col_rgb[1], col_rgb[2])
        await self.bot.say(embed=discord.Embed(color=int(col_str, 16), title='Hex: ' + col_str.replace('0x', '#') + ' | RGB: ' + ', '.join([str(c) for c in col_rgb]) + ' | Integer: ' + str(int(col_str, 16))))

    @commands.command(pass_context=True, aliases=['ip', 'rdns', 'reverse_dns', 'reversedns'])
    async def ipinfo(self, ctx, *, ip: str):
        """Get the GeoIP and rDNS data for an IP.
        Usage: ipinfo [ip/domain]"""
        emb = discord.Embed(color=random.randint(1, 255**3-1))
        target = self.bot.user
        au = target.avatar_url
        avatar_link = (au if au else target.default_avatar_url)
        emb.set_author(icon_url=avatar_link, name='IP Data')
        async with aiohttp.ClientSession(loop=self.loop) as sess:
            with async_timeout.timeout(5):
                async with sess.get('https://freegeoip.net/json/' + ip) as r:
                    data_res = await r.json()
        rdns = 'Failed to fetch'
        try:
            with async_timeout.timeout(6):
                rdns = (await self.loop.run_in_executor(None, socket.gethostbyaddr, data_res['ip']))[0]
        except Exception:
            pass
        emb.add_field(name='IP', value=data_res['ip'])
        emb.add_field(name='Reverse DNS', value=rdns)
        emb.add_field(name='Country', value=data_res['country_name'] + ' (%s)' % data_res['country_code'])
        region_val = data_res['region_name'] + ' (%s)' % data_res['region_code']
        emb.add_field(name='Region', value=(region_val if region_val != ' ()' else 'Not specified'))
        emb.add_field(name='City', value=(data_res['city'] if data_res['city'] else 'Not specified'))
        emb.add_field(name='ZIP Code', value=(data_res['zip_code'] if data_res['zip_code'] else 'Not specified'))
        emb.add_field(name='Timezone', value=(data_res['time_zone'] if data_res['time_zone'] else 'Not specified'))
        emb.add_field(name='Longitude', value=data_res['longitude'])
        emb.add_field(name='Latitude', value=data_res['latitude'])
        emb.add_field(name='Metro Code', value=(data_res['metro_code'] if data_res['metro_code'] != 0 else 'Not specified'))
        await self.bot.send_message(ctx.message.channel, embed=emb)

def setup(bot):
    n = Random(bot)
    bot.add_cog(n)
