from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class Person(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: UUID
    imdb_rating: Optional[float]
    genres: List[str]
    title: str
    description: Optional[str]
    directors_names: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    directors: Optional[List[Person]]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]

    @field_validator("directors_names", mode="before")
    def set_directors_names(cls, v):
        return v if v is not None else []


class ENVData(BaseModel):
    tables: List[str]
    periodicity: int
    schema_name: str
    index: str

    @field_validator("tables", mode="before")
    def set_tables(cls, v):
        return [table.strip() for table in v.split(",") if table.strip()]
