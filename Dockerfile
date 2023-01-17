FROM python:3.8

RUN apt-get update && apt-get install -y python3 python3-dev python3-pip build-essential
RUN pip install psycopg2 uwsgi pipenv
RUN pipenv install
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pipenv install --system --deploy
