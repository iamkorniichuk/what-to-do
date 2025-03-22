FROM postgres:17-bookworm

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install --no-install-recommends  -y \
    postgis postgresql-17-postgis-3 \
    postgresql-17-postgis-3-scripts \
    postgresql-17-pgvector \
    && rm -rf /var/lib/apt/lists/*
