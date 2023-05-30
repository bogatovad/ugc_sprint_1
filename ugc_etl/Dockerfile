FROM python:3.10.8-slim-bullseye

WORKDIR /ugc_etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY .. .

CMD python3 migrator.py