from typing import Tuple

from django.core.validators import MaxValueValidator, MinValueValidator


def min_max_validator(
    min_value: int, max_value: int
) -> Tuple[MinValueValidator, MaxValueValidator]:
    """Возвращает 2 валидатора ограничивающих мин. и мах. значения."""
    return MinValueValidator(min_value), MaxValueValidator(max_value)
