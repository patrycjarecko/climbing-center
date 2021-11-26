FROM nikolaik/python-nodejs:python3.9-nodejs16-alpine
RUN apk add gcc g++ make libffi-dev openssl-dev python3-dev build-base linux-headers zlib-dev jpeg-dev musl-dev cargo

RUN mkdir -p /app/media

COPY manage.py /app/
COPY pyproject.toml /app/
COPY poetry.lock /app/
COPY package.json /app/
COPY yarn.lock /app/
COPY *.config.js /app/
COPY django_icm /app/django_icm
COPY icm /app/icm
COPY docker /app/docker

WORKDIR /app
RUN touch db.sqlite3
RUN poetry install
RUN yarn install

RUN poetry run python manage.py migrate
RUN docker/production/seed.sh
RUN yarn build
RUN yes | poetry run python manage.py collectstatic

CMD poetry run python manage.py runserver 0.0.0.0:8000
