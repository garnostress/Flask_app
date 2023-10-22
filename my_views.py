from flask.views import MethodView
from models import Session, User, Advertisement
from errors import HttpError
from flask import jsonify, request
from schema import validate, CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement
from hashlib import md5
from sqlalchemy.exc import IntegrityError


def get_user(user_id: int, session: Session) -> User:
    """
    Позволяет получить пользователя по id или возвращает ошибку.

    :param user_id: int
        Id пользователя.
    :param session:
        Объект сессии.
    :return:
        Объект пользователя.
    """
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'user not found.')
    return user


def make_hash_password(password):
    """
    Функция для хэширования пароля или иных строчных данных.

    :param password: str
        пароль, полученный из json-файла.
    :return: str
        хешированный пароль.
    """
    encode_password = password.encode()  # переводим в байты
    hashed_password = md5(encode_password).hexdigest()  # хэшируем
    return hashed_password


def get_adv(advertisement_id: int, session: Session) -> Advertisement:
    """
    Позволяет получить объявление по id или возвращает ошибку.

    :param advertisement_id: int
        Id объявления.
    :param session:
        Объект сессии.
    :return:
        Объект объявления.
    """
    adv = session.get(Advertisement, advertisement_id)
    if adv is None:
        raise HttpError(404, 'Advertisement not found.')
    return adv


class UserView(MethodView):  # создаем класс с методами CRUD
    """Viewset для модели пользователя"""

    def get(self, user_id: int):
        """
        Метод для получения конкретного пользователя.

        :param user_id: int
            Id пользователя.
        :return:
            Объект пользователя.
        """
        with Session() as session:
            user = get_user(user_id=user_id, session=session)
            response = jsonify({
                'id': user.id,
                'name': user.name
            })
            return response

    def post(self):
        """
        Метод для создания пользователя. Есть проверка валидности данных и хешироавание пароля.
        В случае ошибки вызывается исключение.

        :return: dict
            Id и имя созданного пользователя.
        """

        json_data = validate(json_data=request.json, model_class=CreateUser)  # валидируем данные.

        #  делаем хэширование пароля при помощи md5
        password = json_data.get('user_pass')  # достаем пароль из json
        hashed_password = make_hash_password(password)  # хэшируем функцией
        json_data['user_pass'] = hashed_password  # сохраняем хэш на месте пришедшего пароля

        with Session() as session:
            new_user = User(**json_data)  # создаем объект User, распаковывая параметры.
            session.add(new_user)  # добавляем
            try:
                session.commit()  # пробуем сохранить.
            except IntegrityError as error:
                raise HttpError(409, 'user already exists.')  # вызываем обработанную ошибку, если не выходит.
            return jsonify({'id': new_user.id, 'name': new_user.name})

    def patch(self, user_id: int):
        """
        Метод для обновления пользователя. Есть проверка валидности данных и хеширование пароля.
        В случае ошибки вызывается исключение.

        :param user_id: int
            Id пользователя.
        :return: dict
            Id обновленного пользователя.
        """

        json_data = validate(json_data=request.json, model_class=UpdateUser)
        with Session() as session:
            user = get_user(user_id=user_id, session=session)
            for field, value in json_data.items():
                if field == 'user_pass':
                    setattr(user, field, make_hash_password(value))
                else:
                    setattr(user, field, value)
            try:
                session.commit()
            except IntegrityError as error:
                raise HttpError(409, 'data is not unique')

            return jsonify({'id': user.id})

    def delete(self, user_id: int):
        """
        Метод для удаления конкретного пользователя.

        :param user_id: int
            Id пользователя.
        :return: dict
            Значение - имя удаленного пользователя.
        """

        with Session() as session:
            user = get_user(user_id=user_id, session=session)
            session.delete(user)
            session.commit()
            return jsonify({'deleted': user.name})


class AdvertisementView(MethodView):
    """Viewset для объявлений"""

    def get(self, advertisement_id: int):
        """
        Метод для получения конкретного объявления.

        :param advertisement_id: int
            Id объявления.
        :return:
            Объект объявления.
        """
        with Session() as session:
            adv = get_adv(advertisement_id=advertisement_id, session=session)
            response = jsonify({
                'id': adv.id,
                'name': adv.header
            })
            return response

    def post(self):
        """
        Метод для создания объявления. Есть проверка валидности данных.
        В случае ошибки вызывается исключение.

        :return: dict
            Id и заголовок созданного объявления.
        """

        json_data = validate(json_data=request.json, model_class=CreateAdvertisement)  # валидируем данные.

        with Session() as session:
            new_adv = Advertisement(**json_data)  # создаем объект Advertisement, распаковывая параметры.
            session.add(new_adv)  # добавляем
            try:
                session.commit()  # пробуем сохранить.
            except IntegrityError as error:
                raise HttpError(409, 'ADV already exists.')  # вызываем обработанную ошибку, если не выходит.
            return jsonify({'id': new_adv.id, 'header': new_adv.header})

    def patch(self, advertisement_id: int):
        """
        Метод для обновления объявления. Есть проверка валидности данных. В случае ошибки вызывается исключение.

        :param advertisement_id: int
            Id объявления.
        :return: dict
            Id обновленного объявления и его заголовок.
        """

        json_data = validate(json_data=request.json, model_class=UpdateAdvertisement)
        with Session() as session:
            adv = get_adv(advertisement_id=advertisement_id, session=session)
            for field, value in json_data.items():
                setattr(adv, field, value)
            # try:
                session.commit()
            # except IntegrityError as error:
            #     raise HttpError(409, 'data is not unique')

            return jsonify({'id': adv.id, 'header': adv.header})

    def delete(self, advertisement_id: int):
        """
        Метод для удаления конкретного объявления.

        :param advertisement_id: int
            Id объявления.
        :return: dict
            Значение - заголовок удаленного объявления.
        """

        with Session() as session:
            adv = get_adv(advertisement_id=advertisement_id, session=session)
            session.delete(adv)
            session.commit()
            return jsonify({'deleted': adv.header})
