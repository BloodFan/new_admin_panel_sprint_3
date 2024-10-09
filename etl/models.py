from uuid import UUID
from typing import Union, Type

from pydantic import BaseModel, field_validator


class PersonToFilmWork(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: UUID
    imdb_rating: float | None
    genres: list[str]
    title: str
    description: str | None
    directors_names: list[str] | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    directors: list[PersonToFilmWork] | None
    actors: list[PersonToFilmWork] | None
    writers: list[PersonToFilmWork] | None

    @field_validator("directors_names", mode="before")
    def set_directors_names(cls, v):
        return v if v is not None else []


class Genre(BaseModel):
    id: UUID
    name: str


class RoleToFilmWork(BaseModel):
    role: str
    film_work_title: str
    film_work_id: UUID


class Person(BaseModel):
    id: UUID
    full_name: str
    participated: list[RoleToFilmWork] | None


class IndexData(BaseModel):
    query_handlers: tuple
    model: Type[Union[Movie, Genre, Person]]
    index: str
