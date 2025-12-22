FROM node:25.2.1-alpine3.21 AS asset_builder

WORKDIR /app

COPY package.json package-lock.json rollup.config.js  ./
COPY . .
RUN npm ci
RUN npm run compile


FROM python:3.14.1-alpine3.21 AS python_base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    USER=app

RUN addgroup --gid 1000 --system ${USER} \
    && adduser --uid 1000 --system ${USER} --ingroup ${USER}


FROM python_base AS builder

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


FROM python_base

USER ${USER}
WORKDIR /app

COPY --from=builder --chown=${USER}:${USER} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=${USER}:${USER} ./lung_cancer_screening /app/lung_cancer_screening
COPY --from=asset_builder --chown=${USER}:${USER} /app/lung_cancer_screening/assets/compiled /app/lung_cancer_screening/assets/compiled
COPY --chown=${USER}:${USER} manage.py ./

RUN python ./manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/app/.venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "lung_cancer_screening.wsgi"]
