FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y python3-dev libpq-dev build-essential


WORKDIR /app

COPY ./requirements.txt /app/requirements.txt 

COPY . /app/


RUN pip install --no-cache-dir  -r requirements.txt
