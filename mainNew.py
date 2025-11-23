import discord
import random
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
VERSION = "v.1.0.3.rc2"
VERSION_DESCRIPTION = "mention and reply detection added."
# TODO: add error messages
# TODO: add avoiding replying in dms
# TODO: add rate-limit handling if spammy
# TODO: improve logging system

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
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.reference and message.reference.resolved:
        replied_message = message.reference.resolved
        if replied_message.author == client.user:
            await message.reply("Just shut up!")
            print("Bot was replied. Told user to shut up.")
            return    

    if client.user in message.mentions:
        await message.reply("Shut up!")
        print("Bot was mentioned. Told user to shut up.")
        return

    rand_val = random.randint(1, 100)

    if rand_val == 1:
        await message.reply("YOU REALLY NEED TO SHUT UP!")
        print("The bot said YOU REALLY NEED TO SHUT UP!")

    elif rand_val <= 11:
        await message.reply("Shut up!")
        print("The bot said Shut up!")

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