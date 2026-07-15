import ssl
from urllib.parse import parse_qs, unquote, urlparse


def normalize_database_url(url: str) -> str:
    cleaned = url.strip()
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


def _should_use_ssl(host: str, port: int, query: dict) -> bool:
    sslmode = query.get("sslmode", ["prefer"])[0].lower()
    if sslmode in {"require", "verify-ca", "verify-full"}:
        return True
    return "supabase" in host or port == 6543


async def connect_postgres(database_url: str):
    import asyncpg

    cfg = parse_postgres_url(database_url)
    connect_kwargs: dict = {
        "user": cfg["user"],
        "password": cfg["password"],
        "host": cfg["host"],
        "port": cfg["port"],
        "database": cfg["database"],
        "statement_cache_size": 0,
    }

    if _should_use_ssl(cfg["host"], cfg["port"], cfg["query"]):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connect_kwargs["ssl"] = ssl_context

    return await asyncpg.connect(**connect_kwargs)
