from django.urls import include, path

app_name = "v1"

urlpatterns = [
    path("movies/", include("api.v1.movies.urls")),
]
