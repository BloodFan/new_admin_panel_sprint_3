import time
from functools import wraps
from typing import Any, Callable, Iterable, TypeVar

RT = TypeVar("RT")


def backoff(
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
    max_restart: int = 100,
    errors: Iterable = (Exception,),
    client_errors: Iterable = (Exception,),
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до
    граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * (factor ^ n), если t < border_sleep_time
        t = border_sleep_time, иначе
    :param start_sleep_time: начальное время ожидания
    :param factor: во сколько раз нужно увеличивать
        время ожидания на каждой итерации
    :param border_sleep_time: максимальное время ожидания
    :max_restart - мах кол-во попыток восстановления соеденения
    :errors - ошибки при которых разумна попытка переподключения
    :client_errors - ошибка на стороне клиента, переподключения неактуально
    :return: результат выполнения функции
    """

    def decorator(func: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> RT:
            n = 0
            restart_count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except errors as e:
                    print(f"error {e}")
                    t = border_sleep_time
                    _time = start_sleep_time * (factor ^ n)
                    if _time < border_sleep_time:
                        t = _time
                    time.sleep(t)
                    n += 1
                    restart_count += 1
                    if restart_count > max_restart:
                        raise RuntimeError(f"Превышено  мах число попыток - {e}")
                except client_errors as e:
                    raise RuntimeError(f"Проблема на стороне клиента - {e}")

        return wrapper

    return decorator
