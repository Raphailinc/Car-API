import os
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


def parse_origins(raw_origins: str | None) -> list[str]:
    if not raw_origins:
        return DEFAULT_CORS_ORIGINS
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def load_config(app):
    base_dir = Path(__file__).resolve().parent.parent
    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///" + str(base_dir / "cars.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["ADMIN_TOKEN"] = os.getenv("ADMIN_TOKEN")

    cors_origins = parse_origins(os.getenv("CORS_ORIGINS"))
    trusted_origins_env = os.getenv("CORS_TRUSTED_ORIGINS")
    cors_trusted_origins = (
        parse_origins(trusted_origins_env) if trusted_origins_env is not None else cors_origins
    )
    app.config["CORS_ORIGINS"] = cors_origins
    app.config["CORS_TRUSTED_ORIGINS"] = cors_trusted_origins
