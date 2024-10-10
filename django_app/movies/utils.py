from typing import List, Union

from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from movies.choices import PersonRole
from movies.models import FilmWork, Person


def get_films_to_person(obj: Person) -> str:
    """
    Возвращает строку из ссылок на страницы Админки из
    всех фильмов где персона принимала участие.
    """
    links = [
        format_html(
            f'<a href="{settings.FRONTEND_URL}admin/movies/'
            f"filmwork/{relation.film_work.id}/"
            f'change/">{relation.film_work.title}</a>'
        )
        for relation in obj.film_works
    ]
    return mark_safe(", ".join(links))


def get_name_depending_role(
    obj: FilmWork, role: PersonRole
) -> Union[List[str], str]:
    """
    Возвращает либо:
    1. список из участников определенной роли
    2. строку о факте отсутствия участников с подобной ролью
    """
    result = []
    for person in obj.all_persons:
        if person.role == role:
            result.append(person.person.full_name)
    return result if result else f"Данные о {role} отсутствуют."
