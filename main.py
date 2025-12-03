import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("shutupbotlogs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ShutUpBot")

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class ShutUpBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        initial_extensions = ['cogs.events', 'cogs.commands']
        
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")

        await self.tree.sync()
        logger.info("Command tree synced.")

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')

bot = ShutUpBot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await interaction.response.send_message(f'Slow down, dude. Wait like {error.retry_after:.2f} seconds lol.')
    else:
        logger.error(f'Command error detected: {error}')
        try:
            await interaction.response.send_message("Something broke. SHUT UP and try again LATER.")
        except:
            pass

token = os.getenv("TOKEN")
if not token:
    logger.critical("TOKEN not found in environment variables.")
else:
    bot.run(token)