import os
import typing
import discord

from discord import app_commands
from discord.ext import commands

from utils import giphy
from utils import tenor
from utils.config import get_config
from utils.general import get_member_name
from utils.stickers import get_sticker_path
from utils.logger import get_logger

logger = get_logger("cogs.stickers")
stickers_config = get_config()["stickers"]

gif_source_t = typing.Literal["giphy", "tenor"]


class Stickers(commands.Cog):
    '''
    Info
    ----
    Sticker cog.
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="gif",
        description="Pinkbot sends a random gif of the given query."
    )
    async def gif(
            self,
            interaction: discord.Interaction,
            source: gif_source_t,
            query: str
    ):
        if source == "giphy":
            giphy_gif = giphy.get_random_gif(query, interaction.user.name)
            if giphy_gif:
                await interaction.response.send_message(giphy_gif)
                return
        tenor_gif = tenor.get_random_gif(query, get_member_name(interaction.user))
        if tenor_gif:
            await interaction.response.send_message(tenor_gif)
            return
        await interaction.response.send_message("No such gif found.")


    @app_commands.command(
        name="add_sticker",
        description="Add a sticker to pinkbot."
    )
    async def add_sticker(self, interaction: discord.Interaction, name: str, attachment: discord.Attachment):
        original_name = attachment.filename
        if get_sticker_path(name):
            await interaction.response.send_message("Sticker already exists.")
            return
        extension = original_name[original_name.rfind("."):]
        if extension not in stickers_config["extensions"]:
            message = "Attachment does not have a valid extension.\n"
            message += f"Valid extensions: {stickers_config['extensions']}"
            await interaction.response.send_message(message)
            return
        name = name.strip() + extension
        await interaction.response.defer()
        await attachment.save(os.path.join(stickers_config["path"], name))
        await interaction.followup.send(f"Sticker added: {name}")

    @app_commands.command(
        name="remove_sticker",
        description="Removes a sticker from pinkbot."
    )
    async def remove_sticker(self, interaction: discord.Interaction, sticker: str):
        sticker = os.path.basename(sticker)
        name = os.path.join(stickers_config["path"], sticker)
        if not os.path.exists(name) and sticker not in os.listdir(stickers_config["path"]):
            await interaction.response.send_message("No such sticker found.")
            return
        os.remove(name)
        await interaction.response.send_message(f"Deleted sticker: {name}")

    @remove_sticker.autocomplete("sticker")
    async def remove_sticker_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        stickers = [
            os.path.basename(name)
            for name in os.listdir(stickers_config["path"])
        ]
        return [
            app_commands.Choice(name=os.path.basename(name), value=name)
            for name in os.listdir(stickers_config["path"])
            if current.lower() in name.lower()
        ]

    @app_commands.command(
        name="sticker",
        description="Pinkbot sends a sticker."
    )
    async def sticker(self, interaction: discord.Interaction, sticker: str):
        name = os.path.join(stickers_config["path"], sticker)
        if not os.path.exists(name):
            await interaction.response.send_message("No such sticker found.")
            return
        await interaction.response.defer()
        await interaction.followup.send(file=discord.File(name), ephemeral=False)

    @sticker.autocomplete("sticker")
    async def sticker_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=os.path.basename(name), value=name)
            for name in os.listdir(stickers_config["path"])
            if current.lower() in name.lower()
        ]


async def setup(bot: commands.Bot):
    await bot.add_cog(Stickers(bot))
