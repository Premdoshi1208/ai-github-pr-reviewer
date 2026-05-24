FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir alembic sqlalchemy[asyncio] asyncpg psycopg2-binary

COPY alembic.ini .
COPY migrations ./migrations

CMD ["alembic", "-c", "alembic.ini", "upgrade", "head"]
