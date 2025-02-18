from telebot.handler_backends import State, StatesGroup


class MovieSearchState(StatesGroup):
    movie_title = State()
    movie_genre = State()
    number_of_movie = State()
    show_movies = State()


class MovieSearchRatingState(StatesGroup):
    movie_type = State()
    movie_rating_platform = State()
    movie_rating = State()
    number_of_movie = State()


class MovieSearchBudgetState(StatesGroup):
    movie_type = State()
    movie_country = State()
    movie_budget = State()
    number_of_movie = State()


class MovieSearchHistory(StatesGroup):
    history_date = State()
