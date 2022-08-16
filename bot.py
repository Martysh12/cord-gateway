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

async def fetch_channel(channel_id, send_message):
    try:
        return await bot.fetch_channel(channel_id)
    except nextcord.errors.NotFound:
        await send_message(f"Couldn't access the other channel. (is it deleted?)")
    except nextcord.errors.Forbidden:
        await send_message(f"Couldn't access the other channel. (does the bot have the required permissions?)")

    return

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

        other_channel = await fetch_channel(gateway[opposite_color], lambda s: message.channel.send(s + f"\n{opposite_color.title()} portal has been reset."))

        if other_channel is None:
            gateway[opposite_color] = None
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
    global ignore_next_message
    ignore_next_message = True

    message = ""

    message += f"Blue: "

    if gateway["blue"] is not None:
        channel = await fetch_channel(gateway["blue"], lambda s: ctx.send(s + "\nBlue portal has been reset."))

        if channel is None:
            message += "closed"
        else:
            message += f"opened (`#{channel.name} :: {channel.guild.name}`)"
    else:
        message += "closed"

    message += "\n"

    message += f"Orange: "

    if gateway["orange"] is not None:
        channel = await fetch_channel(gateway["orange"], lambda s: ctx.send(s + "\nOrange portal has been reset."))

        if channel is None:
            message += "closed"
        else:
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

