FROM python:3.7

RUN pip install poetry

COPY pyproject.toml /app/
COPY poetry.lock /app/

WORKDIR app

RUN poetry install

COPY app.py /app/

CMD poetry run gunicorn app:app -b 0.0.0.0:5000
EXPOSE 5000
