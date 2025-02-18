import json
from typing import List
from database.custom_models import *
from config_data.config import *
import httpx
from utils.json_search import find_value_in_json
from exception.custom_exception import BadRequest
from api.formed_response_list import formed_response


async def movie_search(search: BasicRequest) -> List:
    movie_title = search.movie_title
    movie_genre = search.movie_genre
    number_of_movie = search.number_of_movie
    params = {
        'page': 1,
        'limit': 250,
        'query': movie_title
    }
    headers = {
        'X-API-Key': KINOPOISK_API_KEY
    }

    movie_request_body = f'{BASE_URL}movie/search'
    async with httpx.AsyncClient() as client:
        response = await client.get(
            movie_request_body, headers=headers, params=params
        )

    if response.status_code != 200:
        raise BadRequest

    text_json = json.loads(response.text)
    response_list = []
    counter = 0

    for item in text_json['docs']:
        if counter == int(number_of_movie):
            break
        if find_value_in_json(item, movie_genre.lower()):
            counter += 1
            response_list.append(await formed_response(search, item))
    return response_list
