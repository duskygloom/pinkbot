import discord
import importlib

from discord.ext import commands
from discord.app_commands import AppCommand

import cli

from utils.config import get_config
from utils.logger import get_logger
from utils.general import is_developer

logger = get_logger("cogs.development")
version_config = get_config()["version"]


def is_developer_context(ctx: commands.Context):
    return is_developer(ctx.author)


class Development(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def respond(self, ctx: commands.Context, message: str):
        await ctx.reply(message, ephemeral=True, mention_author=False)

    async def search_app_command(self, name: str, guild: discord.Guild = None) -> AppCommand | None:
        '''
        Parameters
        ----------
        name    : name of the command to be searched
        guild   : guild where name is to be searched

        Returns
        -------
        AppCommand if any app command has been found
        of the given name.
        Returns None if not found.
        '''
        command = None
        app_commands = await self.bot.tree.fetch_commands(guild=guild)
        for app_command in app_commands:
            if app_command.name == name:
                return app_commands
        return None
    
    @commands.command(name="reload", description="Reloads commands.")
    @commands.check(is_developer_context)
    async def reload(self, ctx: commands.Context):
        for cog in version_config["cogs"]:
            await self.bot.reload_extension(cog)
            logger.debug(f"Reloaded extension: {cog}")
        await self.respond(ctx, "Extensions loaded.")
    
    @commands.command(name="sync", description="Syncs commands.")
    @commands.check(is_developer_context)
    async def sync(self, ctx: commands.Context):
        synced = await self.bot.tree.sync()
        logger.info(f"Synced {len(synced)} commands.")
        await self.respond(ctx, f"Synced {len(synced)} commands.")

    @commands.command(name="add", description="Adds a slash command.")
    @commands.check(is_developer_context)
    async def add(self, ctx: commands.Context, name: str):
        await self.reload(ctx)
        app_command = await self.search_app_command(name)
        if not app_command:
            await self.respond(ctx, f"No app command found: {name}")
            return
        self.bot.tree.add_command(app_command)
        await self.respond(ctx, f"New command added: {name}")
        logger.info(f"New command added: {name}")

    @commands.command(name="remove", description="Removes a slash command.")
    @commands.check(is_developer_context)
    async def remove(self, ctx: commands.Context, name: str):
        app_command = await self.search_app_command(name)
        if not app_command:
            await self.respond(ctx, f"No app command found: {name}")
            return
        self.bot.tree.remove_command(name)
        await self.respond(ctx, f"Command removed: {name}")
        logger.info(f"Command removed: {name}")

    @commands.command(name="run", description="Runs runner script.")
    @commands.check(is_developer_context)
    async def run(self, ctx: commands.Context):
        importlib.reload(cli)
        await cli.runner(ctx)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Development(bot))
