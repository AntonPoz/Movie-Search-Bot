from config_data.config import DEFAULT_COMMANDS
from handlers.custom_handlers.movie_search_handler import *
from telebot.types import Message


@bot.message_handler(commands=["help"])
async def handle_movie_by_rating(message: Message):
    show_command_info = f"⬇ Вот что умеет бот ⬇\n"
    for tuple in DEFAULT_COMMANDS:
        show_command_info += f"/{tuple[0]} - {tuple[1]}\n"
    await bot.send_message(
        message.from_user.id,
        show_command_info
    )
