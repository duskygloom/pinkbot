import discord

from utils.config import get_config
from utils.general import FakeSnowflake
from utils.logger import get_logger

logger = get_logger("utils.roles")
roles_config = get_config()["roles"]


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, emoji: str):
        super().__init__(
            label=role.name,
            emoji=emoji,
            style=discord.ButtonStyle.secondary,
            custom_id=f"button_{role.name}"
        )
        self.role = role
    
    async def callback(self, interaction: discord.Interaction):
        role = await fetch_role(interaction.guild, self.role.id)
        if interaction.user in role.members:
            await interaction.user.remove_roles(role)
            message = f"You have been removed from {role.name}."
        else:
            await interaction.user.add_roles(role)
            message = f"You have been added to {role.name}."
        await interaction.response.send_message(message, ephemeral=True, delete_after=1)


class RolesView(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        # inverting roles_emoji dict into roles_id
        roles_emoji = roles_config["emoji"]
        roles_id = {
            role_id : emoji
            for (role_id, emoji) in zip(roles_emoji.values(), roles_emoji.keys())
        }
        # add role buttons
        for role in roles:
            if role.id not in roles_id:
                continue
            self.add_item(RoleButton(role, roles_id[role.id]))


async def fetch_role(guild: discord.Guild, role_id: int) -> discord.Role:
    '''
    Returns
    -------
    If any role in the guild has an id matching role_id,
    returns the role.
    Else returns None.
    '''
    roles = await guild.fetch_roles()
    for role in roles:
        if role.id == role_id:
            return role
    return None


async def add_member(
        guild: discord.Guild,
        emoji: str,
        member: discord.Member
):
    # getting role
    role_id = roles_config["emoji"][emoji]            
    role = await fetch_role(guild, role_id)
    if not role:
        logger.error(f"Invalid role: {role_id}")
        return
    # adding role to members
    if role in member.roles:
        logger.debug(f"{member.name} is already in {guild.name}/{role.name}")
        return
    await member.add_roles(FakeSnowflake(role_id))
    logger.debug(f"{member.name} was added to {guild.name}/{role.name}")


async def remove_member(
        guild: discord.Guild,
        emoji: str,
        member: discord.Member
):
    # getting role
    role_id = roles_config["emoji"][emoji]
    role = await fetch_role(guild, role_id)
    if not role:
        logger.error(f"Invalid role: {role_id}")
        return
    # removing role from members
    if role not in member.roles:
        logger.debug(f"{member.name} is not in {guild.name}/{role.name}")
        return
    await member.remove_roles(role)
    logger.debug(f"{member.name} was removed from {guild.name}/{role.name}")
