FROM python:3.10.8-slim-bullseye

RUN pip install --upgrade pip

WORKDIR /ugc
RUN mkdir /ugc/tests
RUN groupadd -r ugc && useradd -d /ugc -r -g ugc ugc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .. .
RUN chown ugc:ugc -R /ugc
RUN chmod +x ./wait-for-it.sh

USER ugc
CMD ["./wait-for-it.sh", "kafka:9092", "--", "python3", "main.py"]