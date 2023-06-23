import disnake
from disnake.ext import commands
import json
import os

config_file_path = "config.json"

if not os.path.exists(config_file_path):
    config_data = {
        "TOKEN": "token",
        "YOU_ID": 123456789
    }
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    
with open(config_file_path, "r") as config_file:
    config = json.load(config_file)

token = config["TOKEN"]
bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("I am ready")
    print(f"Logged on {bot.user.name}")

bot.run(token)