#!/usr/bin/env sh

FILES=$(find icm/seed -type f)
for file in $FILES; do
  poetry run python manage.py loaddata "$file"
done
