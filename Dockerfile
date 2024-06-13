FROM python:3.12

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./ ./

# ENV PYTHONPATH=$PYTHONPATH:/src

CMD ["alembic", "upgrade", "head"]

CMD ["python", "src/main.py"]
