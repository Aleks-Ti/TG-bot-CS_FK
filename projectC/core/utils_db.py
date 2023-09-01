import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.utils import get_message_profile_user
from models.models import User

logging.basicConfig(
    format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'alchemy.log'),
    encoding='utf-8',
)

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(
    DATABASE_URL, echo=False
)  # Параметр echo выводит SQL-запросы в консоль

Session = sessionmaker(bind=engine)
session = Session()


def save_data_commit():
    '''Сохраняет данные в БД.'''
    try:
        session.commit()
    except Exception as err:
        session.rollback()
        logging.ERROR(f'Ошибка создания юзера: {err}')
        session.close()


def create_user(data):
    '''Создание профиля пользователя если нет в БД.'''
    user = data['from']

    user_exists = (
        session.query(User).filter_by(user_id=user['id']).first() is None
    )

    if user_exists:
        new_user = User(
            username=user['username'],
            user_id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
        )

        session.add(new_user)
        save_data_commit()
        return new_user


def game_data_update_users_profile(data_user: dict, value: int) -> None:
    '''Занесение результата игры в профиль пользователя.'''
    user_profile = (
        session.query(User).filter_by(user_id=data_user['from']['id']).first()
    )
    new_total = user_profile.total_number_games + 1

    session.query(User).filter_by(user_id=data_user['from']['id']).update(
        {
            'total_number_games': new_total,
            'best_result': value
            if user_profile.best_result is None
            or user_profile.best_result > value
            else user_profile.best_result,
        }
    )
    save_data_commit()


def get_profile_users(data_user: dict):
    '''Получение профиля пользователя.'''
    user = data_user['from']
    user_profile = session.query(User).filter_by(user_id=user['id']).first()
    if user_profile is None:
        user_profile = create_user(data_user)
    best_result = user_profile.best_result
    if best_result is None:
        return get_message_profile_user(user_profile)
    return get_message_profile_user(user_profile, best_result)
