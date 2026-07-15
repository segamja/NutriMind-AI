import os
from urllib.parse import parse_qs, unquote, urlparse


def normalize_database_url(url: str) -> str:
    cleaned = url.strip().strip('"').strip("'")
    for prefix in ("postgresql+asyncpg://", "postgres+asyncpg://"):
        if cleaned.startswith(prefix):
            cleaned = "postgresql://" + cleaned[len(prefix) :]
    if cleaned.startswith("postgres://"):
        cleaned = "postgresql://" + cleaned[len("postgres://") :]
    return cleaned


def parse_postgres_url(url: str) -> dict:
    normalized = normalize_database_url(url)
    parsed = urlparse(normalized)
    if not parsed.hostname:
        raise ValueError("Invalid DATABASE_URL: missing host")

    port = parsed.port or 5432
    host = parsed.hostname

    # Supabase transaction pooler (6543) is unreliable on Vercel serverless.
    if port == 6543 and host and "pooler.supabase.com" in host:
        port = 5432

    return {
        "user": unquote(parsed.username or ""),
        "password": unquote(parsed.password or ""),
        "host": host,
        "port": port,
        "database": parsed.path.lstrip("/") or "postgres",
        "query": parse_qs(parsed.query),
    }


def build_conninfo(database_url: str) -> dict[str, str | int]:
    cfg = parse_postgres_url(database_url)
    sslmode = cfg["query"].get("sslmode", ["prefer"])[0]
    if sslmode == "prefer" and ("supabase" in cfg["host"] or cfg["port"] in (5432, 6543)):
        sslmode = "require"

    return {
        "host": cfg["host"],
        "port": cfg["port"],
        "user": cfg["user"],
        "password": cfg["password"],
        "dbname": cfg["database"],
        "sslmode": sslmode,
    }


def _clear_pg_env() -> dict[str, str]:
    env_keys = (
        "PGHOSTADDR",
        "PGHOST",
        "PGPORT",
        "PGUSER",
        "PGPASSWORD",
        "PGDATABASE",
        "PGSSLMODE",
    )
    return {key: os.environ.pop(key) for key in env_keys if key in os.environ}


async def connect_postgres(database_url: str):
    import psycopg
    from psycopg.rows import dict_row

    saved_env = _clear_pg_env()
    try:
        return await psycopg.AsyncConnection.connect(
            build_conninfo(database_url),
            autocommit=True,
            prepare_threshold=None,
            row_factory=dict_row,
        )
    finally:
        os.environ.update(saved_env)
