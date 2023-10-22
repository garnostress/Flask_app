from flask import Flask


def make_app():
    """
    Функция создает и возвращает экземпляр класс Flask.
    :return:
        Экземпляр Flask.
    """

    application = Flask('app')
    return application
