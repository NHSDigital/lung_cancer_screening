FROM node:25.2.1-alpine3.21 AS asset_builder

WORKDIR /app

COPY package.json package-lock.json rollup.config.js  ./
COPY . .
RUN npm ci
RUN npm run compile


FROM python:3.13.7-alpine3.21 AS python_base

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
FROM python:3.13.7-slim AS development

ENV UID=1000
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

# Install system dependencies needed for Playwright
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PLAYWRIGHT_BROWSERS_PATH=${APP_DIR}/browsers

COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
RUN poetry run playwright install --with-deps chromium

USER ${USER}
COPY --chown=${USER}:${USER} . .

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
