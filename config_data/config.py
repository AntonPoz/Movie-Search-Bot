import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")
KINOPOISK_VERSION = "v1.4"
BASE_URL = f"https://api.kinopoisk.dev/{KINOPOISK_VERSION}/"
DB_PATH = os.getenv("DATABASE")
DATE_FORMAT = "%Y-%m-%d"
DEFAULT_COMMANDS = (
    ("start", "Запуск бота"),
    ("movie_search", "Поиск фильма"),
    ("movie_by_rating", "Поиск по рейтингу"),
    ("movie_by_budget", "Поиск по бюджету"),
    ("history", "Вывод истории поиска"),
    ("help", "Вывести справку")
)

RATING_MOVIE_TYPES = {
    "rating_movie": "Фильм",
    "rating_tv-series": "Сериал",
    "rating_cartoon": "Мультфильм",
    "rating_animated-series": "Мультсериал",
    "rating_anime": "Аниме"
}

BUDGET_MOVIE_TYPES = {
    "budget_movie": "Фильм",
    "budget_tv-series": "Сериал",
    "budget_cartoon": "Мультфильм",
    "budget_animated-series": "Мультсериал",
    "budget_anime": "Аниме"
}

RATING_PLATFORM = {
    "platform_kp": "Кинопоиск",
    "platform_imdb": "IMDB",
    "platform_tmdb": "TMDB"
}

BUDGET_RANGE = {
    "range_budget_low": "Низко-бюджетные фильмы",
    "range_budget_middle": "Средне-бюджетные фильмы",
    "rangebudget_high": "Высоко-бюджетные фильмы"
}

GENRE_LIST = ['аниме', 'биография', 'боевик',
              'вестерн', 'военный', 'детектив',
              'детский', 'для взрослых', 'документальный',
              'драма', 'игра', 'история',
              'комедия', 'концерт', 'короткометражка',
              'криминал', 'мелодрама', 'музыка',
              'мультфильм', 'мюзикл', 'новости',
              'приключения', 'реальное ТВ', 'семейный',
              'спорт', 'ток-шоу', 'триллер',
              'ужасы', 'фантастика', 'фильм-нуар',
              'фэнтези', 'церемония'
              ]
