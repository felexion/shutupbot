import discord
import random
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
VERSION = "v.1.0.3.rc3"
VERSION_DESCRIPTION = "better helpcommand response"
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

    embed = discord.Embed(
        title=f"Shut Up Bot {VERSION}",
        description="This bot tells you to shut up!"
    )
    embed.add_field(
        name="Version Info",
        value=f"{VERSION_DESCRIPTION}",
        inline=False
    );

    embed.add_field(
        name="Source Code",
        value="[GitHub Repository](YOUR_GITHUB_LINK_HERE)",
        inline=False
    )

    embed.add_field(
        name="Privacy Policy",
        value="I don't collect your data. LMAO. XD. Fixing commit errors right now.",
        inline=False
    )

    embed.set_footer(text="No, I will not help you")
    await interaction.response.send_message(embed=embed)


token = os.getenv("TOKEN")
client.run(token)