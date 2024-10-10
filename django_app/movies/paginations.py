from typing import Union

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from movies.models import FilmWork, Person


class BasePageNumberPagination(PageNumberPagination):
    page_size: int = 5
    page_query_param: str = "page"
    max_page_size: int = 100
    page_size_query_param: str = "page_size"

    def get_paginated_response(
        self, data: Union[Person, FilmWork]
    ) -> Response:
        total_pages = self.page.paginator.num_pages
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": total_pages,
                "prev": self.get_previous_link(),
                "next": self.get_next_link(),
                "results": data,
            }
        )
