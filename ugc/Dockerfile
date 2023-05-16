FROM python:3.10.8

RUN pip install --upgrade pip

ARG ROOT_DIR=/ugc

WORKDIR $ROOT_DIR

RUN groupadd -r ugc && useradd -d $ROOT_DIR -r -g ugc ugc

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ $ROOT_DIR
COPY entrypoint.sh $ROOT_DIR
RUN chown ugc:ugc -R $ROOT_DIR
RUN chmod +x entrypoint.sh

USER ugc

ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]