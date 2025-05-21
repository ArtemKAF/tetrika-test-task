FROM python:3.12.1-alpine3.19

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /workspace

COPY ./requirements.txt requirements.txt

RUN apk update --no-cache && \
    apk add --no-cache github-cli && \
    python -m pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir
