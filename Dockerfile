FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app/game

ENV DJANGO_SETTINGS_MODULE=game.settings

RUN python manage.py migrate

CMD ["gunicorn", "game.game.wsgi:application", "--bind", "0.0.0.0:8000"]
