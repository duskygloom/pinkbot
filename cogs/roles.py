import discord

from discord import app_commands
from discord.ext import commands

from utils.roles import RolesView
from utils.config import get_config
from utils.logger import get_logger

logger = get_logger("cogs.roles")
roles_config = get_config()["roles"]


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
            
    @app_commands.command(
        name="send_roles",
        description="Sends a new message for managing roles."
    )
    @app_commands.default_permissions(manage_guild=True)
    async def send_roles(self, interaction: discord.Interaction):
        try:
            roles_channel = await interaction.guild.fetch_channel(roles_config["channel"])
        except discord.errors.NotFound:
            message = f"Channel not found: {interaction.guild.name}/{roles_config['channel']}"
            await interaction.response.send_message(message, ephemeral=True)
            return
        roles = await interaction.guild.fetch_roles()
        message = "Select role to join or leave."
        await roles_channel.send(message, view=RolesView(roles))
        await interaction.response.send_message("Sent.", ephemeral=True, delete_after=1)

async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
