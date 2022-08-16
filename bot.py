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

async def create_portal(ctx, color):
    gateway[color] = ctx.channel.id

    print(f"Portal bound: {color.upper().ljust(6)} -- {repr('#' + ctx.channel.name)} :: {repr(ctx.channel.guild.name)}")
    await ctx.send(f"{'A' if color == 'blue' else 'An'} {color} portal has been spawned.")

@bot.command()
async def blue(ctx):
    """Open a blue portal"""
    global ignore_next_message
    ignore_next_message = True

    await create_portal(ctx, "blue")

@bot.command()
async def orange(ctx):
    """Open an orange portal"""
    global ignore_next_message
    ignore_next_message = True

    await create_portal(ctx, "orange")

async def status_message_for_portal(ctx, portal):
    opposite_color = "orange" if portal == "blue" else "blue"

    status = ""

    if gateway[portal] is None:
        status = "closed"
    else:
        channel = await fetch_channel(gateway[portal], lambda s: ctx.send(s + f"\n{portal.title()} portal has been reset."))

        if channel is None:
            status = "closed"
        else:
            status = f"open (`#{channel.name} :: {channel.guild.name}`)"

    return portal.title() + ": " + status

@bot.command()
async def status(ctx):
    """Query portal status"""
    global ignore_next_message
    ignore_next_message = True

    message = await status_message_for_portal(ctx, "blue") + "\n" + await status_message_for_portal(ctx, "orange")

    await ctx.send(message)

@bot.command()
async def reset(ctx):
    """Reset all portals"""
    gateway["blue"]   = None
    gateway["orange"] = None

    print("Portals reset")
    await ctx.send("All portals have been reset.")

bot.run(os.getenv("TOKEN"))

