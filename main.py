import logging, asyncio, bot, sys, os

try:
    from secret import bot_token
except ModuleNotFoundError:
    token_env = "PINKBOT_DISCORD_TOKEN"
    bot_token = os.getenv(token_env)
    if bot_token is None:
        logging.error(f"Token not found. Try setting the value of {token_env} environment variable.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        bot_instance = asyncio.run(bot.create_bot())
        bot_instance.run(bot_token)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
