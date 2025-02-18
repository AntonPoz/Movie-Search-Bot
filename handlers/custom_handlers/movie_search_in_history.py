from telebot.types import Message
from database.custom_models import *
from states.custom_state import MovieSearchHistory
from telebot.types import InlineKeyboardMarkup
from utils.show_data import show_movies
from handlers.custom_handlers.show_movies_handler import *
from tests.check_value import check_date


def gen_markup(buttons):
    keyboard = InlineKeyboardMarkup()
    for key, value in buttons.items():
        button = InlineKeyboardButton(text=value, callback_data=key)
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=["history"])
async def handle_movie_by_rating(message: Message):
    user_id = message.from_user.id
    if await User.get_or_none(id=user_id) is None:
        await bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
    await bot.send_message(message.from_user.id, "Введите дату поиска в формате: yyyy-mm-dd")
    await bot.set_state(message.from_user.id, MovieSearchHistory.history_date)


@bot.message_handler(state=MovieSearchHistory.history_date)
async def handle_search_movie(message):
    try:
        format_date, result = check_date(message.text)
    except ValueError:
        await bot.set_state(
            message.from_user.id,
            MovieSearchHistory.history_date, message.chat.id
        )
        await bot.send_message(
            message.from_user.id,
            "Ошибка! Дата должна быть в формате: yyyy-mm-dd"
        )
        await bot.send_message(
            message.from_user.id,
            "Введите дату поиска в формате: yyyy-mm-dd"
        )
        return
    response_list = await Response.filter(
        created_date=format_date,
        user_id=message.from_user.id
    )
    watched_movie_dict = {}
    for item in response_list:
        watched_movie = await item.watched_movie
        watched_movie_dict[watched_movie.id] = watched_movie
    watched_movie_list = watched_movie_dict.values()
    list_for_display = await show_movies(watched_movie_list)
    if len(watched_movie_list) > 0:
        paginator = Paginator(message, list_for_display)
        await paginator.show()
    else:
        await bot.send_message(
            message.from_user.id,
            f"В истории за дату {format_date} пока пусто!"
            f"\nСначала необходимо сделать запрос на поиск."
        )
    await bot.delete_state(message.from_user.id)
