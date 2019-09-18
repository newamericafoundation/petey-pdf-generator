FROM python:3.7

RUN pip install poetry

COPY pyproject.toml /app/
COPY poetry.lock /app/

WORKDIR app

RUN poetry config settings.virtualenvs.create false
RUN poetry install

COPY app.py /app/

CMD poetry run gunicorn app:app -b 0.0.0.0:$PORT
