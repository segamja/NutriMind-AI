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

    return {
        "user": unquote(parsed.username or ""),
        "password": unquote(parsed.password or ""),
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "database": parsed.path.lstrip("/") or "postgres",
        "query": parse_qs(parsed.query),
    }


def build_conninfo(database_url: str) -> dict[str, str | int]:
    """Build libpq params from DATABASE_URL, ignoring stray PG* env vars."""
    cfg = parse_postgres_url(database_url)
    sslmode = cfg["query"].get("sslmode", ["prefer"])[0]
    if sslmode == "prefer" and (
        "supabase" in cfg["host"] or cfg["port"] == 6543
    ):
        sslmode = "require"

    return {
        "host": cfg["host"],
        "port": cfg["port"],
        "user": cfg["user"],
        "password": cfg["password"],
        "dbname": cfg["database"],
        "sslmode": sslmode,
        # Prevent PGHOSTADDR env (often set to hostname on Vercel) from breaking connect.
        "hostaddr": "",
    }


async def connect_postgres(database_url: str):
    import psycopg
    from psycopg.rows import dict_row

    return await psycopg.AsyncConnection.connect(
        build_conninfo(database_url),
        autocommit=True,
        prepare_threshold=None,
        row_factory=dict_row,
    )
