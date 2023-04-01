import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from app import Bot
from app.apis import apis

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(apis, prefix="/api")

bot = Bot()

app.state.bot = bot


def load_env():
    if not bot.APP_SETTINGS.TESTING:
        return
    bot.logger.debug("Loading .env file...")
    load_dotenv(dotenv_path=bot.BASE_DIR / '.env')

async def load_cogs():
    cogs_folder = bot.BASE_DIR / "app" / "cogs"
    for cog in cogs_folder.glob("*.py"):
        bot.logger.debug("Found cog: {}".format(cog.stem))
        if cog.name.startswith("_"):
            bot.logger.debug("Skipping cog: {}".format(cog.stem))
            continue
        bot.load_extension(f"app.cogs.{cog.stem}")
        bot.logger.info("Loaded cog: {}".format(cog.stem))


@app.on_event("startup")
async def startup():
    bot.logger.debug("Loading env...")
    load_env()
    bot.logger.debug("Loading cogs...")
    await load_cogs()


    try:
        bot.logger.debug("Starting bot...")
        discord_token = os.getenv("DISCORD_TOKEN")
        bot.logger.debug("Discord token gotten")

        bot.logger.info(f"Starting bot in {'Some'} mode.")

        if isinstance(discord_token, str) and len(discord_token) > 5:
            asyncio.create_task(bot.start(discord_token))
        else:
            bot.logger.critical("No Discord token found!")

    except:  # noqa
        pass

@app.on_event("shutdown")
async def shutdown():
    pass