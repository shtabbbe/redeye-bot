import discord
from discord.ext import commands
import json
bot = commands.Bot(command_prefix="?")
startup_extensions = ["ticket"]
json_data = json.load(open('secrets.json'))

@bot.event
async def on_ready():
    print("Bot is ready")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(json_data["token"])

#invite https://discordapp.com/oauth2/authorize?client_id=425001421856047108&scope=bot&permissions=0
