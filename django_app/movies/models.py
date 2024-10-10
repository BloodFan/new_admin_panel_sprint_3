from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import FilmworkType, PersonRole
from .mixins import TimeStampedMixin, UUIDMixin
from .validators import min_max_validator


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")

    def __str__(self) -> str:
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(
        _("rating"),
        blank=True,
        null=True,
        validators=[*min_max_validator(0, 10)],
    )
    type = models.CharField(
        _("type"),
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
        max_length=7,
    )
    genres = models.ManyToManyField(
        Genre,
        through="GenreFilmwork",
        verbose_name=_("genres"),
        related_name="filmwork_set",
    )
    persons = models.ManyToManyField(
        Person,
        through="PersonFilmwork",
        verbose_name=_("PersonFilmwork"),
        related_name="filmwork_set",
    )

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("filmwork")
        verbose_name_plural = _("filmworks")
        ordering = ["-creation_date"]
        indexes = [
            models.Index(
                fields=["creation_date", "rating"],
                name="film_work_creation_rating_idx",
            )
        ]

    def __str__(self) -> str:
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="genrefilmworks",
        verbose_name=_("filmwork"),
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="genrefilmworks",
        verbose_name=_("genre"),
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre")
        verbose_name_plural = _("film genres")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="film_work_genre_idx",
            ),
        ]

    def __str__(self):
        return self.genre.name


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="personfilmworks",
        verbose_name=_("filmwork"),
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="personfilmworks",
        verbose_name=_("person"),
    )
    role = models.CharField(
        _("role"),
        choices=PersonRole.choices,
        default=PersonRole.ACTOR,
        max_length=10,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("person")
        verbose_name_plural = _("film persons")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="film_work_person_role_idx",
            ),
        ]

    def __str__(self):
        return self.person.full_name
