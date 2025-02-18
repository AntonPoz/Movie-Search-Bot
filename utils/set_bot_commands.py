from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS
from telebot.asyncio_filters import StateFilter


async def set_default_commands(bot):
    await bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
    bot.add_custom_filter(StateFilter(bot))
