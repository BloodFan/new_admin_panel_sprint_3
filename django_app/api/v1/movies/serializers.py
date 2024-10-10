from rest_framework import serializers

from movies.choices import PersonRole
from movies.models import FilmWork, Person, PersonFilmWork
from movies.utils import get_name_depending_role


class PersonFilmWorksSerializer(serializers.ModelSerializer):
    film_title = serializers.CharField(source="film_work.title")

    class Meta:
        model = PersonFilmWork
        fields = ("role", "film_title")


class PersonSerializer(serializers.ModelSerializer):
    film_works = PersonFilmWorksSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ("id", "full_name", "film_works")


class FilmWorkSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()

    class Meta:
        model = FilmWork
        fields = (
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
            "genres",
            "actors",
            "directors",
            "writers",
        )

    def get_genres(self, obj: FilmWork) -> list[str]:
        return [genre.name for genre in obj.genres.all()]

    def get_actors(self, obj: FilmWork) -> list[str]:
        return get_name_depending_role(obj=obj, role=PersonRole.ACTOR)

    def get_directors(self, obj: FilmWork) -> list[str]:
        return get_name_depending_role(obj=obj, role=PersonRole.DIRECTOR)

    def get_writers(self, obj: FilmWork) -> list[str]:
        return get_name_depending_role(obj=obj, role=PersonRole.WRITER)
