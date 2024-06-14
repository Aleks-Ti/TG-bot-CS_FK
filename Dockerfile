FROM python:3.12

WORKDIR /app

COPY requirements.txt .

COPY Makefile .

COPY alembic.ini .

COPY ./migrations ./migrations

RUN pip install -r requirements.txt --no-cache-dir

COPY ./src ./src

ENV PYTHONPATH=$PYTHONPATH:/src

CMD ["alembic", "upgrade head"]

CMD ["python", "src/main.py"]
