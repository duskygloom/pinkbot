import random
import typing
import requests

from utils.config import get_config
from utils.logger import get_logger

stickers_config = get_config()["stickers"]

logger = get_logger("utils.giphy")

gif_search_endpoint = "https://api.giphy.com/v1/gifs/search"
stickers_search_endpoint = "https://api.giphy.com/v1/stickers/search"

rating_t = typing.Literal[
    "g",                        # General audience
    "pg",                       # Mild suggestive content
    "pg-13",                    # Highly suggestive content
    "r"                         # r for run away
]

bundle_t = typing.Literal[
    "clips_grid_picker",        # For clips content type
    "messaging_non_clips",      # For messaging
    "sticker_layering",         # For transparent gifs
    "low_bandwidth"             # For gifs less than 1MB
]


def get_api_request(
        query: str,
        username: str,
        limit: int = 10,
        offset: int = 0,
        rating: rating_t = "pg",
        lang: str = "en",
        bundle: bundle_t = "messaging_non_clips"
):
    '''
    Parameters
    ----------
    - query: Search query term or phrase. Add @<username>
    to search gifs of username.
    Maximum length: 50 characters.
    - username: Username of who is searching.
    - limit: The maximum number of objects to return.
    For beta keys max limit is 50.
    - offset: Specifies the starting position of the results.
    Maximum: 4999
    - rating: Filters results by specified rating.
    - lang: Specify default language for regional content.
    - bundle: Returns only renditions that correspond to the named bundle.
    '''
    api_request = gif_search_endpoint
    api_request += f"?api_key={stickers_config['giffy_api_key']}"
    api_request += f"&q={query}"
    api_request += f"&random_id={username}"
    api_request += f"&limit={limit}"
    api_request += f"&offset={offset}"
    api_request += f"&rating={rating}"
    api_request += f"&lang={lang}"
    api_request += f"&bundle={bundle}"
    return api_request


def get_gifs(
        query: str,
        username: str,
        limit: int = 10
) -> list[str]:
    '''
    Returns
    -------
    Returns list of gif urls.
    '''
    api_request = get_api_request(query, username, limit)
    r = requests.get(api_request)
    # unsuccessful API request
    if r.status_code != 200:
        logger.error(f"Something went wrong ({r.status_code}): {r.reason}")
        return []
    # storing original gif urls
    gifs = []
    results = r.json()["data"]
    for data in results:
        gifs.append(data["images"]["original"]["url"])
    return gifs


def get_random_gif(
        query: str,
        username: str,
        limit: int = 10
):
    gifs = get_gifs(query, username, limit)
    return random.choice(gifs)
