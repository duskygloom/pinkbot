import discord
from datetime import datetime

from utils.config import get_config

config = get_config()
bot_config = config["bot"]
version_config = config["version"]


class FakeSnowflake:
    def __init__(self, id: int):
        self.id = id


def get_member_name(member: discord.Member) -> str:
    return member.nick or member.display_name


def is_admin(user: discord.Member|discord.User) -> bool:
    if isinstance(user, discord.User):
        return is_developer(user)
    return user.guild_permissions.administrator


def is_developer(user: discord.Member|discord.User) -> bool:
    return user.id == version_config["developer_id"]


async def default_response(interaction: discord.Interaction):
    # await interaction.response.send_message("Done.", ephemeral=True, delete_after=1)
    await interaction.response.defer(ephemeral=True, thinking=False)


def get_member_embed(member: discord.Member) -> discord.Embed:
    embed = discord.Embed(
        title=member.name,
        colour=discord.Colour.from_str(bot_config["colour"])
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(
        name="Joined on",
        value=member.joined_at.strftime("%d-%m-%Y"),
    )
    return embed
