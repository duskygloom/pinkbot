import discord, logging
from discord.ext import commands
from utils import get_member_name

context_type = commands.Context

class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="assign_roles", 
             description="Assign roles to others... if you are permitted to.",
             usage="$assign_roles member1 member2 ... role1 role2 ...",
             brief="Assign roles to others.",
             help="Assign roles to others, if only you are permitted to modify roles yourself.")
    async def assign_roles(
            self, ctx: context_type, 
            members: commands.Greedy[discord.Member], 
            roles: commands.Greedy[discord.Role]
    ):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.reply(f"You don't have the permission to manage roles, {get_member_name(ctx.author)}.", mention_author=False)
            return
        for member in members:
            for role in roles:
                await member.add_roles(role)
            await ctx.reply(f"Successfully assigned role(s) to {get_member_name(member)}.", mention_author=False)

    @assign_roles.error
    async def assign_roles_error(self, ctx: context_type, error: discord.DiscordException):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.reply("Invalid member.", mention_author=False, delete_after=5)
        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.reply("Invalid role.", mention_author=False, delete_after=False)
        else:
            logging.error(error)

    @commands.command(name="remove_roles", 
                description="Removes roles from others... if you are permitted to.",
                usage="$remove_roles member1 member2 ... role1 role2 ...",
                brief="Removes roles from others.",
                help="Removes roles from others, if only you are permitted to modify roles yourself.")
    async def remove_roles(
            self, ctx: context_type, 
            members: commands.Greedy[discord.Member], 
            roles: commands.Greedy[discord.Role]
    ):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.reply(f"You don't have the permission to manage roles.", mention_author=False)
        for member in members:
            for role in roles:
                await member.remove_roles(role)
            await ctx.reply(f"Successfully removed role(s) from {get_member_name(member)}.", mention_author=False)            

    @remove_roles.error
    async def remove_roles_error(self, ctx: context_type, error: discord.DiscordException):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.reply("Invalid member.", mention_author=False, delete_after=5)
        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.reply("Invalid role.", mention_author=False, delete_after=5)
        else:
            logging.error(error)

    @commands.command(
            name="create_roles",
            usage="create_roles 'role 1' 'role 2' 'role 3' ...",
            description="Let me spawn some roles real quick.",
            brief="Creates roles of the same names.",
            help="Creates roles of the same names."
    )
    async def create_roles(self, ctx: context_type, *names: str):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.reply("You don't have the permissions to manage roles.", mention_author=False)
            return
        roles = await ctx.guild.fetch_roles()
        for name in names:
            role_exists = False
            for role in roles:
                if role.name == name:
                    role_exists = True
                    await ctx.reply(f"Role '{name}' already exists.", mention_author=False)
                    break
            if not role_exists:
                await ctx.guild.create_role(name=name)
        await ctx.message.add_reaction('✅')
    
    @commands.command(
            name="delete_roles",
            usage="delete_roles role1 role2 role3 ...",
            description="Roles go poof.",
            brief="Deletes the mentioned roles.",
            help="Deletes the mentioned roles."
    )
    async def delete_role(self, ctx: context_type, roles: commands.Greedy[discord.Role]):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.reply("You don't have the permissions to manage roles.", mention_author=False)
            return
        for role in roles:
            await role.delete()
        await ctx.message.add_reaction('✅')
        
