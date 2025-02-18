# Телеграм-бот для поиска фильмов и сериалов

Этот проект представляет собой Телеграм-бота, который взаимодействуя с API кинопоиска ищет фильмы и сериалы подходящие пользвателю. 
Бот позволяет пользователям искать фильмы по названию, рейтингу, бюджету и просматривать историю запросов.

## Функциональные возможности

Бот поддерживает следующие команды:
#### custom command:
1) **movie_search**: поиск фильма/сериала по названию.

Запрос без параметров:
CURL GET 'https://api.kinopoisk.dev/v1.4/movie/search'

Пример ответа на запрос:
```console
{
  "docs": [
    {
      "id": 180609,
      "name": "Адреналин",
      "alternativeName": "Crank",
      "enName": "",
      "type": "movie",
      "year": 2006,
      "description": "Наемный убийца Чев узнает, что недоброжелатели отравили его редким китайским ядом и отрава начнет действовать немедленно, как только пульс перестанет биться ниже определенной отметки. \n\nИ теперь Чеву нужно успеть сделать все свои дела, попробовать раздобыть противоядие и отомстить своим отравителям в прямом смысле слова впопыхах - стараясь создавать вокруг себя как можно более напряженную обстановку и не расслабляться ни на секунду.",
      "shortDescription": "",
      "movieLength": 88,
      "isSeries": false,
      "ticketsOnSale": false,
      "totalSeriesLength": null,
      "seriesLength": null,
      "ratingMpaa": "r",
      "ageRating": 18,
      "top10": null,
      "top250": null,
      "typeNumber": 1,
      "status": null,
      "names": [
        {
          "name": "Адреналин"
        },
        {
          "name": "Crank"
        },
        {
          "name": "בלתי יציב",
          "language": "IL",
          "type": null
        },
        {
          "name": "Zastaneš a neprežiješ",
          "language": "SK",
          "type": null
        },
        {
          "name": "Crank - Felpörgetve",
          "language": "HU",
          "type": null
        },
        {
          "name": "Crank - Langsam sterben war gestern",
          "language": "DE",
          "type": null
        },
        {
          "name": "Crank: Veneno en la sangre",
          "language": "ES",
          "type": "Castilian Spanish"
        }
      ],
      "externalId": {
        "imdb": "tt0479884",
        "tmdb": 1948,
        "kpHD": "473655392e5d9815a67430072a1685f3"
      },
      "logo": {
        "url": "https://imagetmdb.com/t/p/original/8DD3IgWBXQUQH0Qfdbi8mA4UAQp.png"
      },
      "poster": {
        "url": "https://image.openmoviedb.com/kinopoisk-images/4303601/adb765e9-65e2-44a0-b584-33f48c198388/orig",
        "previewUrl": "https://image.openmoviedb.com/kinopoisk-images/4303601/adb765e9-65e2-44a0-b584-33f48c198388/x1000"
      },
      "backdrop": {
        "url": "https://image.openmoviedb.com/kinopoisk-ott-images/374297/2a00000180cc2d2ed42a7d3347f440e3cf60/orig",
        "previewUrl": "https://image.openmoviedb.com/kinopoisk-ott-images/374297/2a00000180cc2d2ed42a7d3347f440e3cf60/x1000"
      },
      "rating": {
        "kp": 7.256,
        "imdb": 6.9,
        "filmCritics": 6.1,
        "russianFilmCritics": 0,
        "await": null
      },
      "votes": {
        "kp": 151639,
        "imdb": 265333,
        "filmCritics": 102,
        "russianFilmCritics": 1,
        "await": 0
      },
      "genres": [
        {
          "name": "боевик"
        },
        {
          "name": "триллер"
        },
        {
          "name": "криминал"
        }
      ],
      "countries": [
        {
          "name": "США"
        }
      ],
      "releaseYears": []
    }
  ],
  "total": 18,
  "limit": 1,
  "page": 1,
  "pages": 18
}
```

2) **movie_by_rating**: поиск фильмов/сериалов по рейтингу.

Запрос без параметров:
CURL GET 'https://api.kinopoisk.dev/v1.4/movie'

Пример ответа на запрос:
```console
{
  "docs": [
    {
      "id": 6862424,
      "name": "У края бездны",
      "alternativeName": null,
      "type": "tv-series",
      "typeNumber": 2,
      "year": 2024,
      "description": null,
      "shortDescription": null,
      "status": "completed",
      "rating": {
        "kp": 9.789,
        "imdb": 0,
        "filmCritics": 0,
        "russianFilmCritics": 0,
        "await": null
      },
      "votes": {
        "kp": 564,
        "imdb": 0,
        "filmCritics": 0,
        "russianFilmCritics": 0,
        "await": 0
      },
      "movieLength": null,
      "totalSeriesLength": null,
      "seriesLength": null,
      "ratingMpaa": null,
      "ageRating": null,
      "genres": [
        {
          "name": "документальный"
        }
      ],
      "countries": [
        {
          "name": "Россия"
        }
      ],
      "releaseYears": [
        {
          "start": 2024,
          "end": 2024
        }
      ],
      "top10": null,
      "top250": null,
      "isSeries": true,
      "ticketsOnSale": false
    }
  ],
  "total": 19,
  "limit": 1,
  "page": 1,
  "pages": 19
}
```

3) **movie_search_by_budget**: поиск фильмов/сериалов разным бюджетом.

Запрос с параметрами:
CURL GET 'https://api.kinopoisk.dev/v1.4/movie?page=1&limit=1&type=anime&budget.value=50000000-1000000000&audience.count=&countries.name=%D0%AF%D0%BF%D0%BE%D0%BD%D0%B8%D1%8F'

Пример ответа на запрос:
```console
{
  "docs": [
    {
      "id": 346737,
      "name": null,
      "alternativeName": "Beyblade: The Movie - Fierce Battle",
      "enName": "Beyblade the Movie: Decisive Battle! Takao VS Daichi",
      "names": [
        {
          "name": "Bakuten Shoot Beyblade The Movie: Gekitou!! Takao vs Daichi",
          "language": "JP",
          "type": "romaji"
        },
        {
          "name": "Beyblade the Movie: Decisive Battle! Takao VS Daichi",
          "language": "US",
          "type": null
        },
        {
          "name": "Beyblade: The Movie - Fierce Battle",
          "language": "FR",
          "type": null
        },
        {
          "name": "Bakuten Shoot Beyblade the Movie: Gekitou!! Takao vs. Daichi",
          "language": "IT",
          "type": null
        },
        {
          "name": "탑 블레이드 더 무비",
          "language": "KR",
          "type": null
        }
      ],
      "type": "anime",
      "typeNumber": 4,
      "year": 2002,
      "description": "",
      "shortDescription": null,
      "status": null,
      "rating": {
        "kp": 0,
        "imdb": 5.6,
        "filmCritics": 0,
        "russianFilmCritics": 0,
        "await": 0
      },
      "votes": {
        "kp": 41,
        "imdb": 478,
        "filmCritics": 0,
        "russianFilmCritics": 0,
        "await": 0
      },
      "movieLength": 74,
      "totalSeriesLength": null,
      "seriesLength": null,
      "ratingMpaa": null,
      "ageRating": null,
      "poster": {
        "url": "https://image.openmoviedb.com/kinopoisk-images/1704946/2315b9a5-91a3-4ebc-a208-f713ba781b94/orig",
        "previewUrl": "https://image.openmoviedb.com/kinopoisk-images/1704946/2315b9a5-91a3-4ebc-a208-f713ba781b94/x1000"
      },
      "backdrop": {
        "url": "https://image.openmoviedb.com/tmdb-images/original/vCzOuT343wXpbDemaDOFlUNkkUb.jpg",
        "previewUrl": "https://image.openmoviedb.com/tmdb-images/w500/vCzOuT343wXpbDemaDOFlUNkkUb.jpg"
      },
      "genres": [
        {
          "name": "аниме"
        },
        {
          "name": "мультфильм"
        },
        {
          "name": "боевик"
        },
        {
          "name": "приключения"
        }
      ],
      "countries": [
        {
          "name": "Япония"
        }
      ],
      "ticketsOnSale": false,
      "top10": null,
      "top250": null,
      "isSeries": false,
      "releaseYears": [],
      "logo": {
        "url": null,
        "previewUrl": null
      }
    }
  ],
  "total": 18,
  "limit": 1,
  "page": 1,
  "pages": 18
}
```

#### default command:
4) **history**: возможность просмотра истории запросов и поиска фильма/сериала.
5) **help**: выводит информацию о доступных функциях бота.
6) **start**: запуск бота и сохраняет информацию о пользователе в БД.

## Сценарий поиска

При выполнении поиска бот задает следующие вопросы:

- Название фильма/сериала
- Страну производства
- Рейтинг фильмов
- Жанр (комедия, ужасы, фантастика и т.д.)
- Количество выводимых вариантов

## Вывод информации о фильме/сериале

При выводе информации о каждом фильме/сериале бот отображает следующие данные:

- Название
- Описание
- Рейтинг
- Год производства
- Жанр
- Возрастной рейтинг
- Постер

## История запросов

При просмотре истории запросов бот отображает следующие данные:

- Дата поиска
- Название фильма/сериала
- Описание фильма/сериала
- Рейтинг
- Год производства
- Жанр
- Возрастной рейтинг
- Постер

## Дополнительные функции
- Вывод информации о каждом фильме/сериале. Реализовано с использованием пагинации.
- В истории поиска доступные кнопки для отметки просмотренных и непросмотренных фильмов и сериалов.

### Как запустить
Для запуска бота необходимо установить необходимые библиотеки указанные в файле requirements.txt.
Запустить с помощью интерпритатора python файл main.py.