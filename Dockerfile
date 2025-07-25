FROM python:3.12-alpine3.19 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
COPY lung_cancer_screening ./lung_cancer_screening
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.12-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN apk add --no-cache \
    postgresql-libs \
    curl

RUN addgroup -g 1000 app && adduser -D -s /bin/sh -u 1000 -G app app

COPY --from=builder /opt/venv /opt/venv

RUN mkdir -p /app && chown -R app:app /app

WORKDIR /app

COPY --chown=app:app . .

USER app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
