# bot_subclass.py
# testing bot subclass from Discord extensions package

import os
import discord
import random
import pyowm
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # loading Discord Bot token from .env

# OpenWeatherMap API
OWMKey = os.getenv('OWM_API') # retrieving OWM Key
owm = pyowm.OWM(OWMKey) # establishing connection to OWM API
reg = owm.city_id_registry() # using OWM city ID registry to look up cities given their names
mgr = owm.weather_manager() # usage of OWM weather manager

# instead of the Client superclass, we utilize the Bot subclass
bot = commands.Bot(command_prefix='!')

# very similar to Client
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# //-------------------------------------------------------
# but bots must utilize arbitrary keywords (set by the programmer) for events to be called
# bot.command() takes in an argument, which allows the function to be called whenever the argument is mentioned, !JOJO
@bot.command(name='JOJO', help='Responds with the power of Jojo and Dio')
async def jojo(ctx):
    jojo_quotes = [
        'ORA ORA ORA ORA!!!',
        'MUDA MUDA MUDA MUDA MUDA MUDA MUDA MUDA MUDA MUDA!!'
    ]

    response = random.choice(jojo_quotes)
    await ctx.send(response)

@bot.command(name='weather')
async def weather(ctx, *, arg1):
    list_of_locations = reg.locations_for(arg1)
    city = list_of_locations[0]
    lat = city.lat
    lon = city.lon
    current_forecast_json = mgr.weather_at_coords(lat, lon)

    weather_dict = current_forecast_json.to_dict()
    city_name = weather_dict['location']['name']
    city_country = weather_dict['location']['country']
    temp_in_k = weather_dict['weather']['temperature']['temp']
    temp_in_fahrenheit = ((temp_in_k - 273.15) * (9/5) + 32)
    cloudiness = weather_dict['weather']['clouds']

    await ctx.send(f'City: {city_name}\n'
                   f'Country: {city_country} \n'
                   f'Temperature: {"{0:.2g}".format(temp_in_fahrenheit)}° F \n'
                   f'Clouds: {cloudiness}%'
                   )

bot.run(TOKEN)

