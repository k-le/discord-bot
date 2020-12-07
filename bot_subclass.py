# bot_subclass.py
# testing bot subclass from Discord extensions package

import os
from dotenv import load_dotenv

from discord.ext import commands

import owm
import smartystreets
from youtube import YouTubeClient
from AllRecipes import AllRecipes

load_dotenv()
# Discord Token
TOKEN = os.getenv('DISCORD_TOKEN')

# OpenWeatherMap API Key
OWMKey = os.getenv('OWM_API')

# YouTube API
ytKEY = os.getenv('GOOGLE_KEY')

# instead of the Client superclass, we utilize the Bot subclass
bot = commands.Bot(command_prefix='!')


# //-------------------------------------------------------
# bots must utilize arbitrary keywords (set by the programmer) for events to be called
# bot.command() takes in an argument, which allows the function to be called whenever the argument is mentioned

# //-------------------------------------------------------
# weather command
@bot.command(name='weather',
             help='Given a 5-digit postal-code, will print out details about the current weather for that location')
async def weather(ctx, postal_code):
    """
    takes in a 5-digit postal code and prints out details about the current weather for the location
    utilizes OpenWeatherMap API for weather information and SmartyStreets API for location
    :param ctx: Context for bot
    :param postal_code: Int, 5-digit postal code for location purposes
    :return:
    """
    if ctx.author == bot.user:
        return

    weather_dict = owm.get_weather_dict(
        postal_code)  # creates a nested dictionary of weather info from parsed OpenWeatherMap JSON object
    loc_dict = smartystreets.get_loc_dict(
        postal_code)  # creates a nested dictionary of location info from parsed SmartyStreets JSON object

    weather_id = owm.get_weather_id(weather_dict)  # grabs weather id to identify weather conditions
    weather_cond = owm.get_weather_conditions(
        weather_id)  # weather conditions based on id parsed, snow, rain, clouds, etc.

    temp = owm.get_temperature(weather_dict)  # grabs temperature in fahrenheit
    wind_speed = owm.get_wind(weather_dict)  # wind speeds in mph
    humidity = owm.get_humidity(weather_dict)  # humidity percentage

    city = smartystreets.get_city(loc_dict)  # grabs city
    state = smartystreets.get_state(loc_dict)  # state

    await ctx.send(f'{city}, {state} \n'  # prints out a formatted response detailing the current weather of the
                   f'{temp}° F \n'  # given location into the server channel where the command was called
                   f'Currently {weather_cond} \n'
                   f'Winds at {wind_speed}mph \n'
                   f'{humidity}% Humidity')


@bot.command(name='play', help='Given a title, plays a video from YouTube')
async def play(ctx, *, video_title):
    if ctx.author == bot.user:
        return

    youtube = YouTubeClient(KEY=ytKEY)

    videoId = youtube.get_video_id(title=video_title)
    youtube.add_vid_to_playlist(videoId=videoId)

    if ctx.author.voice is None:
        await ctx.send("User is not connected to a channel.")
        raise RuntimeError("User is not connected to a channel.")
        return
    else:
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(f'https://www.youtube.com/watch?v={videoId["videoId"]}')

    await ctx.send(f'Added https://www.youtube.com/watch?v={videoId["videoId"]} to the queue.')
    bot._volume = 0.5


@bot.command(name='recipe', help='Given an ingredient, returns the top five recipes from allrecipes.com')
async def play(ctx, *, ingredient):
    if ctx.author == bot.user:
        return

    all_recipes = AllRecipes(ingredient=ingredient)

    count = 1
    to_print = ''
    for recipe in all_recipes.recipes[0:3]:
        await ctx.author.send(f'{count}. {recipe["name"]}\n'
                              f'{recipe["ratings"]}\n'
                              f'{recipe["description"]}\n'
                              f'{recipe["recipe_page"]}\n')
        count += 1

    # await ctx.send(to_print)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
