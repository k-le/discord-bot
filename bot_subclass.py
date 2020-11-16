# bot_subclass.py
# testing bot subclass from Discord extensions package

import owm
import smartystreets
import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # loading Discord Bot token from .env

# OpenWeatherMap API
OWMKey = os.getenv('OWM_API') # retrieving OWM Key

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
async def weather(ctx, postal_code):
    weather_dict = owm.get_weather_dict(postal_code)
    loc_dict = smartystreets.get_loc_dict(postal_code)

    weather_id = owm.get_weather_id(weather_dict)

    temp = owm.get_temperature(weather_dict)
    weather_cond = owm.get_weather_conditions(weather_id)
    wind_speed = owm.get_wind(weather_dict)
    humidity = owm.get_humidity(weather_dict)

    city = owm.get_city(weather_dict)
    state = smartystreets.get_state(loc_dict)

    await ctx.send(f'{city}, {state} \n'
                   f'{temp}° F \n'
                   f'Currently {weather_cond} \n'
                   f'Winds at {wind_speed}mph \n'
                   f'{humidity}% Humidity')

bot.run(TOKEN)

