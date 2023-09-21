import logging, asyncio, bot, sys

try:
    from secret import bot_token
except ModuleNotFoundError:
    import os
    bot_token = os.getenv("DISCORD_TOKEN")
    if bot_token is None:
        logging.error("No token found.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        bot_instance = asyncio.run(bot.create_bot())
        bot_instance.run(bot_token)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
