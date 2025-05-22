import unittest

from task1.solution import strict

SUPPORTED_TYPES = (bool, int, float, str)

VALUE_MAP = {
    bool: True,
    int: 42,
    float: 3.14,
    str: "test",
}

WRONG_VALUES = {
    bool: 1.24,
    int: "not an int",
    float: "not a float",
    str: 123,
}


class TestDecorator(unittest.TestCase):
    """
    Тестирование декоратора @strict для проверки типов аргументов и
    возвращаемых значений функций.
    """

    def test_correct_argument_types(self):
        """
        Проверяет, что декоратор @strict допускает вызов функции,
        если типы аргументов соответствуют аннотированным.
        """

        for typ in SUPPORTED_TYPES:
            with self.subTest(type=typ):

                @strict
                def func(x):
                    return x

                func.__annotations__["return"] = typ

                result = func(VALUE_MAP[typ])
                self.assertEqual(result, VALUE_MAP[typ])

    def test_incorrect_argument_types(self):
        """
        Проверяет, что декоратор @strict выбрасывает TypeError,
        если тип переданного аргумента не соответствует аннотированному.
        """

        for typ in SUPPORTED_TYPES:
            with self.subTest(expected_type=typ):

                @strict
                def func(x):
                    return x

                func.__annotations__["x"] = typ

                with self.assertRaises(TypeError):
                    func(WRONG_VALUES[typ])

    def test_correct_types_positional_and_keyword(self):
        """
        Проверяет работу декоратора на функции с корректными позиционными
        и именованными аргументами разных типов.
        """

        for typ1, typ2 in zip(SUPPORTED_TYPES, SUPPORTED_TYPES):
            with self.subTest(types=(typ1, typ2)):

                @strict
                def func(a, b):
                    return a, b

                func.__annotations__["a"] = typ1
                func.__annotations__["b"] = typ2

                val1 = VALUE_MAP[typ1]
                val2 = VALUE_MAP[typ2]

                self.assertEqual(func(val1, val2), (val1, val2))

                if typ1 != typ2:
                    continue

                self.assertEqual(func(a=val1, b=val2), (val1, val2))

    def test_function_returns_correct_type(self):
        """
        Проверяет, что возвращаемое значение соответствует указанному типу.
        """

        for typ in SUPPORTED_TYPES:
            with self.subTest(return_type=typ):

                @strict
                def func():
                    return VALUE_MAP[typ]

                func.__annotations__["return"] = typ

                self.assertEqual(func(), VALUE_MAP[typ])

    def test_no_annotations(self):
        """
        Проверяет, что функция без аннотаций типов работает без ошибок.
        """

        values = [
            (2, 3),
            ("a", "b"),
            (True, False),
            (3.14, 2.71),
        ]

        for a, b in values:
            with self.subTest(args=(a, b)):

                @strict
                def func(x, y):
                    return x, y

                self.assertEqual(func(a, b), (a, b))

    def test_function_returns_wrong_type(self):
        """
        Проверяет, что возврат значения неверного типа вызывает TypeError.
        """

        for typ in SUPPORTED_TYPES:
            with self.subTest(expected_return_type=typ):

                @strict
                def func():
                    return WRONG_VALUES[typ]

                func.__annotations__["return"] = typ

                with self.assertRaises(TypeError):
                    func()


if __name__ == "__main__":
    unittest.main()
