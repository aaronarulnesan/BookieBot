from discord.enums import NotificationLevel
import discord
from discord.ext import commands
import os
from database.database import DBConnection


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

bookieDB = DBConnection()

bot = commands.Bot(command_prefix = "$")

@bot.event
async def on_ready():
    print("------------------------------")
    print("API Version: {0}".format(discord.__version__))
    print('We have logged in as {0.user}'.format(bot))
    print("------------------------------")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!') 
    
#     if message.content.startswith('$close'):
#         bookieDB.close()
#         await bot.close()
#     await bot.process_commands(message)

@bot.command()
async def shutdown(ctx):
    bookieDB.close()
    await bot.close()

bot.run(DISCORD_TOKEN)