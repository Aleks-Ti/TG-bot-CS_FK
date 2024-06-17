FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY Makefile .

COPY alembic.ini .

COPY ./migrations ./migrations

COPY ./static ./static

RUN pip install -r requirements.txt --no-cache-dir

COPY ./src ./src

ENV PYTHONPATH=$PYTHONPATH:/src

CMD ["python", "src/main.py"]
