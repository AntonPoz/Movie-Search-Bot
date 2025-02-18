from typing import List
from config_data.config import *
import json
import httpx
from exception.custom_exception import BadRequest
from api.formed_response_list import formed_response


async def movie_search_by_rating(rating_search: dict) -> List:
    movie_type = rating_search.movie_type
    rating_platform = rating_search.rating_platform
    movie_rating = rating_search.rating_range
    number_of_movie = rating_search.number_of_movie
    params = {
        'page': 1,
        'limit': number_of_movie,
        'type': movie_type,
        f'rating.{rating_platform}': movie_rating
    }
    headers = {
        'X-API-Key': KINOPOISK_API_KEY
    }

    movie_request_body = f'{BASE_URL}movie'
    async with httpx.AsyncClient() as client:
        response = await client.get(
            movie_request_body, headers=headers, params=params
        )

    if response.status_code != 200:
        raise BadRequest

    text_json = json.loads(response.text)
    response_list = []

    for item in text_json['docs']:
        response_list.append(await formed_response(rating_search, item))
    return response_list
