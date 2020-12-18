FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser user

WORKDIR /home/user

COPY app app
COPY likes_bot likes_bot
COPY migrations migrations
COPY openapi openapi
COPY requirements.txt requirements.txt
COPY runserver.sh runserver.sh
COPY gunicorn_config.py gunicorn_config.py
RUN pip install --no-cache-dir -r requirements.txt --upgrade pip && pip install gunicorn

ENTRYPOINT ["./runserver.sh"]
