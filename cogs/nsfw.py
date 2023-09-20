import typing, logging, discord, asyncio
from discord.ext import commands
from utils.onlyfans import *

context_type = commands.Context

class NSFW(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(
            name="onlyfans",
            description="Sending onlyfans content~",
            usage="$onlyfans [post] [timeout] 'username'",
            brief="Sends onlyfans posts.",
            help="Sends onlyfans post of username."
    )
    async def onlyfans(self, ctx: context_type, post: typing.Optional[int] = 1, timeout: typing.Optional[int] = 60, *, username: str = ""):
        await ctx.message.add_reaction('⏳')
        if username == "":
            username = get_random_username()
        codes = generate_code(username, post)
        # handling abnormal conditions
        if codes == ScrappingStatus.username_not_found:
            await ctx.reply(f"Could not find the user: {username}.", mention_author=False)
            return
        elif codes == ScrappingStatus.website_not_found:
            await ctx.reply(f"Could not find website.", mention_author=False)
            return
        elif codes == ScrappingStatus.could_not_connect:
            await ctx.reply(f"Could not connect to the website.", mention_author=False)
            return
        await ctx.message.remove_reaction('⏳', member=self.bot.user)
        await ctx.message.add_reaction('😇')
        # yielding codes
        try:
            keep_running = True
            check_reaction = lambda reaction, member:  reaction.emoji in ['⏹️', '▶️'] and member == ctx.author
            thread = await ctx.channel.create_thread(name=username, type=discord.ChannelType.private_thread, )
            while keep_running:
                code = next(codes)
                videos, images = get_post(username, code)
                # sending messages to private thread
                await thread.add_user(ctx.author)
                for url in videos:
                    await thread.send(url)
                for url in images:
                    await thread.send(url)
                message: discord.Message = await thread.send(f"Found {len(videos)} videos.\nFound {len(images)} images.")
                post_id = message.id
                # reaction controls
                await message.add_reaction('⏹️')
                await message.add_reaction('▶️')
                await asyncio.sleep(0.1)
                await self.bot.wait_for("reaction_add", check=check_reaction, timeout=timeout)
                message = await thread.fetch_message(post_id)
                message_reactions = message.reactions
                for reaction in message_reactions:
                    has_reacted = await is_reactor(ctx.author, reaction)
                    if has_reacted and reaction.emoji == '⏹️':
                        keep_running = False
                    elif has_reacted and reaction.emoji == '▶️':
                        code = next(codes)
        except StopIteration:
            await ctx.reply("No more posts.", mention_author=False)
        finally:
            await ctx.message.remove_reaction('😇', member=self.bot.user)
            await ctx.message.add_reaction('✅')

    @onlyfans.error
    async def onlyfans_error(self, ctx: context_type, error: discord.DiscordException):
        logging.error(error)
        await ctx.message.remove_reaction('😇', member=self.bot.user)
        await ctx.message.add_reaction('✅')
