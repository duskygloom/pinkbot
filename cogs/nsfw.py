import typing
import discord

from discord import app_commands
from discord.ext import commands

from utils.coomer import get_posts
from utils.coomer import PaginationView
from utils.coomer import get_creator_posts
from utils.coomer import get_random_creator
from utils.coomer import get_matching_creators

homepage = "https://coomer.su"


def check_nsfw_channel(interaction: discord.Interaction) -> bool:
    is_dm_channel = isinstance(interaction.channel, discord.DMChannel)
    return is_dm_channel or interaction.channel.is_nsfw()


class NSFW(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(
        name="random_creator",
        description="A random onlyfans or fansly creator."
    )
    @app_commands.check(check_nsfw_channel)
    async def random_creator(self, interaction: discord.Interaction):
        await interaction.response.defer()
        creator = await get_random_creator()
        await interaction.followup.send(embed=creator.get_embed())
    
    @app_commands.command(
        name="search_creator",
        description="Search for creators."
    )
    @app_commands.check(check_nsfw_channel)
    async def search_creator(
            self,
            interaction: discord.Interaction,
            id: str = "",
            name: str = "",
            limit: int = 10,
            offset: int = 0
    ):
        await interaction.response.defer()
        creators = await get_matching_creators(id, name)
        creators = creators[offset:offset+limit]
        if len(creators) == 0:
            await interaction.followup.send("No such creator found.")
            return
        await interaction.followup.send(
            f"Creators: 1/{len(creators)}",
            embed=creators[0].get_embed(),
            view=PaginationView(creators)
        )

    @app_commands.command(
        name="search_post",
        description="Search for posts."
    )
    @app_commands.check(check_nsfw_channel)
    async def search_post(
            self,
            interaction: discord.Interaction,
            query: str = "",
            limit: int = 10,
            offset: int = 0,
            page: int = 1
    ):
        await interaction.response.defer()
        posts = await get_posts(query, page-1)
        posts = posts[offset:offset+limit]
        if len(posts) == 0:
            await interaction.followup.send("No such post found.")
            return
        message = f"1/{len(posts)}"
        for attachment in posts[0].attachments["path"]:
            message += f"\n{homepage}{attachment}"
        await interaction.followup.send(
            content=message,
            embed=posts[0].get_embed(),
            view=PaginationView(posts)
        )

    @app_commands.command(
        name="search_creator_post",
        description="Search for posts of a creator."
    )
    @app_commands.check(check_nsfw_channel)
    async def search_creator_post(
            self,
            interaction: discord.Interaction,
            creator_id: str,
            service: typing.Literal["onlyfans", "fansly"],
            query: str = "",
            limit: int = 10,
            offset: int = 0,
            page: int = 1
    ):
        await interaction.response.defer()
        posts = await get_creator_posts(query, creator_id, service, page-1)
        posts = posts[offset:offset+limit]
        if len(posts) == 0:
            await interaction.followup.send("No such post found.")
            return
        message = f"1/{len(posts)}"
        for attachment in posts[0].attachments["path"]:
            message += f"\n{homepage}{attachment}"
        await interaction.followup.send(
            content=message,
            embed=posts[0].get_embed(),
            view=PaginationView(posts)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(NSFW(bot))
