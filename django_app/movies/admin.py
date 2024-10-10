from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from api.v1.movies.services import MoviesService
from movies.utils import get_films_to_person

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "get_film_count",
        "get_film__actor_count",
        "get_films",
    )
    search_fields = ("full_name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Person]:
        service = MoviesService()
        return service.person_queryset_for_admin()

    def get_film__actor_count(self, obj):
        return obj.count_actor

    def get_film_count(self, obj):
        return obj.count_not_actor

    def get_films(self, obj):
        return get_films_to_person(obj)

    get_film__actor_count.short_description = _("Starred in")
    get_film_count.short_description = _("Participated in")


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ("genre",)


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ("person",)


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)
    list_display = ("title", "type", "creation_date", "rating", "get_genres", 'modified')
    list_filter = ("type", "genres")
    search_fields = ("title", "description", "id")

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related("genres")
        return queryset

    def get_genres(self, obj):
        return ",".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _("genres")
