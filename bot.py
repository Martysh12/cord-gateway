import nextcord
from nextcord.ext import commands

from dotenv import load_dotenv

import os

load_dotenv()

bot = commands.Bot(command_prefix="gate?")

gateway = {
    "blue"  : None,
    "orange": None
}

@bot.event
async def on_ready():
    print(f'Ready! Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def blue(ctx):
    """Open a blue portal"""
    gateway["blue"] = ctx.channel.id

    print(f"Portal bound: BLUE   -- {repr('#' + ctx.channel.name)} :: {repr(ctx.channel.guild.name)}")
    await ctx.send("A blue portal has been spawned.")

@bot.command()
async def orange(ctx):
    """Open an orange portal"""
    gateway["orange"] = ctx.channel.id

    print(f"Portal bound: ORANGE -- {repr('#' + ctx.channel.name)} :: {repr(ctx.channel.guild.name)}")
    await ctx.send("An orange portal has been spawned.")

@bot.command()
async def reset(ctx):
    """Reset all portals"""
    gateway["blue"]   = None
    gateway["orange"] = None

    print("Portals reset")
    await ctx.send("All portals have been reset.")

bot.run(os.getenv("TOKEN"))

