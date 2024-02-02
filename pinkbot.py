import discord

from discord.ext import commands

from utils.roles import RolesView
from utils.config import get_config
from utils.logger import get_logger

config = get_config()
bot_config = config["bot"]
version_config = config["version"]

logger = get_logger("bot")


class Pinkbot(commands.Bot):
    def __init__(self, prefix: str, description: str):
        intents = discord.Intents.all()
        super().__init__(prefix, description=description, intents=intents)
        self.activity = discord.CustomActivity(
            bot_config["activity"],
            emoji=bot_config["emoji"]
        )

    async def setup_hook(self):
        async for guild in self.fetch_guilds():
            roles = await guild.fetch_roles()
            self.add_view(RolesView(roles))

    async def on_ready(self):
        logger.info(f"{self.user.name} is ready.")
        # status and activity
        self.status = discord.Status.idle
        # emoji
        activity = bot_config["activity"]
        emoji = bot_config["emoji"]
        self.activity = discord.CustomActivity(activity, emoji=emoji)
        # loading cogs
        for cog in version_config["cogs"]:
            await self.load_extension(cog)
            logger.debug(f"Loaded extension: {cog}")
        # checking all the guilds
        async for guild in self.fetch_guilds():
            if version_config["config"] == "RELEASE" and bot_config["greeting"]:
                await guild.system_channel.send(bot_config["greeting"])
            logger.info(f"{self.user.name} reached {guild.name}.")
            