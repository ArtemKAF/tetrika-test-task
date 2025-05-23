import inspect
from functools import wraps
from typing import Any, Callable, TypeVar, no_type_check

T = TypeVar("T")


def strict(func: Callable[..., T]) -> Callable[..., T]:
    """
    Декоратор, проверяющий типы аргументов и возвращаемого значения функции.

    Если тип не соответствует аннотации — вызывает TypeError.

    :param func: Оборачиваемая функция.
    :return: Обёрнутая функция с проверкой типов.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        """
        Внутренний обработчик, выполняющий проверку типов перед вызовом
        функции.

        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        :return: Результат оборачиваемой функции.
        """
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            param = sig.parameters[name]
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue
            annotation = param.annotation

            if annotation != inspect.Parameter.empty:
                if not isinstance(value, annotation):
                    raise TypeError(
                        f"Аргумент '{name}' должен быть типа '{annotation}', "
                        f"а получен {type(value)}."
                    )

        result = func(*args, **kwargs)
        return_annotation = sig.return_annotation
        if return_annotation != inspect.Parameter.empty:
            if not isinstance(result, return_annotation):
                raise TypeError(
                    f"Возвращаемое значение должно быть типа "
                    f"'{return_annotation}', а получено {type(result)}."
                )

        return result

    return wrapper


@strict
@no_type_check
def sum_two(a: int, b: int) -> int:
    """
    Складывает два целых числа.

    :param a: Первое число.
    :param b: Второе число.
    :return: Сумма чисел.
    """
    return a + b


def main():
    """
    Основная функция для демонстрации работы декоратора.
    """
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError


if __name__ == "__main__":
    main()
