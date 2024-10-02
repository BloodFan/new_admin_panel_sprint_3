from typing import List, Optional
from pydantic import BaseModel

from uuid import UUID


class Person(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: UUID
    imdb_rating: Optional[float]
    genres: str
    title: str
    description: Optional[str]
    directors_names: Optional[str]
    actors_names: Optional[str]
    writers_names: Optional[str]
    directors: Optional[List[Person]]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]
