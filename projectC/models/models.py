from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///database.db"

# Параметр echo выводит SQL-запросы в консоль если True
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()

'''Для создания таблицы в БД. Раскомментить. Выделите весь код в этом файле,
    нажать шифт + ентер в vs code.
В режиме командной строки python, ввести команду:
                                Base.metadata.create_all(engine)
'''
'''
Для удаления например пользователя. Раскомментить. Выделите весь код в файле,
    нажать шифт + ентер в vs code.
В режиме командной строки python, ввести команду:
        me = session.query(User).filter_by(id=нужный id)
        me.delete()
        session.commit()
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
