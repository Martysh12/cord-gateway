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
    gateway["blue"] = ctx.channel

@bot.command()
async def orange(ctx):
    """Open an orange portal"""
    gateway["orange"] = ctx.channel

bot.run(os.getenv("TOKEN"))

