import asyncio
from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from tortoise import Tortoise
from database.custom_models import connect


async def main():
    await set_default_commands(bot)
    await connect()
    await bot.polling()
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
    Tortoise.close_connections()
