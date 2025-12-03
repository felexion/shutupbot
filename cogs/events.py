import discord
from discord.ext import commands
import random
import time
import logging
import config

logger = logging.getLogger("ShutUpBot")

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_spam_tracker = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if message.guild is None:
            return
        
        current_time = time.time()
        last_time = self.user_spam_tracker.get(message.author.id, 0)

        if current_time - last_time < config.SPAM_COOLDOWN_SECONDS:
            return
        
        triggered = False

        if message.reference and message.reference.resolved:
            replied_message = message.reference.resolved
            if replied_message.author == self.bot.user:
                await message.reply("Just shut up!")
                logger.info("Replied to a user who replied to bot.")
                return
            
        elif self.bot.user in message.mentions:
            await message.reply("Shut up!")
            logger.info("Replied to mention from a user.")
            triggered = True

        else:
            rand_val = random.randint(1, 100)
            if rand_val == 1:
                await message.reply("YOU REALLY NEED TO SHUT UP!")
                logger.info(f'Hit 1% Trigger')
                triggered = True

            elif rand_val <= 11:
                await message.reply("Shut up!")
                logger.info(f'Hit 10% Trigger')
                triggered = True

        if triggered:
            self.user_spam_tracker[message.author.id] = current_time

async def setup(bot):
    await bot.add_cog(Events(bot))