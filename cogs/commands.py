# cogs/commands.py
import discord
from discord import app_commands
from discord.ext import commands
import config

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shut", description="Tells you to shut up!")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def shut_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Shut up!")

    @app_commands.command(name="help", description="Show how the bot works.")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Shut Up Bot {config.VERSION}",
            description="This bot tells you to shut up!"
        )
        embed.add_field(
            name="Version Info",
            value=f"{config.VERSION_DESCRIPTION}",
            inline=False
        )
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

async def setup(bot):
    await bot.add_cog(Commands(bot))