echo Running UI Tests

if [[ -n "${TAG:-}" ]]; then
  TAG="--tags=$TAG"
else
  TAG=""
fi

docker compose run --rm web poetry run python manage.py behave $TAG --settings=lung_cancer_screening.settings_test --no-skipped
