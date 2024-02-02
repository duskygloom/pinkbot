from pinkbot import Pinkbot

from utils.config import get_config
from utils.logger import get_logger

logger = get_logger("main")
bot_config = get_config()["bot"]

if __name__ == "__main__":
    pinkbot = Pinkbot("$", "Personal server assistant.")
    pinkbot.run(bot_config["token"])
