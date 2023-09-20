import discord, requests, os, bs4, logging
from enum import Enum
from typing import Generator

async def is_reactor(user: discord.User, reaction: discord.Reaction) -> bool:
    async for i in reaction.users():
        if i == user:
            return True
    return False

class ScrappingStatus(Enum):
    username_not_found = 1,
    page_not_found = 2,
    website_not_found = 3,
    could_not_connect = 4,
    no_more_posts = 5

def get_random_username() -> str:
    homepage = "https://coomer.su"
    r = requests.get(f"{homepage}/artists/random", allow_redirects=True)
    username = os.path.basename(r.url)
    return username

def generate_code(username: str, start: int = 0) -> Generator[str, None, ScrappingStatus | None]:
    # defining some required values
    posts_per_page = 50
    homepage = "https://coomer.su"
    userpage = "onlyfans/user"
    # getting current page data
    start -= 1
    current_page = (start // posts_per_page) * posts_per_page
    start %= 50
    codes = [0]             # so than length is not zero
    while len(codes) > 0:
        # getting codes
        pageurl = f"{homepage}/{userpage}/{username}?o={current_page}"
        try:
            r = requests.get(pageurl, allow_redirects=False)
        except Exception as e:
            print(type(e))
            return ScrappingStatus.could_not_connect
        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            prehref = f"/{userpage}/{username}/post"
            codes = [element["href"].lstrip(prehref) for element in soup.find_all("a") if element["href"].startswith(prehref)]
        else:
            r = requests.get(homepage)
            if r.ok:
                return ScrappingStatus.username_not_found
            return ScrappingStatus.website_not_found
        # yielding codes
        for i in range(start, len(codes)):
            yield codes[i]
        start = 0
        current_page += posts_per_page

def get_post(username: str, code: str) -> (list[str], list[str]):
    '''
    returns list of image urls and list of video urls in the post
    '''
    homepage = "https://coomer.su"
    userpage = "onlyfans/user"
    pretext = f"/{userpage}/{username}/post"
    try:
        r = requests.get(f"{homepage}{pretext}/{code}")
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        videos = [element.find("source")["src"] for element in soup.find_all("video", {"class": "post__video"})]
        images = [element["href"] for element in soup.find_all("a", {"class": "fileThumb"})]
        return (videos, images)
    except Exception as e:
        logging.error(e)
        return ([], [])
