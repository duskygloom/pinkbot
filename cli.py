import discord

from discord.ext import commands


async def runner(ctx: commands.Context):
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
    await ctx.send(str(isinstance(ctx.channel, discord.DMChannel)))
