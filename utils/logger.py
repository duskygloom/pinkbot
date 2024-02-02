import logging

from utils.config import get_config

version_config = get_config()["version"]


def get_logger(name: str) -> logging.Logger:
    '''
    Returns
    -------
    Returns a logger with the given name.
    '''
    logger = logging.getLogger(name)
    if version_config["config"] == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif version_config["config"] == "RELEASE":
        logger.setLevel(logging.WARNING)
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('{asctime} {levelname:<8} {name}: {message}', dt_fmt, style='{')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger
