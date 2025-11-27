import discord
import random
import os
import logging
import time
from discord import app_commands
from dotenv import load_dotenv

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',

    handlers = [

        logging.FileHandler("shutupbotlogs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ShutUpBot")

load_dotenv()
VERSION = "v.1.1.1"
VERSION_DESCRIPTION = "Logging system improved. Added spam cooldown. Added some stuff on gitignore"

SPAM_COOLDOWN_SECONDS = 5.0
user_spam_tracker = {}

intents = discord.Intents.default()
intents.message_content = True

class shutUpBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        logger.info("Command tree synced.")

client = shutUpBot()

@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.respond.send_message(f'Slow down, dude. Wait like {error.retry_after:.2f} seconds lol.')
    else:
        logger.error(f'Command error detected: {error}')
        try:
            await interaction.response.send_message("Something broke. SHUT UP and try again LATER.")
        except:
            pass

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user} (ID: {client.user.id})')
    logger.info(f'Running version {VERSION}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.guild is None:
        return

    current_time = time.time()
    last_time = user_spam_tracker.get(message.author.id, 0)

    if current_time - last_time < SPAM_COOLDOWN_SECONDS:
        return
    
    triggered = False

    if message.reference and message.reference.resolved:
        replied_message = message.reference.resolved
        if replied_message.author == client.user:
            await message.reply("Just shut up!")
            logger.info(f'Replied to a user who replied to bot.')
            return    

    elif client.user in message.mentions:
        await message.reply("Shut up!")
        logger.info("Replied to mention from a user.")
        triggered = True

    else:
        rand_val = random.randint(1, 100)

        if rand_val == 1:
            await message.reply("YOU REALLY NEED TO SHUT UP!")
            logger.info(f'Hit 1% trigger')
            triggered = True

        elif rand_val <= 11:
            await message.reply("Shut up!")
            logger.info(f'Hit 10% trigger')
            triggered = True

    if triggered:
        user_spam_tracker[message.author.id] = current_time

@client.tree.command(name="shut", description="Tells you to shut up!")
@app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
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
        value="[Shut Up Bot on GitHub](https://github.com/felexion/shutupbot)",
        inline=False
    )

    embed.add_field(
        name="Privacy Policy",
        value="I don't collect your data, dw.",
        inline=False
    )

    embed.set_footer(text="No, I will not help you")
    await interaction.response.send_message(embed=embed)


token = os.getenv("TOKEN")
if not token:
    logger.critical("TOKEN not found in environment variables.")
else:
    client.run(token)
