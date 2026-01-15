#!/bin/bash

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# This file is for you! Edit it to call your unit test suite. Note that the same
# file will be called if you run it locally as if you run it on CI.

# Replace the following line with something like:
#
#   rubocop
#   python manage.py lint
#   npm run lint
#
# or whatever is appropriate to your project. You should *only* run your fast
# tests from here. If you want to run other test suites, see the predefined
# tasks in scripts/lint.mk.

env UID="$(id -u)" docker compose run --rm web \
  poetry run ruff check --no-cache lung_cancer_screening
