import discord

from discord.ext import commands

from utils.general import get_member_embed


async def runner(ctx: commands.Context, member_id: str):
    '''
    Info
    ----
    This function can be used to execute code
    on behalf of pinkbot.

    Note
    ----
    Ensure that cli is reimported before
    using this function.
    '''
    member = ctx.guild.get_member(int(member_id))
    await ctx.send(embed=get_member_embed(member))
