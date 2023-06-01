FROM python:3.10.8

RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

ARG ROOT_DIR=/ugc
WORKDIR $ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$ROOT_DIR/src

RUN groupadd -r ugc && useradd -d $ROOT_DIR -r -g ugc ugc

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ $ROOT_DIR
RUN chown ugc:ugc -R $ROOT_DIR

USER ugc

CMD ["python", "src/main.py"]
