import time
from functools import wraps


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, FileNotFoundError) as error:
            print(f"Ошибка базы данных: {error}")
            print(
                "Проверьте корректность ввода\n"
                "Для просмотра доступных операций воспользуйтесь командой help"
                )

    return wrapper


def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if answer.strip().lower() != "y":
                print("Операция отменена")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.monotonic() - start
            print(
                f"Функция {func.__name__} "
                f"выполнилась за {elapsed:.3f} секунд"
            )

    return wrapper


def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key not in cache:
            cache[key] = value_func()

        return cache[key]

    return cache_result