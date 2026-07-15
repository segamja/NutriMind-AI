import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_vision_model: str = "gpt-4o-mini"
    database_url: str = "sqlite+aiosqlite:///./nutrimind.db"
    cors_origins: str = "http://localhost:5173,http://localhost:5174"
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_key: str = ""

    @property
    def service_role_key(self) -> str:
        return self.supabase_service_role_key or self.supabase_key

    @property
    def normalized_database_url(self) -> str:
        from app.db.pg import normalize_database_url

        return normalize_database_url(self.database_url)

    @property
    def resolved_supabase_url(self) -> str:
        if self.supabase_url:
            return self.supabase_url.rstrip("/")

        url = self.normalized_database_url
        if "@" in url and "pooler.supabase.com" in url:
            user = url.split("://", 1)[1].split("@", 1)[0].split(":", 1)[0]
            if user.startswith("postgres.") and len(user) > 9:
                project_ref = user.split(".", 1)[1]
                return f"https://{project_ref}.supabase.co"
        return ""

    @property
    def use_supabase_rest(self) -> bool:
        return bool(self.resolved_supabase_url and self.service_role_key)

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        if not origins:
            return ["*"]
        return origins

    @property
    def is_production_db(self) -> bool:
        return self.normalized_database_url.startswith("postgresql")

    @property
    def is_vercel(self) -> bool:
        return os.getenv("VERCEL") == "1"


settings = Settings()
