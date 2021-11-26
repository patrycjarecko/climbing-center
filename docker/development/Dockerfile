FROM nikolaik/python-nodejs:python3.9-nodejs16-alpine
RUN apk add gcc g++ make libffi-dev openssl-dev python3-dev build-base linux-headers zlib-dev jpeg-dev musl-dev cargo

COPY pyproject.toml /app/
COPY docker/development/entrypoint.sh /app/
WORKDIR /app
RUN poetry install

ENTRYPOINT ['./entrypoint.sh']