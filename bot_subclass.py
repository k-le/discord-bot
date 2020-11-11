# bot_subclass.py
# testing bot subclass from Discord extensions package

import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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


bot.run(TOKEN)

