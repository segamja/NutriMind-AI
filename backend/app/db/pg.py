from urllib.parse import parse_qs, urlencode, urlparse, urlunparse, unquote


def normalize_database_url(url: str) -> str:
    cleaned = url.strip().strip('"').strip("'")
    for prefix in ("postgresql+asyncpg://", "postgres+asyncpg://"):
        if cleaned.startswith(prefix):
            cleaned = "postgresql://" + cleaned[len(prefix) :]
    if cleaned.startswith("postgres://"):
        cleaned = "postgresql://" + cleaned[len("postgres://") :]
    return cleaned


def prepare_psycopg_url(url: str) -> str:
    normalized = normalize_database_url(url)
    parsed = urlparse(normalized)
    query = parse_qs(parsed.query)

    if "sslmode" not in query and (
        "supabase" in (parsed.hostname or "") or parsed.port == 6543
    ):
        query["sslmode"] = ["require"]

    rebuilt = parsed._replace(query=urlencode(query, doseq=True))
    return urlunparse(rebuilt)


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
    }


async def connect_postgres(database_url: str):
    import psycopg
    from psycopg.rows import dict_row

    return await psycopg.AsyncConnection.connect(
        prepare_psycopg_url(database_url),
        autocommit=True,
        prepare_threshold=None,
        row_factory=dict_row,
    )
