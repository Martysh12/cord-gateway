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
    await bot.close()

@bot.command()
async def blue(ctx):
    """Open a blue portal"""
    pass

@bot.command()
async def orange(ctx):
    """Open an orange portal"""
    pass

bot.run(os.getenv("TOKEN"))

