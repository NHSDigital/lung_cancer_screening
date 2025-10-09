# ruff: noqa: F403, F405
from .settings import *

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MIDDLEWARE.remove(
    "whitenoise.middleware.WhiteNoiseMiddleware",
)
