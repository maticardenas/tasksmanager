# --- BUILD STAGE ---
FROM python:3.11.7-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry/" \
    PATH="$POETRY_HOME/bin:$PATH"
    POETRY_VERSION=1.7.1 \
    DJANGO_SETTINGS_MODULE=taskmanager.production

RUN apt-get update \
     && apt-get install -y --no-install-recommends curl libpq-dev \

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualens.create false \
    && poetry install --no-dev --no-interaction --no-ansi \

COPY taskmanager /app

RUN poetry run python manage.py collectstatic --noinput


# --- PRODUCTION STAGE ---
FROM python:3.11.7-slim as production

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

WORKDIR /app

RUN groupadd -r django && useradd --no-log-init -r -g django && chown -R django:django /app

USER django

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taskmanager.wsgi"]

EXPOSE 8000