from models import Movie, Genre, Person, IndexData


indexs_dict = [
    {
        'model': Movie, 'index': 'movies',
        'query_handlers': ('person', 'genre', 'film_work')
    },
    {'model': Genre, 'index': 'genres', 'query_handlers': ('genre_index',)},
    {'model': Person, 'index': 'persons', 'query_handlers': ('person_index',)},
]

indexs_data: list[IndexData] = [IndexData(**data) for data in indexs_dict]
