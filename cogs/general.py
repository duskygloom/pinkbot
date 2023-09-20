import typing, asyncio, datetime, logging, discord
from discord.ext import commands

context_type = commands.Context

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.command(
            name="echo", 
            description="Make me say anything.",
            usage="$echo what to repeat ...",
            brief="Repeat before me.",
            help="The bot repeats what you say."
    )
    async def echo(self, ctx: context_type, *, text: str = "Hi"):
        await ctx.reply(text, mention_author=False)

    @commands.command(
            name="request", 
            description="Need something else? Ask it, maybe I can help.",
            usage="$request feature continues ...",
            brief="Request for a new feature.",
            help="Ask the developers for a new feature."
    )
    async def request(self, ctx: context_type, *, text: str = ""):
        text = text.strip()
        if text == "":
            return
        with open("feature_requests.txt", "a") as f:
            f.write(f"{ctx.author}: {text}\n")
        await ctx.reply("Sent your request to the developers.", mention_author=False)

    @request.error
    async def request_error(self, ctx: context_type, error: discord.DiscordException):
        logging.error(error)
    
    @commands.command(
            name="feedback", 
            description="Facing any issues?",
            usage="$feedback feedback continues ...",
            brief="Send a feedback.",
            help="Send a feedback to the developers."
    )
    async def feedback(self, ctx: context_type, *, text: str = ""):
        with open("feedback.txt", "a") as f:
            f.write(f"{ctx.author}: {text}\n")
        await ctx.reply("Sent your feedback to the developers.", mention_author=False)

    @feedback.error
    async def feedback_error(self, ctx: context_type, error: discord.DiscordException):
        logging.error(error)

    @commands.command(
            name="spam",
            description="I repeat you... but 10 times max!",
            usage="$spam [number] what to spam",
            brief="Spam helper.",
            help="Repeats the text maximum of 10 times."
    )
    async def spam(self, ctx: context_type, number: typing.Optional[int] = 10, *words: str):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("Only administrators are allowed to spam!")
            return
        if len(words) == 0:
            return
        if number > 10:
            number = 10
        await ctx.message.add_reaction('⏳')
        sentence = ' '.join(words)
        for i in range(number):
            await ctx.send(sentence)
            await asyncio.sleep(0.1)
        await ctx.message.remove_reaction('⏳', member=self.bot.user)
        await ctx.message.add_reaction('✅')

    @spam.error
    async def spam_error(self, ctx: context_type, error: discord.DiscordException):
        logging.error(error)

    @commands.command(
            name="sleep",
            description="Goodnight zzzZZZ",
            usage="$sleep [reason for making the bot offline]",
            brief="Bot goes offline.",
            help="Bot goes offline."
    )
    async def sleep(self, ctx: context_type, *, reason: str = "No reason specified."):
        if ctx.author.guild_permissions.administrator:
            with open("sleep_reason.txt", "w") as f:
                f.write(f"{datetime.datetime.now().isoformat()} -> {ctx.author}: {reason}")
            await ctx.reply("Byee~", mention_author=False)
            await self.bot.close()
        else:
            await ctx.reply("You are not an administrator.", mention_author=False)

    @sleep.error
    async def sleep_error(self, ctx: context_type, error: discord.DiscordException):
        logging.error(error)

    @commands.command(
            name="delete",
            description="Oops lemme delete that-",
            usage="<reply to the message you want to unsend> $delete [reason for deleting]",
            brief="Deletes the message you reply to.",
            help="Deletes the message you reply to."
    )
    async def delete(self, ctx: context_type, *, reason: str = "No reason specified."):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.reply("You don't have permission to manage messages.", mention_author=False)
            return
        reference_id = ctx.message.reference.message_id
        reference_msg = await ctx.channel.fetch_message(reference_id)
        with open("deleted_messages.txt", "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()} {ctx.author}\n{reference_msg.author} at {reference_msg.created_at.isoformat()}: {reference_msg.content}\n")
        await reference_msg.delete()
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=4)
    
    @delete.error
    async def delete_error(self, ctx: context_type, error: discord.DiscordException):
        logging.error(error)
