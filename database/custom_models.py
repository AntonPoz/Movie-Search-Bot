from tortoise import Tortoise, fields
from tortoise.models import Model
from datetime import date
import uuid
from tortoise.exceptions import DBConnectionError


class User(Model):
    id = fields.IntField(pk=True, source_field="id")
    user_name = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255, null=True)


class BasicRequest(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_date = fields.DateField(default=date.today())
    user = fields.ForeignKeyField(
        "models.User",
        source_field="user",
        related_name="basic_requests"
    )
    movie_title = fields.CharField(max_length=255)
    movie_genre = fields.CharField(max_length=255)
    number_of_movie = fields.IntField()


class RatingRequest(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_date = fields.DateField(default=date.today())
    user = fields.ForeignKeyField(
        "models.User",
        source_field="user",
        related_name="rating_requests"
    )
    movie_type = fields.CharField(max_length=255)
    rating_platform = fields.CharField(max_length=255)
    rating_range = fields.CharField(max_length=255)
    number_of_movie = fields.IntField()


class BudgetRequest(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_date = fields.DateField(default=date.today())
    user = fields.ForeignKeyField(
        "models.User",
        source_field="user",
        related_name="budget_requests"
    )
    movie_type = fields.CharField(max_length=255)
    movie_budget = fields.CharField(max_length=255)
    movie_country = fields.CharField(max_length=255)
    number_of_movie = fields.IntField()


class Response(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    watched_movie = fields.ForeignKeyField(
        "models.WatchedMovie",
        source_field="watched_movie",
        related_name="response"
    )
    user_id = fields.IntField()
    created_date = fields.DateField(default=date.today())


class WatchedMovie(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    movie = fields.ForeignKeyField(
        "models.Movie",
        source_field="movie",
        related_name="watched_movie"
    )
    is_watched = fields.BooleanField(default=False)


class Movie(Model):
    id = fields.IntField(pk=True)
    created_date = fields.DateField(default=date.today())
    movie_type = fields.CharField(max_length=255)
    movie_title = fields.CharField(max_length=255)
    movie_description = fields.CharField(max_length=5000)
    movie_rating = fields.CharField(max_length=255)
    movie_year = fields.CharField(max_length=255)
    movie_genres = fields.TextField()
    movie_age_rating = fields.CharField(max_length=255)
    movie_poster_url = fields.CharField(max_length=255)


async def create_models():
    try:
        await Tortoise.generate_schemas()
    except BaseException as exc:
        raise BaseException(f'Ошибка создания модели БД: {exc}')


async def connect():
    try:
        await Tortoise.init(
            db_url="sqlite://database.db",
            modules={"models": ["database.custom_models"]},
        )
    except DBConnectionError as exc:
        raise DBConnectionError(f'Ошибка подключения к БД: {exc}')
