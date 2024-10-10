import pytest

from movies.models import Genre

pyteststmark = [pytest.mark.django_db]

@pytest.mark.django_db
def test_retrive_film_work(film_work):
    genre_count = Genre.objects.count()
    print(genre_count)
    assert genre_count == 1
    print(genre_count == 1)
