from loader import bot
from telebot.types import Message
from peewee import IntegrityError
from database.custom_models import *
from tortoise.exceptions import IntegrityError


@bot.message_handler(commands=["start"])
async def handle_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        await connect()
        await create_models()
        await User.create(
            id=user_id,
            user_name=username,
            first_name=first_name,
            last_name=last_name,
        )
        await bot.reply_to(
            message, f"Привет {username}! "
                     f"\nЭто бот, который поможет тебе найти любимый фильм!"
        )
    except IntegrityError:
        await bot.reply_to(
            message, f"Рад вас снова видеть, {first_name}!"
        )
