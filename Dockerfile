FROM python:3.10-slim-buster

WORKDIR /src

COPY . /src

RUN python -m pip install -U && python -m pip install aiogram==2.19 'aiohttp[speedups]' uvloop ujson

