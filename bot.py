import discord
from cogs.general import General
from cogs.roles import Roles
from cogs.gifs import Gifs
from cogs.nsfw import NSFW
from discord.ext import commands
from utils.general import get_gif_url, get_member_name

context_type = commands.context.Context

async def create_bot(
        cmd_prefix: str = '$',
        intents: discord.Intents = discord.Intents.all(),
        activity: str = "Listening to you.",
        status: discord.Status = discord.Status.idle
):
    bot = commands.Bot(
        command_prefix=cmd_prefix,
        intents=intents,
        case_insensitive=True,
        strip_after_prefix=True
    )

    bot.activity = discord.CustomActivity(activity)
    bot.status = status

    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            await guild.system_channel.send("Hi I'm online now.")

    @bot.event
    async def on_member_join(member: discord.Member):
        await member.guild.system_channel.send(f"Welcome {get_member_name(member)}!")
        await member.guild.system_channel.send(get_gif_url("welcome funny", get_member_name(member)))

    await load_cogs(bot)
    return bot

async def load_cogs(bot: commands.Bot):
    await bot.add_cog(General(bot))
    await bot.add_cog(Roles(bot))
    await bot.add_cog(Gifs(bot))
    await bot.add_cog(NSFW(bot))
