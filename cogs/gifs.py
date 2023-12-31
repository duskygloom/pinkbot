import discord, typing
from discord.ext import commands
from utils.general import get_gif_url, get_member_name

context_type = commands.Context

class Gifs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.command(
            name="tenor",
            description="Let's send a gif!",
            usage="$tenor topic of the gif [@person]",
            brief="Sends renor gif to others.",
            help="Sends gif related to topic from tenor to the person or just to the channel."
    )
    async def tenor(self, ctx: context_type, recipent: typing.Optional[discord.Member], *, topic: str = ""):
        topic = topic.strip()
        url = get_gif_url(topic, get_member_name(ctx.author))
        if url == "":
            await ctx.reply("Could not find any gifs of that topic.", mention_author=False)
            return
        if recipent is not None:
            await ctx.send(recipent.mention)
        await ctx.send(url)