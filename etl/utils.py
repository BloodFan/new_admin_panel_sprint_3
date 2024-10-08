import uuid
from typing import Generator


def batch_list(
        lst: list, batch_size: int
) -> Generator[list[uuid.UUID], None, None]:
    """Возвращает генератор(срез в размере batch_size)."""
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]
