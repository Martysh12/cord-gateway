import nextcord

from dotenv import load_dotenvi

load_dotenv()

bot = commands.Bot(command_prefix="gate?")

@bot.event
async def on_ready():
    print(f'Ready! Logged in as {bot.user} (ID: {bot.user.id})')
    bot.close()

bot.run(os.getenv("TOKEN"))

