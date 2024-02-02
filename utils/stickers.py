import os

from utils.config import get_config

stickers_config = get_config()["stickers"]


def get_sticker_extension(path: str) -> tuple[str, str]:
    '''
    Returns
    -------
    Returns sticker name and extension as a tuple.
    '''
    basename = os.path.basename(path)
    index = basename.rfind(".")
    if index == -1:
        return basename, ""
    else:
        return basename[:index], basename[index:]


def get_sticker_path(name: str) -> str:
    '''
    Returns
    -------
    Finds a sticker of that name in sticker path.
    Returns path of the file if found.
    Else returns empty string.
    '''
    for path in os.listdir(stickers_config["path"]):
        if get_sticker_extension(path)[0] == name:
            return os.path.join(stickers_config["path"], path)
    return ""
