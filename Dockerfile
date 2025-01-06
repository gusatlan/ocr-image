FROM python:3.11-slim-buster

ENV POETRY_VERSION=1.7.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libffi-dev \
    ffmpeg \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/ocr_image
RUN mkdir -p /ram/images
RUN mkdir -p /ram/data
RUN mkdir -p /ram/backup

VOLUME /ram/backup

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
ADD ocr_image/* /app/ocr_image/
RUN poetry install --no-root --only main

COPY . /app

CMD ["python", "ocr_image/main.py"]

