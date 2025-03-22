FROM python:3.12-bookworm AS build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/app

RUN useradd \
    --uid 1001 \
    --no-log-init \
    --shell "/sbin/nologin" \
    --home "/nonexistent" \
    --system \
    --no-create-home \
    app_user


RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --upgrade pip && \
    pip install -r requirements.txt

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install --no-install-recommends -y \
    gdal-bin && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

RUN mkdir -p /var/www/media /var/www/static && \
    chown -R app_user:app_user /var/www/media /var/www/static && \
    chmod -R 700 /var/www/media /var/www/static && \
    chmod -R g+s /var/www/media /var/www/static


USER app_user

ENTRYPOINT ["./entrypoint.sh"]
