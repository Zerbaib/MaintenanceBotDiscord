import disnake
from disnake.ext import commands
import json
import os

config_file_path = "config.json"

if not os.path.exists(config_file_path):
    config_data = {
        "TOKEN": "token",
        "YOU_ID": 123456789,
        "GUILD_ID": 123456789
    }
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    
with open(config_file_path, "r") as config_file:
    config = json.load(config_file)

token = config["TOKEN"]
guild_id = config["GUILD_ID"]
you = config["YOU_ID"]
bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("I am ready")
    print(f"Logged on {bot.user.name}")

@bot.slash_command(
    name="maintenance"
    description="Set the server in maintenance"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, msg: None):
    if ctx.author.id != you:
        await ctx.send("You can't do that", delete_after=3)
        return
    
    if msg == None:
        msg = "Aucune info n'est donner"

    guild = bot.get_guild(guild_id)
    channels = guild.channels
    for channel in channels:
        if isinstance(channel, disnake.TextChannel) or isinstance(channel, disnake.VoiceChannel):
            await channels.set_permissions(guild.default_role, read_messages=False)
            print(f"The channel {channel.name} a ete bloquer avec succes")


bot.run(token)