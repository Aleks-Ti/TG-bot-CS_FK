# TG-bot-CS_FK

## О приложении

Бот, созданный для знакомства детей, школьников или студентов с компьютерными технологиями в игровом формате.
В игровом режиме, можно узнать как компьютер видит введенные данные от пользователя, и познакомится с интересными головоломками и алгоритмом "разделяй и властвуй" (бинарный поиск).

## Возможности

Доступно несколько функций:
Преобразование любых слов и букв, а также символов в машинный код, как его читают современные компьютеры.
А также обратное преобразование - из машинного кода в человекочитаемые символы или слова.
Игра <<Угадай число>> - где можно с помощью алгоритма "разделяй и властвуй" быстро отгадать загаданное случайное число.
Так же есть увлекательная игра "Пирамида Хаорта", где можно вручную попытаться сделать сотни, а то тычсячи перестановок для достижения победы, когда тот же компьютер может сделать это за считанные секунды.

## Технологии

Бот разработан с использованием фреймворка aiogram, который позволяет легко создавать и управлять ботами для Telegram.
Для миграция alembic. SqlAlchemy для взаимодействия с БД. База данных Postgres.

## Installation

Python 3.12

Клонируйте репозиторий ```TG-bot-CS_FK``` на свою локальную машину.

```bash
git clone https://github.com/Aleks-Ti/TG-bot-CS_FK.git
```

затем установить зависимости проекта в папке проекта:

```bash
poetry install
```

Чтобы бот заработал, необходимо создать файл в папке .env и указать в нем два ключа:

Токен бота Telegram (обязательно!)

```bash
TOKEN = "your TG token of the channel bot"
```

## Start

Чтобы запустить проект, нужно ввести:

```bash
python src/main.py  # должен быть предсозданна БД и на нее в .env указаны данные/Postgres локально установленный
# or
make start  # должен быть предсозданна БД и на нее в .env указаны данные/Postgres локально установленный.
# or
docker compose up --build -d # запуск через докер - первый запуск
# в дальнейшем можно так:
make startd  # запуск через докер
# or
docker compose up -d
```

### License

TG_bot-Exchange-rate is released under the MIT License.
