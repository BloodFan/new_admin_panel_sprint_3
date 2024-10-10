from django.db.models import Count, Prefetch, Q, QuerySet, Subquery, OuterRef

from movies.choices import PersonRole
from movies.models import FilmWork, Person, PersonFilmWork


class MoviesService:
    def filmwork_queryset(self) -> QuerySet[FilmWork]:
        return FilmWork.objects.all()

    def filmwork_extended_queryset(self) -> QuerySet[FilmWork]:
        return FilmWork.objects.prefetch_related(
            "genres",
            Prefetch(
                "personfilmworks",
                queryset=PersonFilmWork.objects.select_related("person"),
                to_attr="all_persons",
            ),
        ).all()

    def person_queryset(self) -> QuerySet[Person]:
        return Person.objects.all()

    def person_extended_queryset(self):
        return (
            self.person_queryset().prefetch_related(
                Prefetch(
                    "personfilmworks",
                    queryset=PersonFilmWork.objects.select_related(
                        "film_work"
                    ),
                    to_attr="film_works",
                )
            )
        ).all()

    def annotate_subquery_count(self, role: PersonRole) -> Subquery:
        """
        При наличии в annotate нескольких Count возможен баг 
        с перемножением результатов. Subquery правит ошибку.
        """
        return Subquery(
            Person.objects.filter(id=OuterRef('id'))
            .annotate(count=Count(
                'personfilmworks',
                filter=Q(personfilmworks__role=role)
                )
            )
            .values('count')[:1]
        )

    def person_queryset_for_admin(self) -> QuerySet[Person]:
        """
        Returns QuerySet with Counts films where person:
        1. count_actor - был актером
        2. count_not_actor - участвовал в ином плане.
        """
        return self.person_extended_queryset().annotate(
            count_actor=self.annotate_subquery_count(PersonRole.ACTOR),
            count_not_actor=Count(
                "personfilmworks",
                filter=~Q(personfilmworks__role=PersonRole.ACTOR),
            ),
        )
