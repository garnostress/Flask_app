from flask import jsonify
from typing import Union


class HttpError(Exception):
    """Этот класс нужен для формирования читаемых ошибок"""

    def __init__(self, status_code: int, message: Union[str, list, dict]):
        """
        Этот метод позволяет передавать полезную информацию об ошибке.
        :param status_code: int
            Код статуса.
        :param message: str | list| dict
            Строка, список или словарь со ошибкой, выдаваемый программой.
        """

        self.status_code = status_code
        self.message = message


def error_handler(error: HttpError):
    """
    Метод генерирует ответ для пользователя на основании ошибки.
    :param error: class
        Класс ошибки.
    :return:
        Response с читаемым кодом ошибки.
    """

    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response



