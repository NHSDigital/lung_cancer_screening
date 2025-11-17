# ruff: noqa: F403, F405
import logging

from .settings import *

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MIDDLEWARE.remove(
    "whitenoise.middleware.WhiteNoiseMiddleware",
)

INSTALLED_APPS += ["behave_django"]

logging.disable(logging.CRITICAL)
