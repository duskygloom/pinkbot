import secret, logging, asyncio
import bot

if __name__ == "__main__":
    try:
        bot_instance = asyncio.run(bot.create_bot())
        bot_instance.run(secret.bot_token)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
