from telebot.types import Message
from database.custom_models import *
from states.custom_state import MovieSearchRatingState
from telebot.types import InlineKeyboardMarkup
from config_data.config import RATING_MOVIE_TYPES, RATING_PLATFORM
from api.movie_search_by_rating import movie_search_by_rating
from utils.show_data import show_movies
from handlers.custom_handlers.show_movies_handler import *
from exception.custom_exception import BadRequest


def gen_markup(buttons):
    keyboard = InlineKeyboardMarkup()
    for key, value in buttons.items():
        button = InlineKeyboardButton(text=value, callback_data=key)
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=["movie_by_rating"])
async def handle_movie_by_rating(message: Message):
    user_id = message.from_user.id
    if await User.get_or_none(id=user_id) is None:
        await bot.reply_to(
            message, "Вы не зарегистрированы. Напишите /start"
        )
        return
    await bot.send_message(
        message.from_user.id, "⬇️Выберите тип фильма⬇️",
        reply_markup=gen_markup(RATING_MOVIE_TYPES)
    )
    await bot.set_state(
        message.from_user.id,
        MovieSearchRatingState.movie_rating_platform
    )
    async with bot.retrieve_data(
            message.from_user.id, message.chat.id
    ) as data:
        data["movie_search_rating"] = {"user_id": user_id}


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("rating")
)
async def handle_type_of_movie(callback_query):
    movie_type = callback_query.data.split("_")[1]
    async with bot.retrieve_data(
            callback_query.from_user.id, callback_query.message.chat.id
    ) as data:
        data["movie_search_rating"]["movie_type"] = movie_type
    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id, "⬇️Выберите рейтинговую-платформу⬇️",
        reply_markup=gen_markup(RATING_PLATFORM))
    await bot.set_state(
        callback_query.from_user.id, MovieSearchRatingState.movie_rating
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("platform")
)
async def handle_rating_platform(callback_query):
    rating_platform = callback_query.data.split("_")[1]
    async with bot.retrieve_data(
            callback_query.from_user.id, callback_query.message.chat.id
    ) as data:
        data["movie_search_rating"]["rating_platform"] = rating_platform
    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Введите диапазон рейтинга для поиска"
    )
    await bot.set_state(
        callback_query.from_user.id,
        MovieSearchRatingState.movie_rating
    )


@bot.message_handler(state=MovieSearchRatingState.movie_rating)
async def handle_search_movie(message):
    rating = message.text
    async with bot.retrieve_data(
            message.from_user.id, message.chat.id
    ) as data:
        data["movie_search_rating"]["rating_range"] = rating
    await bot.send_message(
        message.from_user.id, "Введите количество фильмов для вывода"
    )
    await bot.set_state(
        message.from_user.id, MovieSearchRatingState.number_of_movie
    )


@bot.message_handler(state=MovieSearchRatingState.number_of_movie)
async def handle_search_movie(message):
    number_of_movie = message.text
    async with bot.retrieve_data(
            message.from_user.id, message.chat.id
    ) as data:
        data["movie_search_rating"]["number_of_movie"] = number_of_movie

    new_search = await RatingRequest.create(**data["movie_search_rating"])
    await bot.send_message(
        message.from_user.id,
        f"Выполняется поиск фильма!"
    )

    try:
        response_list = await movie_search_by_rating(new_search)
    except BadRequest as exc:
        await bot.send_message(message.from_user.id, exc)
        await bot.delete_state(message.from_user.id)
        return

    watched_movie_dict = {}
    for item in response_list:
        watched_movie = await item.watched_movie
        watched_movie_dict[watched_movie.id] = watched_movie
    watched_movie_list = watched_movie_dict.values()

    movie_list = await show_movies(watched_movie_list)
    if len(movie_list) > 0:
        paginator = Paginator(message, movie_list)
        await paginator.show()
    else:
        await bot.send_message(
            message.from_user.id,
            f"По вашему запросу отсутствует фильм. "
            f"\nЗаново введите команду /movie_by_rating"
        )
    await bot.delete_state(message.from_user.id)
