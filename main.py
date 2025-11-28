import discord
import random
import os
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()
VERSION = "v1.1.3"
VERSION_DESCRIPTION = "Added Docker files to repo"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class ShutUpBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=1397259714298908772)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

client = ShutUpBot()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if random.randint(1, 10) == 1:
        await message.reply("Shut up!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if random.randint(1, 100) == 1:
        await message.reply("You really need to shut the f--- up!")

@client.tree.command(name="shut", description="Tells you to shut up!")
async def self_shut_up(interaction: discord.Interaction):
    msg = (
        "Shut up!"
    )
    await interaction.response.send_message(msg)


@client.tree.command(name="help", description="Show how the bot works")
async def help_command(interaction: discord.Interaction):
    msg = (
        f"shut up bot {VERSION} by forcerex\n"
        f"Version Description: {VERSION_DESCRIPTION}\n"
        "this bot will tell you to shut up!!!!!\n"
        "no, i will not help you."
    )
    await interaction.response.send_message(msg)

token = os.getenv("TOKEN")
client.run(token)