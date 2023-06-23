import disnake
from disnake.ext import commands
import json
import os

config_file_path = "config.json"

if not os.path.exists(config_file_path):
    config_data = {
        "TOKEN": "your_token_here",
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
    name="maintenance",
    description="Set the server in maintenance"
)
async def maintenance(ctx: disnake.ApplicationCommandInteraction, msg: str = None):
    if ctx.author.id != you:
        await ctx.send("You can't do that", delete_after=3)
        return

    if msg is None:
        msg = "Aucune info n'est donnée"

    guild = bot.get_guild(guild_id)
    channels = guild.channels
    for channel in channels:
        if isinstance(channel, disnake.TextChannel) or isinstance(channel, disnake.VoiceChannel):
            await channel.set_permissions(guild.default_role, read_messages=False)
            print(f"The channel {channel.name} a été bloqué avec succès")

    chan = await guild.create_text_channel("soon")
    new_msg = await chan.send(f"{msg}\n@everyone")
    await new_msg.pin()

bot.run(token)