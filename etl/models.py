from uuid import UUID

from pydantic import BaseModel, field_validator


class Person(BaseModel):
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
    directors: list[Person] | None
    actors: list[Person] | None
    writers: list[Person] | None

    @field_validator("directors_names", mode="before")
    def set_directors_names(cls, v):
        return v if v is not None else []


class ENVData(BaseModel):
    tables: list[str]
    periodicity: int
    schema_name: str
    index: str
    batch_size: int

    @field_validator("tables", mode="before")
    def set_tables(cls, v):
        return [table.strip() for table in v.split(",") if table.strip()]
