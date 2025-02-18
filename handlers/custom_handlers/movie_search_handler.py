from telebot.types import Message
from config_data.config import GENRE_LIST
from database.custom_models import *
from states.custom_state import MovieSearchState
from api.movie_search_request import movie_search
import httpx
from utils.show_data import show_movies
from handlers.custom_handlers.show_movies_handler import *


@bot.message_handler(commands=["movie_search"])
async def handle_movie_search(message: Message) -> None:
    user_id = message.from_user.id
    if await User.get_or_none(id=message.from_user.id) is None:
        await bot.reply_to(
            message, "Вы не зарегистрированы.\nНапишите /start"
        )
        return
    await bot.send_message(user_id, "Введите название фильма")
    await bot.set_state(
        message.from_user.id,
        MovieSearchState.movie_title, message.chat.id
    )
    async with bot.retrieve_data(message.from_user.id) as data:
        data["movie_search"] = {"user_id": user_id}


@bot.message_handler(state=MovieSearchState.movie_title)
async def handle_movie_genre(message: Message) -> None:
    async with bot.retrieve_data(message.from_user.id) as data:
        data["movie_search"]["movie_title"] = message.text
    await bot.send_message(message.from_user.id, "Введите жанр")
    await bot.set_state(
        message.from_user.id,
        MovieSearchState.movie_genre, message.chat.id
    )


@bot.message_handler(state=MovieSearchState.movie_genre)
async def handle_movie_count(message: Message) -> None:
    async with bot.retrieve_data(message.from_user.id) as data:
        if message.text.lower() in GENRE_LIST:
            data["movie_search"]["movie_genre"] = message.text
        else:
            await bot.set_state(
                message.from_user.id,
                MovieSearchState.movie_genre, message.chat.id
            )
            await bot.send_message(
                message.from_user.id,
                "Такой жанр отсутствует. Попробуйте еще раз!"
            )
            await bot.send_message(
                message.from_user.id, "Введите жанр"
            )
            return
    await bot.send_message(
        message.from_user.id,
        "Введите количество фильмов для вывода"
    )
    await bot.set_state(
        message.from_user.id,
        MovieSearchState.number_of_movie, message.chat.id
    )


@bot.message_handler(state=MovieSearchState.number_of_movie)
async def handle_movie_api_request(message: Message) -> None:
    async with bot.retrieve_data(message.from_user.id) as data:
        try:
            user_message = int(message.text)
        except ValueError:
            await bot.set_state(
                message.from_user.id,
                MovieSearchState.number_of_movie, message.chat.id
            )
            await bot.send_message(
                message.from_user.id,
                f"Необходимо ввести целое число!"
            )
            return
        if 250 >= user_message > 0:
            data["movie_search"]["number_of_movie"] = message.text
        else:
            await bot.set_state(
                message.from_user.id,
                MovieSearchState.number_of_movie, message.chat.id
            )
            await bot.send_message(
                message.from_user.id,
                "Ошибка! Значение должно быть в диапазоне от 0 до 250"
            )
            await bot.send_message(
                message.from_user.id,
                "Введите количество фильмов для вывода"
            )
            return

    new_search = await BasicRequest.create(**data["movie_search"])
    await bot.send_message(
        message.from_user.id,
        f"Выполняется поиск фильма!"
    )
    try:
        response_list = await movie_search(new_search)
    except httpx.HTTPError as exc:
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
        bot.send_message(
            message.from_user.id,
            f"По вашему запросу отсутствует фильм. "
            f"\nЗаново введите команду /movie_search"
        )
    await bot.delete_state(message.from_user.id)
