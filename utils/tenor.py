import random
import requests

from utils.config import get_config
from utils.logger import get_logger

stickers_config = get_config()["stickers"]

logger = get_logger("utils.tenor")


def get_api_request(query: str, client_key: str) -> str:
    '''
    Info
    ----
    Returns tenor API request url to search with
    query and client key provided in argument.

    Parameters
    ----------
    query       : topic of the gif
    client_key  : username of who requested the gif

    Returns
    -------
    API request for searching query in tenor.
    '''
    api_request = "https://tenor.googleapis.com/v2/search"
    api_request += f"?q='{query}'"
    api_request += f"&key={stickers_config['tenor_api_key']}"
    api_request += f"&client_key={client_key}"
    api_request += f"&limit={stickers_config['gif_search_results']}"
    return api_request


def get_gifs(query: str, username: str) -> list[str]:
    '''
    Returns
    -------
    Returns list of gif urls.
    '''
    # api request
    api_request = get_api_request(query, username)
    r = requests.get(api_request)
    # unsuccessful API request
    if r.status_code != 200:
        logger.error(f"Something went wrong ({r.status_code}): {r.reason}")
        return []
    # storing gifs
    gifs = []
    results = r.json()["results"]
    for data in results:
        gifs.append(data["media_formats"]["gif"]["url"])
    return gifs


def get_random_gif(query: str, username: str) -> str:
    '''
    Info
    ----
    Returns the url of a random gif obtained
    by query from tenor.

    Parameters
    ----------
    query       : topic of the gif
    username    : username of who requested the gif

    Returns
    -------
    If no gif is found, returns empty string.
    Else returns one of the gifs found.
    '''
    gifs = get_gifs(query, username)
    if not gifs:
        return ""
    return random.choice(gifs)
