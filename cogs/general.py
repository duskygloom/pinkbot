import asyncio
import discord

from discord import app_commands
from discord.ext import commands

from datetime import datetime

from utils.config import get_config
from utils.logger import get_logger
from utils.general import is_admin
from utils.general import is_developer

logger = get_logger("cogs.general")
config = get_config()


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="say", description="Ping pinkbot.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(config["general"]["ping_message"])

    @app_commands.command(name="spam", description="Pinkbot spams a message.")
    async def spam(self, interaction: discord.Interaction, text: str, number: int):
        if number > config["general"]["admin_spam_limit"] and is_admin(interaction.user):
            number = config["general"]["admin_spam_limit"]
        elif number > config["general"]["common_spam_limit"]:
            number = config["general"]["common_spam_limit"]
        await interaction.response.defer()
        for _ in range(number):
            await interaction.channel.send(text)
            await asyncio.sleep(1)
        await interaction.followup.send(f"Spammed {number} times.")

    @commands.command(name="sleep", description="Pinkbot goes offline.")
    async def sleep(self, ctx: commands.Context, reason: str = ""):
        # only developers can shutdown in DM
        if isinstance(ctx.channel, discord.DMChannel) and is_developer(ctx.author):
            await ctx.reply(
                "This command can only be executed by the developers.",
                mention_author=False
            )
            return
        # only administrators can shutdown in server
        if not is_admin(ctx.author):
            await ctx.reply(
                "This command can only be executed by administrators.",
                mention_author=False
            )
            return
        # actual closing
        with open(config["general"]["sleep_reason"], "w") as f:
            f.write(f"{datetime.now().isoformat()} -> {ctx.author}: {reason}")
        await ctx.reply("Be right back.", mention_author=False)
        await self.bot.close()


@app_commands.context_menu(name="Delete message.")
async def delete_message(
        interaction: discord.Interaction,
        message: discord.Message
):
    if message.author != interaction.client.user:
        await interaction.response.send_message(
            "Cannot delete other people's message.",
            ephemeral=True,
            delete_after=1
        )
        return
    await message.delete()
    await interaction.response.send_message("Deleted.", ephemeral=True, delete_after=1)


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
    bot.tree.add_command(delete_message)
