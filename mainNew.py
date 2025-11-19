import discord
import random
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
VERSION = "v.1.0.2"
VERSION_DESCRIPTION = "New Code!"

intents = discord.Intents.default()
intents.message_content = True

class shutUpBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = shutUpBot()

@client.event
async def onReady():
    print(f'Logged in as {client.user}!')

@client.event
async def onMessage(message):
    if message.author == client.user:
        return
    
    if random.randint(1, 10) == 1:
        await message.reply("Shut up!")

    elif random.randint(1, 100) == 1:
        await message.reply("YOU REALLY NEED TO SHUT UP!")

@client.tree.command(name="shut", description="Tells you to shut up!")
async def shutCommand(interaction: discord.Interaction):
    await interaction.response.send_message("Shut up!")

@client.tree.command(name="help", description="Show how the bot works.")
async def helpCommand(interaction: discord.Interaction):
    msg = (
        f"Shut Up Bot {VERSION} by felexion\n"
        f"Version Description: {VERSION_DESCRIPTION}\n"
        "This bot will tell you to shut up randomly!\n"
        "No, I will not help you."
    )
    await interaction.response.send_message(msg)


token = os.getenv("TOKEN")
client.run(token)