from telebot.types import Message
from database.custom_models import *
from states.custom_state import MovieSearchBudgetState
from telebot.types import InlineKeyboardMarkup
from config_data.config import BUDGET_MOVIE_TYPES, BUDGET_RANGE
from api.movie_search_by_budget import movie_search_by_budget
from utils.show_data import show_movies
from handlers.custom_handlers.show_movies_handler import *
from exception.custom_exception import BadRequest


def gen_markup(buttons):
    keyboard = InlineKeyboardMarkup()
    for key, value in buttons.items():
        button = InlineKeyboardButton(text=value, callback_data=key)
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=["movie_by_budget"])
async def handle_movie_by_rating(message: Message):
    user_id = message.from_user.id
    if await User.get_or_none(id=user_id) is None:
        await bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
    await bot.send_message(
        message.from_user.id, "⬇️Выберите тип фильма⬇️",
        reply_markup=gen_markup(BUDGET_MOVIE_TYPES)
    )
    await bot.set_state(
        message.from_user.id, MovieSearchBudgetState.movie_type
    )
    async with bot.retrieve_data(
            message.from_user.id, message.chat.id
    ) as data:
        data["movie_search_budget"] = {"user_id": user_id}


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("budget"))
async def handle_type_of_movie(callback_query):
    movie_type = callback_query.data.split("_")[1]
    async with bot.retrieve_data(
            callback_query.from_user.id,
            callback_query.message.chat.id
    ) as data:
        data["movie_search_budget"]["movie_type"] = movie_type
    await bot.delete_message(
        callback_query.from_user.id,
        callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Введите страну производства️"
    )
    await bot.set_state(
        callback_query.from_user.id,
        MovieSearchBudgetState.movie_country
    )


@bot.message_handler(state=MovieSearchBudgetState.movie_country)
async def handle_search_movie(message):
    country = message.text
    async with bot.retrieve_data(
            message.from_user.id,
            message.chat.id
    ) as data:
        data["movie_search_budget"]["movie_country"] = country
    await bot.send_message(
        message.from_user.id, "⬇️Выберите бюджет⬇️",
        reply_markup=gen_markup(BUDGET_RANGE)
    )
    await bot.set_state(
        message.from_user.id, MovieSearchBudgetState.movie_budget
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data.startswith("range")
)
async def handle_type_of_movie(callback_query):
    budget = callback_query.data
    if budget == "range_budget_low":
        budget = "0-10000000"
    elif budget == "range_budget_middle":
        budget = "10000000-50000000"
    else:
        budget = "50000000-1000000000"
    async with bot.retrieve_data(
            callback_query.from_user.id,
            callback_query.message.chat.id
    ) as data:
        data["movie_search_budget"]["movie_budget"] = budget
    await bot.delete_message(
        callback_query.from_user.id,
        callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        "Введите количество фильмов для вывода"
    )
    await bot.set_state(
        callback_query.from_user.id,
        MovieSearchBudgetState.number_of_movie
    )


@bot.message_handler(state=MovieSearchBudgetState.number_of_movie)
async def handle_search_movie(message):
    number_of_movie = message.text
    async with bot.retrieve_data(
            message.from_user.id, message.chat.id
    ) as data:
        data["movie_search_budget"]["number_of_movie"] = number_of_movie
    new_search = await BudgetRequest.create(**data["movie_search_budget"])
    await bot.send_message(message.from_user.id, f"Выполняется поиск фильма!")

    try:
        response_list = await movie_search_by_budget(new_search)
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
