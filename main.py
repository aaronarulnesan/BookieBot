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


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    bookieDB.close()
    await bot.logout()

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

@bot.command()
async def addOutcome(ctx, *, input):
    split = input.split(", ")
    wager = split[0]
    outcome = split[1]
    print(wager)
    print(outcome)
    if (len(wager)>255):
        wager = wager[0:221] + '...'
    bookieDB.insertOutcome(wager, outcome)
    await ctx.send("Outcome: {} has been made and placed under {}".format(outcome, wager))

@addOutcome.error
async def addOutcomeHandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Did not input a name for outcome")


bot.run(DISCORD_TOKEN)