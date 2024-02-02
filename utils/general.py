import discord

from utils.config import get_config

version_config = get_config()["version"]


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
