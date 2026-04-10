FROM node:25.2.1-alpine3.21 AS asset_builder

WORKDIR /app

COPY package.json package-lock.json rollup.config.js  ./
COPY . .
RUN npm ci
RUN npm run compile


FROM python:3.15.0a8-slim AS python_base

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

# Alpine doesn't support playwright
FROM python:3.15.0a8-slim AS development

ARG UID=1000
ENV USER=app
ENV APP_DIR=/app
RUN addgroup --gid $UID --system ${USER} \
    && adduser --uid $UID --system ${USER} --ingroup ${USER} \
    && mkdir -p ${APP_DIR} \
    && chown ${USER}:${USER} ${APP_DIR}

ENV VIRTUAL_ENV=${APP_DIR}/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

USER root
WORKDIR ${APP_DIR}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PLAYWRIGHT_BROWSERS_PATH=${APP_DIR}/browsers

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry install --no-root && rm -rf $POETRY_CACHE_DIR \
    && poetry run playwright install --with-deps chromium \
    && chown -R ${USER}:${USER} ${APP_DIR} \
    && rm -rf /root/.cache/pip /tmp/*

USER ${USER}
COPY --chown=${USER}:${USER} . .

ARG COMMIT_SHA
ENV COMMIT_SHA=$COMMIT_SHA

RUN echo "COMMIT_SHA: $COMMIT_SHA"

FROM python_base

USER ${USER}
WORKDIR /app

COPY --from=builder --chown=${USER}:${USER} ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=${USER}:${USER} ./lung_cancer_screening /app/lung_cancer_screening
COPY --from=asset_builder --chown=${USER}:${USER} /app/lung_cancer_screening/assets/compiled /app/lung_cancer_screening/assets/compiled
COPY --chown=${USER}:${USER} manage.py ./

RUN python ./manage.py collectstatic --noinput

EXPOSE 8000

ARG COMMIT_SHA
ENV COMMIT_SHA=$COMMIT_SHA

CMD ["/app/.venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "lung_cancer_screening.wsgi"]
