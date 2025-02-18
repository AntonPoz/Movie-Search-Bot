from typing import List
from config_data.config import RATING_MOVIE_TYPES
from handlers.custom_handlers.show_movies_handler import PaginatorData


async def show_movies(watched_list: List) -> list:
    movie_list = []
    for watched_movie in watched_list:
        movie = await watched_movie.movie
        movie_type = RATING_MOVIE_TYPES[f'rating_{movie.movie_type}']
        movie_title = movie.movie_title
        movie_description = movie.movie_description
        movie_rating = movie.movie_rating
        movie_year = movie.movie_year
        movie_genres = movie.movie_genres
        movie_age_rating = movie.movie_age_rating
        movie_poster_url = movie.movie_poster_url
        show = f"___{movie_type} «{movie_title}»___ \n\n" \
               f"***Описание:*** {movie_description} \n" \
               f"***Рейтинг фильма:*** {movie_rating} \n" \
               f"***Год:*** {movie_year} \n" \
               f"***Жанр фильма:*** {movie_genres} \n" \
               f"***Возрастной рейтинг:*** {movie_age_rating} \n" \
               f"[Постер]({movie_poster_url})"
        paginator_data = PaginatorData(show, watched_movie)
        movie_list.append(paginator_data)
    return movie_list
