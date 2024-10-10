from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from movies.paginations import BasePageNumberPagination

from .serializers import FilmWorkSerializer, PersonSerializer
from .services import MoviesService


class FilmWorkViewsSet(
    GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):

    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        print(1)
        return MoviesService().filmwork_extended_queryset()

    def get_serializer_class(self):
        if self.action in ("retrive", "list"):
            return FilmWorkSerializer
        else:
            return FilmWorkSerializer


class PersonViewsSet(
    GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):

    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        return MoviesService().person_extended_queryset()

    def get_serializer_class(self):
        if self.action in ("retrive", "list"):
            return PersonSerializer
        else:
            return PersonSerializer
