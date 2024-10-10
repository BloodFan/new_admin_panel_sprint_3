import pytest
from datetime import date

from movies.models import Genre, Person, FilmWork, PersonFilmWork
from movies.choices import FilmworkType, PersonRole

pyteststmark = [pytest.mark.django_db]


@pytest.fixture
def genre():
    """Жанр для Тестирования"""
    return Genre.objects.create(
        name="Action",
        description="Action films")


@pytest.fixture
def three_persons():
    """Создает 3 персонажа для тестирования."""
    person_list = [
        Person(full_name="Danila Kozlovsky"),
        Person(full_name="Daria Zoteeva"),
        Person(full_name="Alexey Serebriakov"),
    ]
    return Person.objects.bulk_create(person_list)


@pytest.fixture
def film_work(genre, three_persons):
    """Фильм для тестирования"""
    film_work = FilmWork.objects.create(
        title="BEST MOVIE EVER",
        description="The title lies!",
        creation_date=date(2023, 10, 10),
        rating=1.1,
        type=FilmworkType.MOVIE
    )
    film_work.genres.add(genre)

    personfilmwork_list = [
        PersonFilmWork(
            film_work=film_work,
            person=person,
            role=PersonRole.ACTOR
        ) for person in three_persons
    ]

    PersonFilmWork.objects.bulk_create(personfilmwork_list)

    return film_work
