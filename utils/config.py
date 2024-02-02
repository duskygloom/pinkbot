import os
import json

from typing import Dict
from typing import List
from typing import Literal
from typing import TypedDict

config_file = "config.json"
version_config_t = Literal["DEBUG", "RELEASE"]

bot_options_t = Literal[
    "emoji",
    "token",
    "prefix",
    "colour",
    "greeting",
    "activity",
    "description",
    "client_secret"
]
bot_subconfig_t = Dict[bot_options_t, str]


class roles_subconfig_t(TypedDict):
    emoji: Dict[str, int]
    channel: int


class general_subconfig_t (TypedDict):
    greeting: str
    feedback: str
    ping_message: str
    sleep_reason: str
    admin_spam_limit: int
    common_spam_limit: int


class version_subconfig_t(TypedDict):
    cogs: List[str]
    config: version_config_t
    developer_id: int
    test_guild_id: int


class stickers_subconfig_t(TypedDict):
    path: str
    extensions: List[str]
    giffy_api_key: str
    tenor_api_key: str
    gif_search_results: int


class config_t(TypedDict):
    bot: bot_subconfig_t
    roles: roles_subconfig_t
    general: general_subconfig_t
    version: version_subconfig_t
    stickers: stickers_subconfig_t


def get_config() -> config_t:
    '''
    Info
    ----
    Parses config json file.

    Returns
    -------
    Returns parsed Dictionary.
    Returns empty Dictionary if config file is not found.
    '''
    if not os.path.isfile(config_file):
        return {}

    config_fp = open(config_file, "r", encoding="utf-8")
    config_data = json.load(config_fp)
    config_fp.close()
    return config_data


def save_config(config_data: config_t):
    '''
    Info
    ----
    Saves config_dict to config json file.
    '''
    config_fp = open(config_file, "w", encoding="utf-8")
    json.dump(config_data, config_fp, ensure_ascii=False, indent="\t")
    config_fp.close()
