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

ignore_next_message = False

@bot.event
async def on_ready():
    print(f'Ready! Logged in as {bot.user} (ID: {bot.user.id})')

@bot.listen("on_message")
async def message_relayer(message):
    if (gateway["blue"] is None) or (gateway["orange"] is None):
        return

    if message.author == bot.user:
        return

    if message.channel.id in gateway.values():
        global ignore_next_message

        if ignore_next_message:
            ignore_next_message = False
            return

        if message.channel.id == gateway["blue"]:
            other_channel = await bot.fetch_channel(gateway["orange"])
            await other_channel.send(message.content)

        if message.channel.id == gateway["orange"]:
            other_channel = await bot.fetch_channel(gateway["blue"])
            await other_channel.send(message.content)

@bot.command()
async def blue(ctx):
    """Open a blue portal"""
    gateway["blue"] = ctx.channel.id

    global ignore_next_message
    ignore_next_message = True

    print(f"Portal bound: BLUE   -- {repr('#' + ctx.channel.name)} :: {repr(ctx.channel.guild.name)}")
    await ctx.send("A blue portal has been spawned.")

@bot.command()
async def orange(ctx):
    """Open an orange portal"""
    gateway["orange"] = ctx.channel.id

    global ignore_next_message
    ignore_next_message = True

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

