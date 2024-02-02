import random
import aiohttp
import discord

from utils.config import get_config
from utils.logger import get_logger
from utils.general import default_response

bot_config = get_config()["bot"]

logger = get_logger("utils.coomer")

homepage = "https://coomer.su"
api_endpoint = "https://coomer.party/api/v1"


class Creator:
    id: str
    name: str
    service: str
    icon: str

    def __init__(self, id: str, name: str, service: str):
        self.id = id
        self.name = name
        self.service = service

    def __str__(self):
        s = f"{self.name}: {self.id}@{self.service}"
        return s

    @property
    def url(self):
        return f"{homepage}/{self.service}/user/{self.id}"

    @property
    def icon(self):
        return f"https://img.coomer.su/icons/{self.service}/{self.id}"

    def get_embed(self) -> discord.Embed:
        embed = discord.Embed(
            colour=discord.Colour.from_str(bot_config["colour"]),
            title=self.service,
            url=self.url
        )
        embed.set_thumbnail(url=self.icon)
        embed.add_field(name="ID", value=self.id)
        embed.add_field(name="Name", value=self.name)
        return embed

    @staticmethod
    def from_response(r: dict) -> "Creator":
        '''
        Returns
        -------
        Returns a new Creator object from id, name and
        service from r.
        '''
        return Creator(r["id"], r["name"], r["service"])


async def get_creators() -> list[Creator]:
    url = f"{api_endpoint}/creators.txt"
    client = aiohttp.ClientSession()
    r = await client.get(url)
    # unsuccessful
    if r.status != 200:
        logger.error(f"Unsuccessful request ({r.status_code}): {r.reason}")
        r.close()
        await client.close()
        return []
    # fetching creators
    creators: list[Creator] = []
    creators_json = await r.json()
    r.close()
    await client.close()
    # storing creators
    for creator in creators_json:
        creators.append(Creator.from_response(creator))
    # return
    return creators


async def get_random_creator() -> Creator:
    creators = await get_creators()
    return random.choice(creators)


async def get_matching_creators(id: str, name: str) -> list[Creator]:
    creators = await get_creators()
    matches = []
    if id:
        for creator in creators:
            if id == creator.id:
                matches.append(creator)
    elif name:
        for creator in creators:
            if name.lower() in creator.name.lower():
                matches.append(creator)
    return matches


class Post:
    id: str
    user: str
    service: str
    title: str
    filename: str
    filepath: str
    attachments: list[str]

    def __init__(
            self,
            id: str,
            user: str,
            service: str,
            title: str,
            filename: str,
            filepath: str,
            attachments: list[str]
    ):
        self.id = id
        self.user = user
        self.service = service
        self.title = title
        self.filename = filename
        self.filepath = filepath
        self.attachments = attachments

    def __str__(self):
        s = f"{self.title}: {self.user}@{self.service} (id={self.id})"
        return s

    @property
    def url(self):
        return f"{homepage}/{self.service}/user/{self.user}/post/{self.id}"

    @property
    def image(self):
        return f"{homepage}{self.filepath}"

    def get_embed(self) -> discord.Embed:
        embed = discord.Embed(
            colour=discord.Colour.from_str(bot_config["colour"]),
            title=self.service,
            url=self.url
        )
        embed.set_image(url=self.image)
        embed.add_field(name="ID", value=self.id)
        embed.add_field(name="Creator", value=self.user)
        embed.add_field(name="Title", value=self.title)
        return embed

    @staticmethod
    def from_response(r: dict) -> "Post":
        return Post(
            r["id"],
            r["user"],
            r["service"],
            r["title"],
            r["file"].get("name") or "",
            r["file"].get("path") or "",
            r["attachments"]
        )


class PaginationView(discord.ui.View):
    def __init__(self, items: list[Post|Creator]):
        super().__init__(timeout=1800)
        self.items = items
        self.index = 0

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    async def on_error(
            self,
            interaction: discord.Interaction,
            error: Exception,
            item: discord.ui.Item
    ):
        for child in self.children:
            child.disabled = True
        logger.error(error, stack_info=True)

    @discord.ui.button(label="Prev", emoji="⬅️")
    async def prev_callback(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ):
        if self.index == 0:
            self.index = len(self.items)
        self.index -= 1
        message = f"{self.index+1}/{len(self.items)}"
        for attachment in self.items[self.index].attachments["path"]:
            message += f"\n{homepage}{attachment}"
        await interaction.message.edit(
            content=message,
            embed=self.items[self.index].get_embed()
        )
        await default_response(interaction)

    @discord.ui.button(label="Next", emoji="➡️")
    async def next_callback(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ):
        self.index = (self.index+1) % len(self.items)
        message = f"{self.index+1}/{len(self.items)}"
        for attachment in self.items[self.index].attachments["path"]:
            message += f"\n{homepage}{attachment}"
        await interaction.message.edit(
            content=message,
            embed=self.items[self.index].get_embed()
        )
        await default_response(interaction)

    @discord.ui.button(label="Stop", emoji="⏹️")
    async def stop_callback(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ):
        for child in self.children:
            child.disabled = True
        self.stop()
        await default_response(interaction)


async def get_posts(
        query: str,
        page: int
) -> list[Post]:
    url = f"{api_endpoint}/posts?q={query}&o={page*50}"
    client = aiohttp.ClientSession()
    r = await client.get(url)
    # unsuccessful
    if r.status != 200:
        logger.error(f"Unsuccessful request ({r.status_code}): {r.reason}")
        return []
    # fetching posts
    posts_json = await r.json()
    r.close()
    await client.close()
    # storing posts
    posts = []
    for post in posts_json:
        posts.append(Post.from_response(post))
    # return
    return posts


async def get_creator_posts(
        query: str,
        creator_id: str,
        service: str,
        page: int
) -> list[Post]:
    url = f"{api_endpoint}/{service}/user/{creator_id}?q={query}&o={page*50}"
    client = aiohttp.ClientSession()
    r = await client.get(url)
    # unsuccessful
    if r.status != 200:
        logger.error(f"Unsuccessful request ({r.status_code}): {r.reason}")
        return []
    # fetching posts
    posts_json = await r.json()
    r.close()
    await client.close()
    # storing posts
    posts = []
    for post in posts_json:
        posts.append(Post.from_response(post))
    # return
    return posts
