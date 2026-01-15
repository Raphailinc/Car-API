import os
from pathlib import Path

from dotenv import load_dotenv


def load_config(app):
    base_dir = Path(__file__).resolve().parent.parent
    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///" + str(base_dir / "cars.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
