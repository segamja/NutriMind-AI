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

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        if not origins:
            return ["*"]
        return origins

    @property
    def is_production_db(self) -> bool:
        return self.database_url.startswith("postgresql")


settings = Settings()
