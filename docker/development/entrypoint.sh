#!/usr/bin/env sh

yarn install
poetry install

poetry run python manage.py makemigrations
poetry run python manage.py migrate

FILES=$(find service/seed -type f)
for file in $FILES; do
  poetry run python manage.py loaddata "$file"
done

exec yarn dev
