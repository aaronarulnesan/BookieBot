from discord.enums import NotificationLevel
import discord
from discord.ext import commands
import os
from database.database import *
import traceback


DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

bookieDB = DBManagement()

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

@bot.command()
async def makeWager(ctx, *, wagerName):
    wager = wagerName
    if (len(wager)>255):
        wager = wager[0:221] + '...'
    bookieDB.insertWager(wager)
    await ctx.send("Wager: {} has been made!".format(wager))

@makeWager.error
async def makeWagerHandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Did not input a name for the wager")


bot.run(DISCORD_TOKEN)