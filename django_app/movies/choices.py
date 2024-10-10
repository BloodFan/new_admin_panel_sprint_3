from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class FilmworkType(TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv show", _("tv show")


class PersonRole(TextChoices):
    ACTOR = "actor", _("actor")
    PRODUCER = "producer", _("producer")
    DIRECTOR = "director", _("director")
    WRITER = "writer", _("writer")
    OTHER = "other", _("other")


class Gender(TextChoices):
    MALE = "male", _("male")
    FEMALE = "female", _("female")
