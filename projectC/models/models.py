from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False)  # Параметр echo выводит SQL-запросы в консоль

Base = declarative_base()

'''Для создания таблицы в БД. Выделите весь код в этом файле,
    нажать шифт + ентер в vs code.
В режиме командной строки python, ввести команду -> Base.metadata.create_all(engine)
'''


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(Integer, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    best_result = Column(Integer)
    total_number_games = Column(Integer, default=0)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
