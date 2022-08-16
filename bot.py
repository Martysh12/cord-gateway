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

        color = {v: k for k, v in gateway.items()}[message.channel.id]
        opposite_color = "blue" if color == "orange" else "orange"

        try:
            other_channel = await bot.fetch_channel(gateway[opposite_color])
        except nextcord.errors.NotFound:
            gateway[opposite_color] = None
            await message.channel.send(f"Couldn't access the other channel. (is it deleted?)\n{opposite_color.title()} portal has been reset.")
            return
        except nextcord.errors.Forbidden:
            gateway[opposite_color] = None
            await message.channel.send(f"Couldn't access the other channel. (does the bot have the required permissions?)\n{opposite_color.title()} portal has been reset.")
            return

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
async def status(ctx):
    """Query portal status"""
    message = ""

    message += f"Blue: "

    if gateway["blue"] is not None:
        channel = await bot.fetch_channel(gateway['blue'])
        message += f"opened (`#{channel.name} :: {channel.guild.name}`)"
    else:
        message += "closed"

    message += "\n"

    message += f"Orange: "

    if gateway["orange"] is not None:
        channel = await bot.fetch_channel(gateway['orange'])
        message += f"opened (`#{channel.name} :: {channel.guild.name}`)"
    else:
        message += "closed"

    await ctx.send(message)

@bot.command()
async def reset(ctx):
    """Reset all portals"""
    gateway["blue"]   = None
    gateway["orange"] = None

    print("Portals reset")
    await ctx.send("All portals have been reset.")

bot.run(os.getenv("TOKEN"))

