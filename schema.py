import pydantic
from typing import Optional, Type  # возможность опционального выбора поля при обновлении данных.
from errors import HttpError
from typing import Type, Union



def validate(
        json_data: dict,
        model_class: Type[Union['CreateUser', 'UpdateUser', 'CreateAdvertisement', 'UpdateAdvertisement']]
            ):
    """
    Функция проверяет значения словаря json, полученного из запроса.

    :param json_data: dict
        Словарь json, получаемый из запроса.
    :param model_class:
        Модель класса, по которой проводим проверку.
    :return:
        Валидные словари или обработанную ошибку.
    """
    try:
        model_item = model_class(**json_data)  # создаем экземпляр принимаемого класса.
        return model_item.dict(exclude_none=True)  # возвращаем словарь с параметрами созданного класса
    except pydantic.ValidationError as error:
        raise HttpError(400, error.errors())  # т.к. на вход требуется словарь, то error.errors() - метод pydantic,
        # который создает словарь с описанием ошибок самостоятельно.


class CreateUser(pydantic.BaseModel):
    """Валидация данных при создании пользователя. Проверки на тип данных и длину значения"""

    name: str
    user_pass: str

    @pydantic.validator('name')
    def validate_name(cls, value):
        """
        Проверка на длину имени.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение
        """

        if len(value) > 50:
            raise ValueError('Name is too big')
        return value

    @pydantic.validator('user_pass')
    def validate_password(cls, value):
        """
        Проверка на длину пароля.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение.
        """

        if len(value) < 8:
            raise ValueError('password is too short')
        if len(value) > 100:
            raise ValueError('password is too big')
        return value


class UpdateUser(pydantic.BaseModel):
    """Валидация данных при обновлении пользователя. Проверки на тип данных и длину значения"""

    name: Optional[str]
    user_pass: Optional[str]

    @pydantic.validator('user_pass')
    def validate_password(cls, value):
        """
        Проверка на длину пароля.
        :param value: str
            Проверяемое значение name.
        :return:
            Проверенное значение.
        """

        if len(value) < 8:
            raise ValueError('password is too short')
        if len(value) > 100:
            raise ValueError('password is too big')
        return value


class CreateAdvertisement(pydantic.BaseModel):
    """Валидация данных при создании объявления."""

    header: str
    desc: Optional[str]
    owner_id: int


class UpdateAdvertisement(pydantic.BaseModel):
    """Валидация данных при обновлении объявления."""

    header: str
    desc: Optional[str]
