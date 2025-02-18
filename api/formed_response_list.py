from database.custom_models import *


async def formed_response(user_info: BasicRequest, response: dict) -> Response:
    user = await user_info.user
    get_existing_movie = await Movie.get_or_none(id=response['id'])
    if not get_existing_movie:
        movie_object = await Movie.create(
            id=int(response['id']),
            movie_type=extract_json_value(response, ['type']),
            movie_title=extract_movie_title(
                response, ['name', 'alternativeName']
            ),
            movie_description=extract_json_value(response, ['description']),
            movie_rating=extract_rating(response['rating']),
            movie_year=extract_json_value(response, ['year']),
            movie_genres=extract_json_value(response, ['genres']),
            movie_age_rating=extract_json_value(response, ['ageRating']),
            movie_poster_url=extract_json_value(response, ['poster', 'url'])
        )
        get_existing_movie = movie_object

    get_existing_watched_flag = await WatchedMovie.get_or_none(
        movie=get_existing_movie.id
    )
    if not get_existing_watched_flag:
        watched_object = await WatchedMovie.create(
            movie=get_existing_movie,
        )
        get_existing_watched_flag = watched_object

    response_object = await Response.create(
        watched_movie=get_existing_watched_flag,
        user_id=user.id,
        created_date=date.today()
    )
    return response_object


def extract_json_value(item, keys: list, default_value='-') -> str:
    try:
        for key in keys:
            item = item[key]
            if isinstance(item, list):
                result_string = str()
                for extract_item in item:
                    if result_string:
                        result_string += ', '
                    result_string += str(list(extract_item.values())[0])
                return result_string
        if item:
            return item
    except Exception:
        pass
    return default_value


def extract_rating(rating_platform: dict) -> str:
    ratings = str()
    for platform, rating in rating_platform.items():
        if platform != 'await':
            if rating != 0:
                if ratings:
                    ratings += ', '
                ratings += f'{platform}: {str(rating)}'
    return ratings


def extract_movie_title(response, keys, default_value='-'):
    for key in keys:
        movie_name = extract_json_value(response, [key])
        if movie_name != '-':
            return movie_name
    return default_value
