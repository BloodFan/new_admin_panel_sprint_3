from rest_framework.routers import DefaultRouter

from .views import FilmWorkViewsSet, PersonViewsSet

router = DefaultRouter()

router.register("persons", PersonViewsSet, basename="persons")
router.register("filmworks", FilmWorkViewsSet, basename="filmworks")

app_name = "movies"

urlpatterns = []

urlpatterns += router.urls
