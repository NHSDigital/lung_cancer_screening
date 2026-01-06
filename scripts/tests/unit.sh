#!/bin/bash

echo Running Unit Tests

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

# This file is for you! Edit it to call your unit test suite. Note that the same
# file will be called if you run it locally as if you run it on CI.

# Replace the following line with something like:
#
#   rails test:unit
#   python manage.py test
#   npm run test
#
# or whatever is appropriate to your project. You should *only* run your fast
# tests from here. If you want to run other test suites, see the predefined
# tasks in scripts/test.mk.

if [[ -n "${TAG:-}" ]]; then
  TAG="--tag=$TAG"
else
  TAG=""
fi

if [[ -n "${TEST_MODULE:-}" ]]; then
  if [[ "$TEST_MODULE" == *\/* ]]; then
    # Modify paths to point to modules
    TEST_MODULE="${TEST_MODULE%.py}"
    TEST_MODULE=${TEST_MODULE//\//\.}
  fi
else
  TEST_MODULE=""
fi

docker compose run --rm --remove-orphans web poetry run python manage.py test $TEST_MODULE $TAG --settings=lung_cancer_screening.settings_test --exclude-tag=accessibility

