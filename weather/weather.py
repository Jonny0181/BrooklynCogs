import os
import aiohttp
from discord.ext import commands


class Weather:
    """
    Bot commands to retrieve weather API data.
    """

    def __init__(self, bot):
        self.bot = bot

    async def weather_api_call(self, endpoint, zip_code):
        async with aiohttp.ClientSession() as session:
            url = 'http://api.wunderground.com/api/c80325c858abf20d/{}/q/{}.json'.format(
                endpoint,
                zip_code
            )
            async with session.get(url) as resp:
                if resp.status is not 200:
                    await self.bot.say('```Error: cannot fetch wunderground.com data.```')
                    raise aiohttp.errors.ClientConnectionError
                else:
                    return await resp.json()

    @commands.command()
    async def wx(self, zip_code: int):
        """
        Return current weather conditions.
        """
        data = await self.weather_api_call(endpoint='conditions', zip_code=zip_code)

        try:
            await self.bot.say(
                '```City: {}\nWeather: {}\nTemp: {}\nWind: {}\nHumidity: {}\nRain: {}```'.format(
                    data['current_observation']['display_location']['full'],
                    data['current_observation']['weather'],
                    data['current_observation']['temperature_string'],
                    data['current_observation']['wind_string'],
                    data['current_observation']['relative_humidity'],
                    data['current_observation']['precip_today_string']
                )
            )
        except:
            await self.bot.say('```Error: invalid zip code.```')

    @commands.command()
    async def forecast(self, zip_code: int):
        """
        Return three day weather forecast.
        """
        data = await self.weather_api_call(endpoint='forecast', zip_code=zip_code)

        try:
            await self.bot.say(
                '```{}:\n\n{}\n\n{}:\n\n{}\n\n{}:\n\n{}\n\n{}:\n\n{}\n\n{}:\n\n{}\n\n{}:\n\n{}```'.format(
                    data['forecast']['txt_forecast']['forecastday'][0]['title'],
                    data['forecast']['txt_forecast']['forecastday'][0]['fcttext'],
                    data['forecast']['txt_forecast']['forecastday'][1]['title'],
                    data['forecast']['txt_forecast']['forecastday'][1]['fcttext'],
                    data['forecast']['txt_forecast']['forecastday'][2]['title'],
                    data['forecast']['txt_forecast']['forecastday'][2]['fcttext'],
                    data['forecast']['txt_forecast']['forecastday'][3]['title'],
                    data['forecast']['txt_forecast']['forecastday'][3]['fcttext'],
                    data['forecast']['txt_forecast']['forecastday'][4]['title'],
                    data['forecast']['txt_forecast']['forecastday'][4]['fcttext'],
                    data['forecast']['txt_forecast']['forecastday'][5]['title'],
                    data['forecast']['txt_forecast']['forecastday'][5]['fcttext']
                )
            )
        except:
            await self.bot.say('```Error: invalid zip code.```')

    @commands.command(pass_context=True)
    async def radar(self, ctx, zip_code: int):
        """
        Display static radar image.
        """
        channel = ctx.message.channel

        try:
            data = await self.weather_api_call(endpoint='conditions', zip_code=zip_code)
            if data['current_observation']['display_location']['zip'] == str(zip_code):
                async with aiohttp.ClientSession() as session:
                    url = 'http://api.wunderground.com/api/c80325c858abf20d/radar/q/{}.png?newmaps=1&smooth=1&noclutter=1'.format(
                        zip_code
                    )
                    async with session.get(url) as resp:
                        if resp.status is not 200:
                            await self.bot.say('```Error: cannot fetch wunderground.com data.```')
                            raise aiohttp.errors.ClientConnectionError
                        else:
                            image_file = '{}.png'.format(zip_code)
                            with open(image_file, 'wb') as f:
                                while True:
                                    chunk = await resp.content.read()
                                    if not chunk:
                                        break
                                    f.write(chunk)
                                    await self.bot.send_file(channel, image_file)
                                    f.close()
                                    os.remove(image_file)
        except:
            await self.bot.say('```Error: invalid zip code.```')


def setup(bot):
    bot.add_cog(Weather(bot))
