from typing import List
from config_data.config import *
import httpx
import json
from exception.custom_exception import BadRequest
from api.formed_response_list import formed_response


async def movie_search_by_budget(budget_search: dict) -> List:
    movie_type = budget_search.movie_type
    movie_budget = budget_search.movie_budget
    movie_country = budget_search.movie_country
    number_of_movie = budget_search.number_of_movie
    params = {
        'page': 1,
        'limit': number_of_movie,
        'type': movie_type,
        'budget.value': movie_budget,
        'countries.name': movie_country
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
        response_list.append(await formed_response(budget_search, item))
    return response_list
